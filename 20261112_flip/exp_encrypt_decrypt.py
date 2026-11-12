import socketserver 
import socket, os
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad,unpad
from Crypto.Random import get_random_bytes
from binascii import unhexlify,hexlify


def encrypt_data(data,key,iv):
    padded = pad(data.encode(),16,style='pkcs7')
    cipher = AES.new(key, AES.MODE_CBC,iv)
    enc = cipher.encrypt(padded)
    return enc.hex()

def decrypt_data(encryptedParams,key,iv):
    cipher = AES.new(key, AES.MODE_CBC,iv)
    paddedParams = cipher.decrypt( unhexlify(encryptedParams))
    return unpad(paddedParams,16,style='pkcs7')
    if b'admin&password=sUp3rPaSs1' in unpad(paddedParams,16,style='pkcs7'):
        return 1
    else:
        return 0

key = unhexlify(b'401237dd2399b183309b4586ffbef0a8') #get_random_bytes(16)
iv = unhexlify(b'3f0030664177d3e65e44039375bd9923') #get_random_bytes(16)
#print(hexlify(key))
#print(hexlify(iv))

message="HORSE"
leaked_ciphertext=encrypt_data(message,key,iv)
print(leaked_ciphertext)
decrypted=decrypt_data(leaked_ciphertext,key,iv)
print(decrypted)

message="HORSE"
leaked_ciphertext=encrypt_data(message,key,iv)
a=list(str(leaked_ciphertext))
a[0]='c'
a=''.join(a)
print(a)
leaked_ciphertext=a
#decrypted=decrypt_data(leaked_ciphertext,key,iv)
decrypted=decrypt_data("b69bfb8d1450cf04a89de7c50c9623ba",key,iv)
print(decrypted)