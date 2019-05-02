# -*- coding: utf-8 -*-
"""
Created on Sat Mar 04 20:38:51 2017

@author: Pericle
"""

import sys
import binascii
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

block = algorithms.AES.block_size/8

filename = raw_input('Type the file to decrypt: ')
with open(filename, 'rb') as f:
    iv = f.read(block)
    ciphertext = f.read()
if len(ciphertext) % block != 0:
    sys.exit('The file must be multiple of ' + str(block) + ' bytes.')

key_hex = raw_input('Type the key in ' + str(2*block) + ' hexadecimal digits: ')
key = binascii.unhexlify(key_hex)

cipher = Cipher(algorithms.AES(key), modes.CBC(iv), default_backend())
ctx = cipher.decryptor()
padded_plaintext = ctx.update(ciphertext) + ctx.finalize()

ctx = padding.PKCS7(8*block).unpadder()
plaintext = ctx.update(padded_plaintext) + ctx.finalize()

with open(filename + '.dec', 'wb') as f:
    f.write(plaintext)
print('Decrypted file: ' + filename + '.dec')
