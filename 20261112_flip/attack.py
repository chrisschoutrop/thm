import socket,time

###################################

IP="10.113.177.102"
PORT=1337

###################################

s = socket.create_connection((IP, PORT), timeout=5)
print(s.recv(1024))
username=b"admin"+b"\n"
s.sendall(username)
print(s.recv(1024))

#password=b"sUp3rPaSs1"+b"\n"
password=b"12345"+b"\n"
s.sendall(password)
print(s.recv(1024))

ciphertext=b"???"+b"\n"
s.sendall(ciphertext)
print(s.recv(1024))
