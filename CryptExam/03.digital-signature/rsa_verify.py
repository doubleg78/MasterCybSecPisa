# -*- coding: utf-8 -*-
"""
Created on Fri Mar 24 14:54:11 2017

@author: Pericle
"""

from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes

# Read the public key.
filename = raw_input('Type the PEM file containing the RSA public key: ')
with open(filename, 'rb') as f:
    pubkey_text = f.read()
    pubkey = serialization.load_pem_public_key(
        pubkey_text,
        backend=default_backend()
    )
    
# Read the file to verify.
filename = raw_input('Type the file to verify: ')
with open(filename, 'rb') as f:
    plaintext = f.read()

# Read the signature.
filename = raw_input('Type the signature file: ')
with open(filename, 'rb') as f:
    signature = f.read()

# Verify the file.
pubkey.verify(
    signature,
    plaintext,
    padding.PSS(
        mgf=padding.MGF1(hashes.SHA256()),
        salt_length=padding.PSS.MAX_LENGTH
    ),
    hashes.SHA256()
)

# If passing here, the verification is ok.
print 'Signature ok'
