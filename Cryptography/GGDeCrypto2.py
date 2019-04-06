from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, hmac
from cryptography.hazmat.primitives import padding
import binascii
import sys

block = algorithms.AES.block_size/8
digest_size = hashes.SHA256.digest_size

# filename = raw_input('Input file name to decrypt: ')
filename = 'giacomo.txt.enc'
with open(filename, 'rb') as f:
    digest_from_file = f.read(hashes.SHA256.digest_size)
    iv = f.read(block)
    ciphertext = f.read()
    if len(ciphertext) % block != 0:
        sys.exit('Error! file content is not multiple of ' + str(2*block) + '.')

# k1 = raw_input('Please enter ' + str(2*block) + ' byte key1 (CryptKey): ')
k1 = 'e3ed4634f770a37fa2ba0a871fa13f44'
cryptkey = binascii.unhexlify(k1)
# k2 = raw_input('Please enter ' + str(2*block) + ' byte key2 (AuthKey): ')
k2 = '268e06f952e4a1233443722f8342a9f2'
authkey = binascii.unhexlify(k2)

if len(cryptkey) % block != 0:
    sys.exit('Error, key is not 16byte!')
if len(authkey) % block != 0:
    sys.exit('Error, key is not 16byte!')

ctx = hmac.HMAC(authkey, hashes.SHA256(), default_backend())
ctx.update(iv)
ctx.update(ciphertext)
ctx.verify(digest_from_file)

ctx = Cipher(algorithms.AES(cryptkey), modes.CBC(iv), default_backend()).decryptor()
padded_plaintext = ctx.update(ciphertext) + ctx.finalize()

ctx = padding.PKCS7(8*block).unpadder()
plaintext = ctx.update(padded_plaintext) + ctx.finalize()

with open(filename + '.dec', 'wb') as f:
    f.write(plaintext)
print('Decrypted file: ' + filename + '.dec')
