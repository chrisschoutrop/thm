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