import unittest
import tkinter as tk
from unittest.mock import patch
from tkinter import messagebox
from pages.librarian.createMember import CreateMember

class TestCreateMember(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()
        self.app = CreateMember(self.root, None)

    def test_validate_staff_account(self):
        # Test valid input
        self.app.firstname.set("John")
        self.app.lastname.set("Doe")
        self.app.email.set("johndoe@example.com")
        self.app.phone.set("1234567890")
        self.app.password.set("password123")
        self.app.retype_pass.set("password123")
        self.app.dob.set("1990-01-01")
        self.app.validateStaffAccount(self.app.formlabel, None)
        self.assertEqual(self.app.formlabel['text'], "Account Created! ")

        # Test invalid input
        self.app.firstname.set("")
        self.app.lastname.set("")
        self.app.email.set("invalidemail")
        self.app.phone.set("1234")
        self.app.password.set("password123")
        self.app.retype_pass.set("password456")
        self.app.dob.set("01-01-1990")
        with patch.object(messagebox, 'showerror') as mock_showerror:
            self.app.validateStaffAccount(self.app.formlabel, None)
            mock_showerror.assert_called_with("Error", "Invalid input! Please check your details and try again.")

    def tearDown(self):
        self.root.destroy()

if __name__ == '__main__':
    unittest.main()