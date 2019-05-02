# -*- coding: utf-8 -*-
"""
Created on Sat Mar 04 20:38:51 2017

@author: Pericle
"""

from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes

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
    
# Sign the file.
signature = prvkey.sign(
    plaintext,
    ec.ECDSA(hashes.SHA256())
)

# Write the signature in the output file.
with open(filename + '.sgn', 'wb') as f:
    f.write(signature)
print('Signature file: ' + filename + '.sgn')
