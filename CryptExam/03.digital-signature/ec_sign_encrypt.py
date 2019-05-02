# -*- coding: utf-8 -*-
"""
Created on Fri Apr 27 13:58:33 2018

@author: Pericle
"""

from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
import os
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

# Cipher block size, expressed in bytes.
block = algorithms.AES.block_size/8

# Read the private key.
filename = raw_input('Type the PEM file containing the EC private key: ')
with open(filename, 'rb') as f:
    prvkey_text = f.read()
    prvkey = serialization.load_pem_private_key(
        prvkey_text,
        password=None,
        backend=default_backend()
    )

# Read the file to sign.
filename = raw_input('Type the file to sign: ')
with open(filename, 'rb') as f:
    plaintext = f.read()

# Read the password to encrypt.
password = raw_input('Type the password to encrypt: ')

# Sign the file.
signature = prvkey.sign(
    plaintext,
    ec.ECDSA(hashes.SHA256())
)

# Write the signature in the output file.
with open(filename + '.sgn', 'wb') as f:
    f.write(signature)
print('Signature file: ' + filename + '.sgn')

# Compute an encryption key from the password.
salt = os.urandom(16)
ps = PBKDF2HMAC(
    hashes.SHA256(),
    length=16,
    salt=salt,
    iterations=10000,
    backend=default_backend()
)
key = ps.derive(password)

# Pad the plaintext to make it multiple of the block size.
ctx = padding.PKCS7(8*block).padder()
padded_plaintext = ctx.update(plaintext) + ctx.finalize()

# Encrypt the plaintext with a random IV.
iv = os.urandom(block)
cipher = Cipher(algorithms.AES(key), modes.CBC(iv), default_backend())
ctx = cipher.encryptor()
ciphertext = ctx.update(padded_plaintext) + ctx.finalize()

# Write the IV and the ciphertext in the output file.
with open(filename + '.enc', 'wb') as f:
    f.write(salt)
    f.write(iv)
    f.write(ciphertext)
print('Encrypted file: ' + filename + '.enc')
