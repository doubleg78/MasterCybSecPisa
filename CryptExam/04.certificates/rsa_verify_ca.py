# -*- coding: utf-8 -*-
"""
Created on Thu Mar 30 13:17:43 2017

@author: Pericle
"""

from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography import x509
from cryptography.x509.oid import NameOID
import sys
import datetime

# Read the CA's certificate.
filename = raw_input('Type the PEM file containing the CA certificate: ')
with open(filename, 'rb') as f:
    ca_cert_text = f.read()
    ca_cert = x509.load_pem_x509_certificate(
        ca_cert_text,
        backend=default_backend()
    )

# Check the CA's certificate validity.
now = datetime.datetime.now()
if now < ca_cert.not_valid_before or now > ca_cert.not_valid_after:
    print 'ERROR. Invalid CA certificate.'
    sys.exit(1)

# Display the CA's name.
ca_name = ca_cert.subject.get_attributes_for_oid(NameOID.COMMON_NAME)[0].value
print 'CA name:', ca_name
ca_pubkey = ca_cert.public_key()

# Read the signer's certificate.
filename = raw_input('Type the PEM file containing the file signer certificate: ')
with open(filename, 'rb') as f:
    sgn_cert_text = f.read()
    sgn_cert = x509.load_pem_x509_certificate(
        sgn_cert_text,
        backend=default_backend()
    )

# Check the signer's certificate validity.
sgn_cert_issuer_name = sgn_cert.issuer.get_attributes_for_oid(NameOID.COMMON_NAME)[0].value
if sgn_cert_issuer_name != ca_name:
    print 'ERROR. Unknown CA: ', sgn_cert_issuer_name
    sys.exit(1)
if now < sgn_cert.not_valid_before or now > sgn_cert.not_valid_after:
    print 'ERROR. Invalid file signer certificate.'
    sys.exit(1)
ca_pubkey.verify(
    sgn_cert.signature,
    sgn_cert.tbs_certificate_bytes,
    padding.PKCS1v15(),
    hashes.SHA256()
)

# If passing here, the signer's certificate is ok.
sgn_name = sgn_cert.subject.get_attributes_for_oid(NameOID.COMMON_NAME)[0].value
print 'Certificate ok'
print 'File signer common name:', sgn_name

# Extract the signer's public key.
pubkey = sgn_cert.public_key()
                                                  
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
