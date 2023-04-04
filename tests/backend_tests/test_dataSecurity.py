import unittest
import os
import shutil
import binascii
from security.AESPasswEncryption import AESPasswEncryption


class TestAESPasswEncryption(unittest.TestCase):
    def setUp(self):
        if not os.path.exists('security/keys'):
            os.makedirs('security/keys')
        if not os.path.exists('security/test'):
            os.makedirs('security/test')

    def test_keygen(self):
        a = AESPasswEncryption()
        key = a.keygen()
        self.assertEqual(len(key), 32)
        self.assertTrue(os.path.exists('security/keys/secret.txt'))
        with open('security/keys/secret.txt', 'rb') as f:
            self.assertEqual(key, f.read())

    def test_encrypt_decrypt(self):
        a = AESPasswEncryption()
        key = a.keygen()
        a.encrypt()
        self.assertTrue(os.path.exists('security/keys/ivector.txt'))
        self.assertTrue(os.path.exists('security/encryption.txt'))
        decrypted = a.decrypt()
        self.assertEqual(decrypted, b'ilsinstance@123')

    def tearDown(self):
        if os.path.exists('security/keys'):
            shutil.rmtree('security/keys')
        if os.path.exists('security/test'):
            shutil.rmtree('security/test')


if __name__ == '__main__':
    unittest.main()