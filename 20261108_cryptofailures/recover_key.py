#!/usr/bin/env python3
"""
Recover the Crypto Failures ENC_SECRET_KEY using the "1 unknown char per 8-byte block" attack.

Usage:
    pip install requests
    # optioneel als PHP niet beschikbaar is:
    # pip install passlib

    python3 recover_key.py --base http://10.114.131.3
"""

import argparse
import os
import shutil
import string
import subprocess
import sys
import time
import urllib.parse

try:
    import requests
except ImportError:
    print("Dit script heeft 'requests' nodig: pip install requests", file=sys.stderr)
    sys.exit(1)


DEFAULT_BASE = "http://10.114.131.3"
USER = "guest"
BASE_UA_LEN = 16

# Standaard charset uit je notes, plus een paar veelvoorkomende extra's.
DEFAULT_CHARSET = (
    "0123456789"
    "abcdefghijklmnopqrstuvwxyz"
    "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    "_{}-./%+="
)

# Fallback als de standaard charset niet genoeg is: alle printable ASCII, behalve control chars.
EXTENDED_CHARSET = "".join(c for c in string.printable if c not in "\t\n\r\x0b\x0c")


BACKEND = None
PHP = None
CRYPT_FUNC = None
PASSLIB_VERIFY = None


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


class PhpBackend:
    def __init__(self, php_bin):
        self.php = php_bin

    def _run(self, code, *args):
        env = os.environ.copy()
        env["LC_ALL"] = "C"
        proc = subprocess.run(
            [self.php, "-r", code] + list(args),
            capture_output=True,
            text=True,
            env=env,
        )
        if proc.returncode != 0:
            raise RuntimeError(f"PHP CLI mislukt:\n{proc.stderr}")
        return proc.stdout

    def one(self, password, salt):
        out = self._run(
            "echo crypt($argv[1], $argv[2]);",
            password,
            salt,
        )
        return out.strip()

    def hashes_for_prefix(self, prefix, salt, charset):
        code = r'''
$salt = $argv[1];
$prefix = $argv[2];
$charset = $argv[3];
for ($i = 0; $i < strlen($charset); $i++) {
    echo crypt($prefix . $charset[$i], $salt), "\n";
}
'''
        out = self._run(code, salt, prefix, charset)
        lines = [line.strip() for line in out.splitlines() if line.strip()]

        if len(lines) != len(charset):
            # Soms kan er extra output staan; probeer dan de laatste N regels.
            if len(lines) > len(charset):
                lines = lines[-len(charset):]
            else:
                raise RuntimeError(
                    f"PHP gaf {len(lines)} hashes, maar verwachtte {len(charset)}. "
                    "Controleer of PHP CLI dezelfde crypt() implementatie gebruikt als de target."
                )

        return lines


def init_backend(php_bin=None):
    global BACKEND, PHP, CRYPT_FUNC, PASSLIB_VERIFY

    php = php_bin or shutil.which("php")
    if php:
        BACKEND = "php"
        PHP = PhpBackend(php)
        eprint(f"[+] Backend: PHP CLI ({php})")
        return

    try:
        import crypt as _crypt_mod

        def _crypt(password, salt):
            # Python's crypt module kan bytes of str; we houden het expliciet ASCII.
            return _crypt_mod.crypt(
                password.encode("utf-8"),
                salt.encode("utf-8"),
            ).decode("ascii")

        BACKEND = "crypt"
        CRYPT_FUNC = _crypt
        eprint("[+] Backend: Python crypt module")
        return
    except Exception:
        pass

    try:
        from passlib.hash import des_crypt as _des_crypt

        def _verify(secret, hash_value):
            try:
                return bool(_des_crypt.verify(secret, hash_value))
            except Exception:
                return False

        BACKEND = "passlib"
        PASSLIB_VERIFY = _verify
        eprint("[+] Backend: passlib.des_crypt")
        return
    except Exception:
        pass

    raise RuntimeError(
        "Geen geschikte crypt-backend gevonden.\n"
        "Installeer PHP CLI, of gebruik een Python met de 'crypt' module, of:\n"
        "    pip install passlib"
    )


def self_test():
    """
    Controleer of onze lokale crypt() overeenkomt met het voorbeeld uit je notes:

        php run_crypt.php guest:Mo MA
        MAQ55hx59Xoc6
    """
    expected = "MAQ55hx59Xoc6"

    if BACKEND == "php":
        return PHP.one("guest:Mo", "MA").strip() == expected

    if BACKEND == "crypt":
        return CRYPT_FUNC("guest:Mo", "MA") == expected

    if BACKEND == "passlib":
        return PASSLIB_VERIFY("guest:Mo", expected)

    raise RuntimeError("Onbekende backend tijdens self-test.")


def get_fresh_cookie(base, ua):
    """
    Vraag een verse guest-cookie op met de opgegeven User-Agent.

    De target genereert deze cookie als we geen secure_cookie/user cookies meesturen:
        plaintext = "guest:" . UA . ":" . ENC_SECRET_KEY
    """
    headers = {"User-Agent": ua}
    resp = requests.get(base, headers=headers, allow_redirects=False, timeout=10)

    value = None

    # Normale route: requests heeft de Set-Cookie al geparseerd.
    if "secure_cookie" in resp.cookies:
        value = resp.cookies["secure_cookie"]
    else:
        # Fallback: probeer ruwe Set-Cookie headers te parsen.
        try:
            for sc in resp.raw.headers.getlist("Set-Cookie"):
                if "secure_cookie=" in sc:
                    value = sc.split("secure_cookie=", 1)[1].split(";", 1)[0]
                    break
        except Exception:
            pass

    if not value:
        raise RuntimeError(
            "Kon 'secure_cookie' niet vinden in de response. "
            "Check of --base klopt en of de target nog steeds cookies genereert."
        )

    # In je notes staat dat '/' soms als %2F voorkwam. Decode dus percent-encoding.
    value = urllib.parse.unquote(value).strip().strip('"')
    return value


def split_blocks(cookie):
    """
    secure_cookie is een concatenatie van 13-char DES-crypt blokken:
        [salt][11 base64-ish chars] per blok
    """
    if len(cookie) % 13 != 0:
        raise ValueError(
            f"Cookie lengte {len(cookie)} is geen veelvoud van 13. "
            "Misschien is de cookie niet correct gedecodeerd of heeft de target een andere format."
        )

    return [cookie[i:i + 13] for i in range(0, len(cookie), 13)]


def find_char(prefix7, salt, target_hash, charset):
    """
    Gegeven:
      - prefix7: bekende eerste 7 bytes van een 8-byte blok
      - salt:    de salt uit de verse cookie
      - target_hash: het 13-char crypt-blok dat de target heeft gegenereerd

    Zoek het 8ste karakter.
    """
    matches = []

    if BACKEND == "php":
        hashes = PHP.hashes_for_prefix(prefix7, salt, charset)
        for c, h in zip(charset, hashes):
            if h == target_hash:
                matches.append(c)

    elif BACKEND == "crypt":
        for c in charset:
            if CRYPT_FUNC(prefix7 + c, salt) == target_hash:
                matches.append(c)

    else:  # passlib
        for c in charset:
            if PASSLIB_VERIFY(prefix7 + c, target_hash):
                matches.append(c)

    return matches


def recover(args):
    key = []
    j = 0

    while j < args.max_len:
        """
        We willen dat KEY[j] de 8ste byte is van een blok.

        plaintext = USER . ":" . UA . ":" . KEY
                   guest:<UA>:<KEY>

        Voor USER="guest":
            prefix lengte = ua_len + len("guest") + 2 = ua_len + 7
            positie van KEY[0] (1-indexed) = ua_len + 8
            positie van KEY[j]             = ua_len + 8 + j

        We kiezen ua_len zodat:
            (ua_len + len(USER) + 3 + j) % 8 == 0
        """
        offset = (-(args.base_ua_len + len(USER) + 3 + j)) % 8
        ua_len = args.base_ua_len + offset
        ua = "A" * ua_len

        cookie = get_fresh_cookie(args.base, ua)
        blocks = split_blocks(cookie)
        salt = cookie[:2]

        prefix_known = USER + ":" + ua + ":"
        p = len(prefix_known) + 1 + j  # 1-indexed positie van het onbekende key-karakter

        if p % 8 != 0:
            raise RuntimeError("Interne alignement-bug: onbekend karakter zit niet op blok-einde.")

        block_index = (p - 1) // 8

        if block_index >= len(blocks):
            eprint(f"[*] Blok {block_index} bestaat niet meer; stop bij pos {j}.")
            break

        target_hash = blocks[block_index]

        # Bouw de bekende 7 bytes vóór het onbekende karakter.
        known = []
        ok = True

        for t in range(7):
            pos = p - 7 + t  # posities p-7 .. p-1, dus de 7 bytes vóór KEY[j]

            if pos <= len(prefix_known):
                # Deze byte zit in "guest:<UA>:"
                known.append(prefix_known[pos - 1])
            else:
                # Deze byte is een eerder herkend key-karakter.
                key_idx = pos - (len(prefix_known) + 1)
                if key_idx < 0 or key_idx >= len(key):
                    ok = False
                    break
                known.append(key[key_idx])

        if not ok:
            eprint(f"[*] Nog niet genoeg key-karakters bekend; stop bij pos {j}.")
            break

        prefix7 = "".join(known)

        matches = find_char(prefix7, salt, target_hash, args.charset)

        # Als de standaard charset te smal is, probeer dan breder.
        if not matches:
            eprint("[*] Geen match in --charset; probeer brede printable-ASCII charset...")
            matches = find_char(prefix7, salt, target_hash, EXTENDED_CHARSET)

        if not matches:
            eprint(f"[*] Stop bij pos {j}: geen kandidaat matched.")
            break

        if len(matches) > 1:
            eprint(f"[!] Meerdere matches voor pos {j}: {matches!r}; kies de eerste.")

        ch = matches[0]
        key.append(ch)

        eprint(
            f"[+] pos={j:3d} "
            f"ua_len={ua_len:3d} "
            f"blok={block_index:2d} "
            f"char={ch!r}"
        )

        j += 1

        if args.delay > 0:
            time.sleep(args.delay)

    return "".join(key)


def main():
    ap = argparse.ArgumentParser(
        description="Recover de Crypto Failures ENC_SECRET_KEY met de 1-char-per-blok aanpak."
    )
    ap.add_argument("--base", default=DEFAULT_BASE, help="Target URL, bijv. http://10.114.131.3")
    ap.add_argument("--charset", default=DEFAULT_CHARSET, help="Charset voor key-karakters.")
    ap.add_argument("--max-len", type=int, default=256, help="Maximale key-lengte om te proberen.")
    ap.add_argument(
        "--base-ua-len",
        type=int,
        default=BASE_UA_LEN,
        help="Basis User-Agent lengte; wordt afgerond naar een veelvoud van 8.",
    )
    ap.add_argument("--delay", type=float, default=0.0, help="Sleep tussen requests in seconden.")
    ap.add_argument("--php-bin", default=None, help="Pad naar php binaire, optioneel.")
    ap.add_argument("--no-self-test", action="store_true", help="Sla de crypt self-test over.")
    args = ap.parse_args()

    # Zorg dat de basis UA-lengte een veelvoud van 8 is.
    if args.base_ua_len < 8:
        args.base_ua_len = 16
    args.base_ua_len -= args.base_ua_len % 8
    if args.base_ua_len == 0:
        args.base_ua_len = 16

    init_backend(args.php_bin)

    if not args.no_self_test:
        try:
            ok = self_test()
        except Exception as exc:
            eprint(f"[-] Self-test mislukt: {exc}")
            sys.exit(1)

        if not ok:
            eprint(
                "[-] Self-test mislukt.\n"
                "    Lokale crypt() komt niet overeen met het voorbeeld uit je notes:\n"
                '        crypt("guest:Mo", "MA") == "MAQ55hx59Xoc6"\n'
                "    Probeer een andere backend, bijv. PHP CLI of passlib."
            )
            sys.exit(1)

        eprint("[+] Self-test OK.")

    key = recover(args)

    if not key:
        eprint("[-] Geen key herkend.")
        sys.exit(1)

    # Eindkey naar stdout, zodat je hem makkelijk kunt kopiëren.
    print(key)


if __name__ == "__main__":
    main()
