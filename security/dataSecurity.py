import pyaes, pbkdf2, binascii, os, secrets

import security.dumps
import logging
logger = logging.getLogger()


class AESPasswEncryption:
    def keygen(self):
        # Derive a 256-bit AES encryption key from the password
        password = "s3cr3t*c0d3"
        passwordSalt = os.urandom(16)
        key = pbkdf2.PBKDF2(password, passwordSalt).read(32)
        with open('security/keys/secret.txt', 'wb') as f:
            f.write(key)
        print('AES encryption key:', binascii.hexlify(key))
        return key

    def encrypt(self):
        # Encrypt the plaintext with the given key:
        #   ciphertext = AES-256-CTR-Encrypt(plaintext, key, iv)
        f = open('security/keys/secret.txt', 'rb')
        key = f.read()
        f.close()
        iv = secrets.randbits(256)
        with open('security/keys/ivector.txt', 'w') as f:
            f.write(str(iv))
        plaintext = 'ilsinstance@123'
        aes = pyaes.AESModeOfOperationCTR(key, pyaes.Counter(iv))
        ciphertext = aes.encrypt(plaintext)
        with open('security/encryption.txt', 'wb') as f:
            f.write(ciphertext)
        print('Encrypted:', binascii.hexlify(ciphertext))

    def decrypt(self):
        f = open("security/keys/secret.txt", 'rb')
        key = f.read()
        f.close()
        f = open('security/keys/ivector.txt', 'r')
        iv = int(f.read())
        f.close()
        with open('security/encryption.txt', 'rb') as f:
            ciphertext = f.read()
        #   plaintext = AES-256-CTR-Decrypt(ciphertext, key, iv)
            aes = pyaes.AESModeOfOperationCTR(key, pyaes.Counter(iv))
            decrypted = aes.decrypt(ciphertext)
            return decrypted

# AESPasswEncryption.keygen(AESPasswEncryption)
# AESPasswEncryption.encrypt(AESPasswEncryption)