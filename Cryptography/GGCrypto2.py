from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, hmac
from cryptography.hazmat.primitives import padding
import binascii
import os
import sys

block = algorithms.AES.block_size/8

# filename = raw_input('Input file name to crypt: ')
filename = 'giacomo.txt'

with open(filename, 'rb') as f:
    plaintext = f.read()
#    if len(plaintext) > block:
#        print ('Error! file content is not multiple of 16')
#        exit()

# k1 = raw_input('Please enter ' + str(2*block) + ' byte key1 (CryptKey): ')
k1 = 'e3ed4634f770a37fa2ba0a871fa13f44'
cryptkey = binascii.unhexlify(k1)
# k2 = raw_input('Please enter ' + str(2*block) + ' byte key2 (AuthKey): ')
k2 = '268e06f952e4a1233443722f8342a9f2'
authkey = binascii.unhexlify(k2)

if len(cryptkey) % block != 0:
    sys.exit('Error, key is not ' + str(2*block) + ' byte!')
if len(authkey) % block != 0:
    sys.exit('Error, key is not ' + str(2*block) + ' byte!')

ctx = padding.PKCS7(8*block).padder()
padded_plaintext = ctx.update(plaintext) + ctx.finalize()

iv = os.urandom(block)
cipher = Cipher(algorithms.AES(cryptkey), modes.CBC(iv), default_backend())
ctx = cipher.encryptor()
ciphertext = ctx.update(padded_plaintext) + ctx.finalize()

ctx = hmac.HMAC(authkey, hashes.SHA256(), default_backend())
ctx.update(iv)
ctx.update(ciphertext) # oppure per fare prima ctx.update(iv + ciphertext)
digest = ctx.finalize()

with open(filename + '.enc', 'wb') as f:
    f.write(digest)
    f.write(iv)
    f.write(ciphertext)
print('Encrypted file: ' + filename + '.enc')
