import unittest
from unittest.mock import patch
from validation import Validation

class TestValidation(unittest.TestCase):

    def setUp(self):
        self.validation = Validation()

    def test_nameValidation(self):
        self.assertTrue(self.validation.nameValidation("John", "Doe", {}))
        self.assertFalse(self.validation.nameValidation("123", "Doe", {}))
        self.assertFalse(self.validation.nameValidation("John", "456", {}))
        self.assertFalse(self.validation.nameValidation("John", "", {}))
        self.assertFalse(self.validation.nameValidation("", "Doe", {}))
        self.assertTrue(self.validation.nameValidation("", "", {}))

    def test_emailValidation(self):
        with patch('util.queryCollection.QueryCollection.checkEmailExists', return_value=False):
            self.assertTrue(self.validation.emailValidation("johndoe@example.com", {}))
        with patch('util.queryCollection.QueryCollection.checkEmailExists', return_value=True):
            self.assertFalse(self.validation.emailValidation("johndoe@example.com", {}))
        self.assertFalse(self.validation.emailValidation("johndoe", {}))
        self.assertFalse(self.validation.emailValidation("johndoe@example", {}))
        self.assertFalse(self.validation.emailValidation("johndoe.com", {}))
        self.assertFalse(self.validation.emailValidation("", {}))
        self.assertTrue(self.validation.emailValidation(None, {}))

    def test_phoneValidation(self):
        self.assertTrue(self.validation.phoneValidation("1234567890", {}))
        self.assertFalse(self.validation.phoneValidation("123-456-7890", {}))
        self.assertFalse(self.validation.phoneValidation("abc1234567", {}))
        self.assertFalse(self.validation.phoneValidation("123456789", {}))
        self.assertFalse(self.validation.phoneValidation("", {}))
        self.assertTrue(self.validation.phoneValidation(None, {}))

    def test_dobValidation(self):
        self.assertTrue(self.validation.dobValidation("1990-01-01", {}))
        self.assertFalse(self.validation.dobValidation("01/01/1990", {}))
        self.assertFalse(self.validation.dobValidation("1990-13-01", {}))
        self.assertFalse(self.validation.dobValidation("", {}))
        self.assertTrue(self.validation.dobValidation(None, {}))

    def test_passValidation(self):
        self.assertTrue(self.validation.passValidation("password123", "password123", {})[0])
        self.assertFalse(self.validation.passValidation("password", "password", {})[0])
        self.assertFalse(self.validation.passValidation("password", "password1", {})[0])
        self.assertFalse(self.validation.passValidation("password", "password", {})[0])
        self.assertFalse(self.validation.passValidation("", "", {})[0])
        self.assertTrue(self.validation.passValidation(None, None, {})[0])

    def test_inputValidation(self):
        with patch('util.queryCollection.QueryCollection.checkEmailExists', return_value=False):
            valid_input = self.validation.inputValidation({}, "password123", "John", "Doe", "johndoe@example.com", "1234567890", "password123", "1990-01-01")
            self.assertTrue(valid_input[0])
            self.assertEqual(valid_input[1], self.validation.passValidation("password123", "password123", {})[1])

        invalid_input = self.validation.inputValidation({}, "password", "John", "Doe", "johndoe@example.com", "1234567890", "password", "1990-01-01")
        self.assertFalse(invalid_input[0])
        self.assertEqual(invalid_input[1], None)

if __name__ == '__main__':
    unittest.main()