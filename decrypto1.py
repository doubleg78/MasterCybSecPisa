from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import binascii
import os

block = algorithms.AES.block_size/8

# filename = raw_input('Input file name to decrypt: ')
filename = 'giacomo.enc'

with open(filename, 'rb') as f:
    ciphertext = f.read()
    if len(ciphertext) % block != 0:
        print ('Error! file content is not multiple of 16')
        exit()

key_b = raw_input('Plese enter 16byte hex key: ')
key_hex = binascii.hexlify(key_b)
key_hex = key_b
if len(key_hex) % block != 0:
    print ('Error, key is not 16byte!')
    exit()
print len(ciphertext)
iv = ciphertext[:block]
cipher_fragment = ciphertext[block:]
print iv
print len(iv)
print cipher_fragment
print len(cipher_fragment)
ctx = Cipher(algorithms.AES(key_hex), modes.CBC(iv), default_backend()).decryptor()
a = ctx.update(ciphertext[block:])
print a
a2 = ctx.finalize()

print a + 'Len ' + str(len(a))
# print ciphertext + 'Len ' + str(len(ciphertext))

with open('giacomo.dec', 'wb') as f:
    f.write(a)
