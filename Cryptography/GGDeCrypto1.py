from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
import binascii
import sys

block = algorithms.AES.block_size/8

# filename = raw_input('Input file name to decrypt: ')
filename = 'giacomo.txt.enc'
with open(filename, 'rb') as f:
    iv = f.read(block)
    ciphertext = f.read()
    if len(ciphertext) % block != 0:
        sys.exit('Error! file content is not multiple of ' + str(block) + 'bytes.')

# key_hex = raw_input('Plese enter + ' str(2*block) ' + hex digits: ')
key_hex = '70bf1fb7756bdcf8e6a77d606807b44c'
key = binascii.unhexlify(key_hex)
if len(key_hex) % block != 0:
    print ('Error, key is not 16byte!')
    exit()

cipher = Cipher(algorithms.AES(key), modes.CBC(iv), default_backend())
ctx = cipher.decryptor()
padded_plaintext = ctx.update(ciphertext) + ctx.finalize()

ctx = padding.PKCS7(8*block).unpadder()
plaintext = ctx.update(padded_plaintext) + ctx.finalize()

with open(filename + '.dec', 'wb') as f:
    f.write(plaintext)
print 'Decrypted file: ' + filename + '.dec'
