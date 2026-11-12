import socket,time

###################################

IP="10.114.131.103"
PORT=1337

###################################

for i in range(100):

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
    print(leaked_ciphertext_text)


    enter_ciphertext_text=s.recv(1024)
    #print(enter_ciphertext_text)

    ciphertext=b""+b"\n"
    s.sendall(ciphertext)
    result_text=s.recv(1024)
    #print(result_text)