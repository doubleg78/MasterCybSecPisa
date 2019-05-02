# -*- coding: utf-8 -*-
"""
Created on Fri Apr 27 14:07:34 2018

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

# Read the public key.
filename = raw_input('Type the PEM file containing the EC public key: ')
with open(filename, 'rb') as f:
    pubkey_text = f.read()
    pubkey = serialization.load_pem_public_key(
        pubkey_text,
        backend=default_backend()
    )
    
# Read the encrypted file to verify.
filename = raw_input('Type the encrypted file to verify: ')
with open(filename, 'rb') as f:
    salt = f.read(16)
    iv = f.read(block)
    ciphertext = f.read()

# Read the password to decrypt.
password = raw_input('Type the password to decrypt: ')

# Read the signature.
filename = raw_input('Type the signature file: ')
with open(filename, 'rb') as f:
    signature = f.read()

# Compute the encryption key from the password and the salt.
ps = PBKDF2HMAC(
    hashes.SHA256(),
    length=16,
    salt=salt,
    iterations=10000,
    backend=default_backend()
)
key = ps.derive(password)

# Decrypt the ciphertext.
cipher = Cipher(algorithms.AES(key), modes.CBC(iv), default_backend())
ctx = cipher.decryptor()
padded_plaintext = ctx.update(ciphertext) + ctx.finalize()

# Unpad the plaintext.
ctx = padding.PKCS7(8*block).unpadder()
plaintext = ctx.update(padded_plaintext) + ctx.finalize()

# Write the decrypted text in the output file.
with open(filename + '.dec', 'wb') as f:
    f.write(plaintext)
print('Decrypted file: ' + filename + '.dec')

# Verify the file.
pubkey.verify(
    signature,
    plaintext,
    ec.ECDSA(hashes.SHA256())
)

# If passing here, the verification is ok.
print 'Signature ok'
