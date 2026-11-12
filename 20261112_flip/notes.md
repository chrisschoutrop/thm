# Flip
## Hey, do a flip!
Difficulty: Easy
URL: https://tryhackme.com/room/flip

### Info given

Log in as the admin and capture the flag!

If you can...

Whenever you are ready, click on the Start Lab Machine button to fire up the Lab Machine. Please allow 3-5 minutes for the VM to fully start.

The server is listening on port 1337 via TCP. You can connect to it using Netcat or any other tool you prefer.

File: app-1684527681671.py

### Tasks
- What is the flag?

![alt text](IMAGE.png "Title")

# Content

Oke we hebben een Python script gekregen
### Dingen die opvallen:
- Het gaat iets van crypto doen met AES (CBC mode), padding (pkcs7), random bytes.
- Padding heeft zo'n "picklock" strategie misschien.
- `admin&password=sUp3rPaSs1`.
- Het start een server op port 1337.
- Server vraagt om username en password
- We mogen niet `admin&password=sUp3rPaSs1` direct in de message zetten.
- We krijgen ook de ciphertext te zien. Dus we hebben controle over deel van de input die de server encrypt.

### Attacking the crypto ideas:
- We hebben hier een chosen plaintext attack (CPA) misschien;
```python
message = 'access_username=' + username +'&password=' + password
send_message(server, "Leaked ciphertext: " + encrypt_data(message,key,iv)+'\n')
```
- We hebben controle over de input, er is een kans dat het de key en IV hergebruikt?
- Dit doet me denken aan die padding attack uit Yehuda \& Katz --> Sectie 3.7.2 Padding Oracle attacks in CPA.
Werkt dat ook voor PKCS7?
https://en.wikipedia.org/wiki/PKCS_7

### Scouting the server:
- Volgens de info kunnen we met ncat proberen. Als het moet kan ook met Python sockets zoals we bij `20261110_dearqa` hadden gedaan.
```
 sudo nmap -sCV  10.113.177.102
[sudo: authenticate] Password:                  
Starting Nmap 7.98 ( https://nmap.org ) at 2026-11-12 20:53 +0100
Nmap scan report for 10.113.177.102
Host is up (0.059s latency).
Not shown: 999 closed tcp ports (reset)
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 8.9p1 Ubuntu 3ubuntu0.13 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   256 a7:ac:80:07:0d:78:44:5c:d8:aa:02:61:73:c5:70:2c (ECDSA)
|_  256 e7:b1:7e:54:88:c4:47:6a:16:d8:21:d2:bb:dc:7d:4d (ED25519)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 2.22 seconds
```
```
$:~/Documents/tryhackme/20261112_flip$ ncat 10.113.177.102 1337
Welcome! Please login as the admin!
username: admin
admin's password: sUp3rPaSs1
Not that easy :)
Goodbye!
$:~/Documents/tryhackme/20261112_flip$ ncat 10.113.177.102 1337
Welcome! Please login as the admin!
username: admin
admin's password: 123
Leaked ciphertext: 757b4307fbe73a2d403159ff973952c03a347d30fd808e6a4cfc9b63d28cdc55ec35cd4e653c4b34f852125f3e574197
enter ciphertext: 757b4307fbe73a2d403159ff973952c03a347d30fd808e6a4cfc9b63d28cdc55ec35cd4e653c4b34f852125f3e574197
Flip off!$:~/Documents/tryhackme/20261112_flip$ ncat 10.113.177.102 1337
Welcome! Please login as the admin!
username: admin
admin's password: 1234
Leaked ciphertext: 3f9d53878dfade437ab8d67e795dbd801101996dcdddf6a9110b1053e72889321b8dbd26d1a8efdb4fb030d643503922
enter ciphertext: 123
Odd-length string
$:~/Documents/tryhackme/20261112_flip$ ncat 10.113.177.102 1337
Welcome! Please login as the admin!
username: admin
admin's password: 123
Leaked ciphertext: 49c9d6b965a76420585a9bedde5185c66ae76256574b8a1175b238ff4c23643d1fcedbb4e08e67f1b1313c6ca5a0043c
enter ciphertext: 49c9d6b965a76420585a9bedde5185c66ae76256574b8a1175b238ff4c23643d1fcedbb4e08e67f1b1313c6ca5a0043 
Odd-length string
$:~/Documents/tryhackme/20261112_flip$ ncat 10.113.177.102 1337
Welcome! Please login as the admin!
username: admin
admin's password: 123
Leaked ciphertext: 63cfe32aa4dc56c6834742289b5366445bdee976fe42c0063a3a9e7fbfbc32c037b077807181f0feebcaccddea8d9ded
enter ciphertext: 
Zero-length input cannot be unpadded
```
**Observaties:**
- Deze werkt niet: sUp3rPaSs1
- Ciphertext terug geven werkt niet.
- Bij gelijke input is de leaked cihertext compleet anders --> Key en IV zijn secure random ook in Python script.
- Er is een message als de padding niet klopt; `Odd-length string`
- Message bij lege ciphertext: `Zero-length input cannot be unpadded`
- Er gebeurt geen authenticatie in CBC mode.

**Ideas:**
- Kijken wat dat pkcs7 precies doet, en of het bekende problemen heeft: https://en.wikipedia.org/wiki/PKCS_7 . Het is sowieso enorm oud: 1 March 1998; 28 years ago was de laatste update.
- CVE-2025-7071 Het padding scenario is echt een probleem: https://www.oberon.ch/security-advisories/cve-2025-7071/; "ocrypto is vulnerable to a timing side-channel attack on its implementation of PKCS#7 padding removal. Its AES-CBC code (function ocrypto_aes_cbc_pkcs_final_dec in file ocrypto_aes_cbc_pkcs.c) is not constant-time: the timing differences between “no padding error” and “padding error” could be used by an attacker that is able to send thousands of ciphertexts as probes. First, the length of the actual message could be determined, and then byte by byte the actual message contents. All clients that use AES-CBC PKCS#7 are affected. "
- Blijkbaar hoeven we de key en de iv niet te weten hiervoor.
- Goed kijken wat `setup` functie eigenlijk doet.

```python
def start(server):
    # Key en IV zijn secure random elke poging
        key = get_random_bytes(16)
        iv = get_random_bytes(16)
        send_message(server, 'Welcome! Please login as the admin!\n')
        send_message(server, 'username: ')
        username = server.recv(4096).decode().strip()

        send_message(server, username +"'s password: ")
        password = server.recv(4096).decode().strip()

        message = 'access_username=' + username +'&password=' + password

        if "admin&password=sUp3rPaSs1" in message:
            send_message(server, 'Not that easy :)\nGoodbye!\n')
        else:
            setup(server,username,password,key,iv)

def setup(server,username,password,key,iv):
    # username & password zijn attacker controlled
        message = 'access_username=' + username +'&password=' + password
        send_message(server, "Leaked ciphertext: " + encrypt_data(message,key,iv)+'\n')
    # server encrypt het, en geeft ons de ciphertext van onze partially chosen plaintext
        send_message(server,"enter ciphertext: ")

        enc_message = server.recv(4096).decode().strip()

        try:
    # Met de leaked ciphertext moeten we iets geven wat decrypt met dezelfde key en iv
    # naar iets met `admin&password=sUp3rPaSs1` in de message.
                check = decrypt_data(enc_message,key,iv)
        except Exception as e:
                send_message(server, str(e) + '\n')
                server.close()

        if check:
                send_message(server, 'No way! You got it!\nA nice flag for you: '+ flag)
                server.close()
        else:
                send_message(server, 'Flip off!')
                server.close()

def encrypt_data(data,key,iv):
    padded = pad(data.encode(),16,style='pkcs7')
# AES op zich is een sterke primitieve
# CBC mode is OK, maar padding nodig als geen veelvoud van 128 bit is
    cipher = AES.new(key, AES.MODE_CBC,iv)
    enc = cipher.encrypt(padded)
    return enc.hex()

def decrypt_data(encryptedParams,key,iv):
    cipher = AES.new(key, AES.MODE_CBC,iv)
    paddedParams = cipher.decrypt( unhexlify(encryptedParams))
# Output moet b'admin&password=sUp3rPaSs1' bevatten voor de flag
    if b'admin&password=sUp3rPaSs1' in unpad(paddedParams,16,style='pkcs7'):
        return 1
    else:
        return 0
```

Oke wat ik denk dat sowieso nuttig gaat zijn is een script wat het volgende doet:
- Send username & password to server
- Receive back leaked ciphertext
- Able to send back the trial ciphertext

Deze hadden we voor `20261110_dearqa`:
```python
import socket, time

def recvuntil(N):
    s = socket.create_connection(('10.114.178.121', 5700), timeout=5)
    print(s.recv(1024))
    payload = b"A"*N + (0x40068a).to_bytes(8,'little') + b"\n"
    s.sendall(payload)
    time.sleep(1)
    try: 
        print(s.recv(4096))
    except: 
        pass

recvuntil(40)
```

Basic script `attack1.py`
```python
import socket,time

###################################

IP="10.113.177.102"
PORT=1337

###################################

s = socket.create_connection((IP, PORT), timeout=5)
welcome_text=s.recv(1024)
print(welcome_text)
welcome_text=s.recv(1024)
print(welcome_text)

username=b"admin"+b"\n"
s.sendall(username)

admin_password_text=s.recv(1024)
print(admin_password_text)

#password=b"sUp3rPaSs1"+b"\n"
password=b"12345"+b"\n"
s.sendall(password)
leaked_ciphertext_text=s.recv(1024)
print(leaked_ciphertext_text)


enter_ciphertext_text=s.recv(1024)
print(enter_ciphertext_text)

ciphertext=b"???"+b"\n"
s.sendall(ciphertext)
result_text=s.recv(1024)
print(result_text)
```

### Investigating the padding

Volgende is dat we moeten nalezen hoe de attack eigenlijk precies werkt; de padding oracle attack.

```python
import socketserver 
import socket, os
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad,unpad
from Crypto.Random import get_random_bytes
from binascii import unhexlify


data="A"
padded = pad(data.encode(),16,style='pkcs7')
print(padded)

data="A"*4
padded = pad(data.encode(),16,style='pkcs7')
print(padded)

data="A"*15
padded = pad(data.encode(),16,style='pkcs7')
print(padded)

data="A"*16
padded = pad(data.encode(),16,style='pkcs7')
print(padded)

data="A"*17
padded = pad(data.encode(),16,style='pkcs7')
print(padded)
```
```log
python3 padding_experiment.py 
b'A\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f'
b'AAAA\x0c\x0c\x0c\x0c\x0c\x0c\x0c\x0c\x0c\x0c\x0c\x0c'
b'AAAAAAAAAAAAAAA\x01'
b'AAAAAAAAAAAAAAAA\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10'
b'AAAAAAAAAAAAAAAAA\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f'
```
Dus hoe het werkt:
- We moeten een blok vullen van 16
- Alles wat niet data is vullen we met hoeveel nog empty is;
- - 1xA  -> 0x0F empty -> 0x0F keer 0x0F als padding
- - 4xA  -> 0x0C empty -> 0x0C keer 0x0C als padding
- - 15xA -> 0x01 empty -> 0x01 keer 0x01 als padding
- - 16xA -> Blok is vol, voeg altijd toch gewoon een blok toe -> 16 bytes toevoegen -> 0x10 keer 0x10
- - 17xA  -> 0x0F empty tot blok2 vol -> 0x0F keer 0x0F als padding, dan is ook blok 2 vol.

Hoe is dit te exploiten?
- We weten iets over de plaintext, namelijk waarop het eindigt, want lengte is bekend, dus we weten hoeveel mist tot volgend blok, dus we weten wat dit padding scheme toevoegt om het blok vol te maken.
Geldig voorbeeld:
- `plaintext=[blok1][blok2][\x41\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f]`
- `plaintext=[blok1][blok2][\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10]`
Ongeldig voorbeeld:
- `plaintext=[blok1][blok2][\x10\x10\x10\x10\x10\x10\x10\x10\x10]`

### Samenvatten
- We kunnen automatisch communiceren met de server via Python script.
- We weten nu hoe de padding werkt.
- We hebben een idee dat hier een padding attack moet gebeuren in zekere zin.
- We weten nog niet helemaal wat we precies eruit moeten kunnen krijgen;
- - De inputs zijn deels gekozen door attacker
- - IV en key zijn random en niet gerecycled, want de server stopt bij een foute poging
- - Gegeven een enkele output van een encryption oracle moeten we een message opstellen wat decrypt naar iets met `admin&password=sUp3rPaSs1` erin?

### Ideeën
- Stel ipv AES hebben we iets wat gewoon 1:1 input terug geeft.
- - Dan is het triviaal want "ciphertext" is dan gewoon de message die we willen hebben als plaintext
- Ik denk ergens niet dat we met 1 encryption de key en iv kunnen krijgen in het algemeen
- - Stel plaintext xor IV -> AES(k) -> ciphertext, IV allemaal 0 voor gemak
- - plaintext -> AES(k) -> ciphertext, wat was k?
- - Volgens mij kan dit niet, want dan kun je met 1 chosen plaintext AES ondermijnen, dat lijkt me sterk;
Boek zegt over CPA-security:
"Chosen-plaintext attacks capture the ability of an adversary to exercise
(partial) control over what the honest parties encrypt. We imagine a scenario
in which two honest parties share a key k, and the attacker can influence
these parties to encrypt messages m1, m2, . . . (using k) and send the resulting
ciphertexts over a channel that the attacker can observe. At some later point
in time, the attacker observes a ciphertext corresponding to some unknown
message m encrypted using the same key k; let us even assume that the
attacker knows that m is one of two possibilities m0, m1. Security against
chosen-plaintext attacks means that even in this case the attacker cannot
tell which of these two messages was encrypted with probability significantly
better than random guessing. "
- - Dus er moet iets anders aan de hand zijn, en ik vermoed dat het met die padding te doen heeft somehow.
- Dingen concatenaten is tricky, want CBC propagate van begin tot einde, we kunnen niet blokken omdraaien zonder dat dat alle volgende blokken kapot maakt.
![alt text](Screenshot_20261112_220747.png "Title")
- 'admin&password=sUp3rPaSs1' moet ergens in de output staan, maakt niet uit waar. 
- We weten wel de "IV" als we blokken achteraan willen plakken, want dat is het laatste ciphertext blok bij CBC.

--> Even pauze nemen
--> Goed het boek lezen sectie 3.7.2.
--> Check als password langer is dat dan ook leaked ciphertext langer is