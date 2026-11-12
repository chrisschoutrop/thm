import socket,time

###################################

IP="10.114.131.103"
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