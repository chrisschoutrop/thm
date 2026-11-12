import socket,time
import random
from Crypto.Random import get_random_bytes

###################################

IP="10.114.131.103"
PORT=1337

###################################

for i in range(1,100):

    s = socket.create_connection((IP, PORT), timeout=5)
    welcome_text1=s.recv(1024)
    #print(welcome_text1)
    welcome_text2=s.recv(1024)
    #print(welcome_text2)

    username=b""+b"\n"
    s.sendall(username)

    admin_password_text=s.recv(1024)
    #print(admin_password_text)

    #password=b"sUp3rPaSs1"+b"\n"
    password=b""+b"\n"
    s.sendall(password)
    leaked_ciphertext_text=s.recv(1024)
    #print(leaked_ciphertext_text)


    enter_ciphertext_text=s.recv(1024)
    #print(enter_ciphertext_text)

    #ciphertext=get_random_bytes(i)+b"\n"
    #ciphertext=b"????\n"
    ciphertext=''.join(random.choice('0123456789abcdef') for n in range(i))
    ciphertext=bytes(ciphertext,'ascii')
    #print(ciphertext)
    s.sendall(ciphertext)
    result_text=s.recv(1024)
    print(f"{i=} : {result_text=}")