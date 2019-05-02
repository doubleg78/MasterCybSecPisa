from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.asymmetric import padding  # RSA
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend  # RSA
from cryptography.hazmat.primitives import hashes  # RSA
from cryptography.hazmat.primitives import hmac
from cryptography.hazmat.primitives import serialization  # RSA
from cryptography import x509  # CERT
from cryptography.x509.oid import NameOID  # CERT
import binascii
import os
import sys


def symmetric_encryption_without_padding():
    block = algorithms.AES.block_size / 8

    filename = raw_input('Type the file to encrypt: ')
    with open(filename, 'rb') as f:
        plaintext = f.read()
    if len(plaintext) % block != 0:
        sys.exit('The file must be multiple of ' + str(block) + ' bytes.')

    key_hex = raw_input('Type the key in ' + str(2 * block) + ' hexadecimal digits: ')
    key = binascii.unhexlify(key_hex)

    iv = os.urandom(block)
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), default_backend())
    ctx = cipher.encryptor()
    ciphertext = ctx.update(plaintext) + ctx.finalize()

    with open(filename + '.enc', 'wb') as f:
        f.write(iv)
        f.write(ciphertext)
    print('Encrypted file: ' + filename + '.enc')


def symmetric_decryption_without_padding():
    block = algorithms.AES.block_size / 8

    filename = raw_input('Type the file to decrypt: ')
    with open(filename, 'rb') as f:
        iv = f.read(block)
        ciphertext = f.read()
    if len(ciphertext) % block != 0:
        sys.exit('The file must be multiple of ' + str(block) + ' bytes.')

    key_hex = raw_input('Type the key in ' + str(2 * block) + ' hexadecimal digits: ')
    key = binascii.unhexlify(key_hex)

    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), default_backend())
    ctx = cipher.decryptor()
    plaintext = ctx.update(ciphertext) + ctx.finalize()

    with open(filename + '.dec', 'wb') as f:
        f.write(plaintext)
    print('Decrypted file: ' + filename + '.dec')


def symmetric_encryption_with_padding():
    block = algorithms.AES.block_size / 8

    filename = raw_input('Type the file to encrypt: ')
    with open(filename, 'rb') as f:
        plaintext = f.read()

    key_hex = raw_input('Type the key in ' + str(2 * block) + ' hexadecimal digits: ')
    key = binascii.unhexlify(key_hex)

    ctx = padding.PKCS7(8 * block).padder()
    padded_plaintext = ctx.update(plaintext) + ctx.finalize()

    iv = os.urandom(block)
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), default_backend())
    ctx = cipher.encryptor()
    ciphertext = ctx.update(padded_plaintext) + ctx.finalize()

    with open(filename + '.enc', 'wb') as f:
        f.write(iv)
        f.write(ciphertext)
    print('Encrypted file: ' + filename + '.enc')


def symmetric_decryption_with_padding():
    block = algorithms.AES.block_size / 8

    filename = raw_input('Type the file to decrypt: ')
    with open(filename, 'rb') as f:
        iv = f.read(block)
        ciphertext = f.read()
    if len(ciphertext) % block != 0:
        sys.exit('The file must be multiple of ' + str(block) + ' bytes.')

    key_hex = raw_input('Type the key in ' + str(2 * block) + ' hexadecimal digits: ')
    key = binascii.unhexlify(key_hex)

    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), default_backend())
    ctx = cipher.decryptor()
    padded_plaintext = ctx.update(ciphertext) + ctx.finalize()

    ctx = padding.PKCS7(8 * block).unpadder()
    plaintext = ctx.update(padded_plaintext) + ctx.finalize()

    with open(filename + '.dec', 'wb') as f:
        f.write(plaintext)
    print('Decrypted file: ' + filename + '.dec')


def hash_encrypt_then_mac():
    # Cipher block size, expressed in bytes.
    block = algorithms.AES.block_size / 8

    # Read the plaintext file.
    filename = raw_input('Type the file to encrypt-then-MAC: ')
    with open(filename, 'rb') as f:
        plaintext = f.read()

    # Read the keys in hexadecimal digits from keyboard.
    key_hex = raw_input('Type the encryption key in ' + str(2 * block) + ' hexadecimal digits: ')
    cryptkey = binascii.unhexlify(key_hex)
    key_hex = raw_input('Type the authentication key in ' + str(2 * block) + ' hexadecimal digits: ')
    authkey = binascii.unhexlify(key_hex)

    # Pad the plaintext to make it multiple of the block size.
    ctx = padding.PKCS7(8 * block).padder()
    padded_plaintext = ctx.update(plaintext) + ctx.finalize()

    # Encrypt the plaintext with a random IV.
    iv = os.urandom(block)
    cipher = Cipher(algorithms.AES(cryptkey), modes.CBC(iv), default_backend())
    ctx = cipher.encryptor()
    ciphertext = ctx.update(padded_plaintext) + ctx.finalize()

    # Authenticate the ciphertext and the IV.
    ctx = hmac.HMAC(authkey, hashes.SHA256(), default_backend())
    ctx.update(iv)
    ctx.update(ciphertext)
    digest = ctx.finalize()

    # Write the MAC, the IV, and the ciphertext in the output file.
    with open(filename + '.enc', 'wb') as f:
        f.write(digest)
        f.write(iv)
        f.write(ciphertext)
    print('Encrypt-then-MACed file: ' + filename + '.enc')


def hash_verify_then_decrypt():
    # Cipher block size, expressed in bytes.
    block = algorithms.AES.block_size / 8

    # Read the MAC, the IV, and the ciphertext from a file.
    filename = raw_input('Type the file to verify-then-decrypt: ')
    with open(filename, 'rb') as f:
        digest_from_file = f.read(hashes.SHA256.digest_size)
        iv = f.read(block)
        ciphertext = f.read()
    if len(ciphertext) % block != 0:
        sys.exit('The ciphertext must be multiple of ' + str(block) + ' bytes.')

    # Read the keys in hexadecimal digits from keyboard.
    key_hex = raw_input('Type the encryption key in ' + str(2 * block) + ' hexadecimal digits: ')
    cryptkey = binascii.unhexlify(key_hex)
    key_hex = raw_input('Type the authentication key in ' + str(2 * block) + ' hexadecimal digits: ')
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
    ctx = padding.PKCS7(8 * block).unpadder()
    plaintext = ctx.update(padded_plaintext) + ctx.finalize()

    # Write the decrypted text in the output file.
    with open(filename + '.dec', 'wb') as f:
        f.write(plaintext)
    print('Verified-then-decrypted file: ' + filename + '.dec')


def sign_rsa():
    # Read the private key.
    filename = raw_input('Type the PEM file containing the RSA private key: ')
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
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )

    # Write the signature in the output file.
    with open(filename + '.sgn', 'wb') as f:
        f.write(signature)
    print('Signature file: ' + filename + '.sgn')


def verify_rsa():
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


def sign_rsa_cert():
    # Read the private key.
    filename = raw_input('Type the PEM file containing the RSA private key: ')
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
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )

    # Write the signature in the output file.
    with open(filename + '.sgn', 'wb') as f:
        f.write(signature)
    print('Signature file: ' + filename + '.sgn')


def verify_rsa_cert():
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


if __name__ == '__main__':
    print 'a'

