from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import binascii
import os

block = algorithms.AES.block_size/8

# filename = raw_input('Input file name: ')
filename = 'giacomo.txt'

with open(filename, 'rb') as f:
    plaintext_fragment = f.read()
    if len(plaintext_fragment) > block:
        print ('Error! file content is not multiple of 16')
        exit()

print plaintext_fragment
key_b = raw_input('Plese enter 16byte hex key: ')
key_hex = binascii.hexlify(key_b)
key_hex = key_b
if len(key_hex) % block != 0:
    print ('Error, key is not 16byte!')
    exit()

iv = os.urandom(block)
print len(iv)
print iv
cipher = Cipher(algorithms.AES(key_hex), modes.CBC(iv), default_backend())
ctx = cipher.encryptor()
ciphertext_fragment = ctx.update(plaintext_fragment)
last_ciphertext_fragment = ctx.finalize()

print ciphertext_fragment
print last_ciphertext_fragment

ciphertext = iv+ciphertext_fragment+last_ciphertext_fragment

# print ciphertext_fragment + 'Len ' + str(len(ciphertext_fragment))
# print ciphertext + 'Len ' + str(len(ciphertext))
with open('giacomo.enc', 'wb') as f:
    f.write(ciphertext)
