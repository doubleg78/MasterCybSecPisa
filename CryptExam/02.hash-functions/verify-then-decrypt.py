# -*- coding: utf-8 -*-
"""
Created on Sat Mar 04 20:38:51 2017

@author: Pericle
"""

import sys
import binascii
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import hashes, hmac
from cryptography.hazmat.backends import default_backend

# Cipher block size, expressed in bytes.
block = algorithms.AES.block_size/8

# Read the MAC, the IV, and the ciphertext from a file.
filename = raw_input('Type the file to verify-then-decrypt: ')
with open(filename, 'rb') as f:
    digest_from_file = f.read(hashes.SHA256.digest_size)
    iv = f.read(block)
    ciphertext = f.read()
if len(ciphertext) % block != 0:
    sys.exit('The ciphertext must be multiple of ' + str(block) + ' bytes.')

# Read the keys in hexadecimal digits from keyboard.
key_hex = raw_input('Type the encryption key in ' + str(2*block) + ' hexadecimal digits: ')
cryptkey = binascii.unhexlify(key_hex)
key_hex = raw_input('Type the authentication key in ' + str(2*block) + ' hexadecimal digits: ')
authkey = binascii.unhexlify(key_hex)

# Verify the authenticity of the ciphertext.
# In case the verification fails, ctx.verify() will rise an exception which will cause the execution to stop.
ctx = hmac.HMAC(authkey, hashes.SHA256(), default_backend())
ctx.update(iv)
ctx.update(ciphertext)
ctx.verify(digest_from_file)

# Decrypt the ciphertext.
cipher = Cipher(algorithms.AES(cryptkey), modes.CBC(iv), default_backend())
ctx = cipher.decryptor()
padded_plaintext = ctx.update(ciphertext) + ctx.finalize()

# Unpad the plaintext.
ctx = padding.PKCS7(8*block).unpadder()
plaintext = ctx.update(padded_plaintext) + ctx.finalize()

# Write the decrypted text in the output file.
with open(filename + '.dec', 'wb') as f:
    f.write(plaintext)
print('Verified-then-decrypted file: ' + filename + '.dec')
