from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
import binascii
import os

block = algorithms.AES.block_size/8

# filename = raw_input('Type the file to encrypt: ')
filename = 'giacomo.txt'

with open(filename, 'rb') as f:
    plaintext = f.read()
#    if len(plaintext) > block:
#        print ('Error! file content is not multiple of 16')
#        exit()

# key_hex = raw_input('Plese enter + ' str(2*block) ' + hex digits: ')
key_hex = '70bf1fb7756bdcf8e6a77d606807b44c'
key = binascii.unhexlify(key_hex)

if len(key) % block != 0:
    print ('Error, key is not 16byte!')
    exit()

ctx = padding.PKCS7(8*block).padder()
padded_plaintext = ctx.update(plaintext) + ctx.finalize()


iv = os.urandom(block)
cipher = Cipher(algorithms.AES(key), modes.CBC(iv), default_backend())
ctx = cipher.encryptor()
ciphertext = ctx.update(padded_plaintext) + ctx.finalize()

# ciphertext = iv+ciphertext_fragment+last_ciphertext_fragment

with open(filename + '.enc', 'wb') as f:
    f.write(iv)
    f.write(ciphertext)
print('Encrypted file: ' + filename + '.enc')