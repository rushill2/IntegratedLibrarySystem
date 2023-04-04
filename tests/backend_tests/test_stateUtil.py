import unittest
import tkinter as tk
from unittest.mock import MagicMock
from util.dataVault import DataVault
from util.stateUtil import LoginManager

class TestLoginManager(unittest.TestCase):

    def setUp(self):
        self.pageMap = {
            "page1": tk.Frame(),
            "page2": tk.Frame()
        }
        self.controller = MagicMock()

    def test_loginManager_not_logged_in(self):
        loginManager = LoginManager()
        loginManager.loginManager(self.pageMap, None, None, "page1", self.controller)
        self.assertEqual(self.pageMap["page1"].log["text"], "Not Logged in yet")
        self.assertEqual(self.pageMap["page1"].log["fg"], "gray")
        self.assertIsNone(self.pageMap["page1"].logoutbtn)

    def test_loginManager_logged_in(self):
        loginManager = LoginManager()
        DataVault.loggedinID = 123
        loginManager.loginManager(self.pageMap, "member", 123, "page1", self.controller)
        self.assertEqual(self.pageMap["page1"].log["text"], "Logged in as member: 123")
        self.assertEqual(self.pageMap["page1"].log["fg"], "gray")
        self.assertIsNotNone(self.pageMap["page1"].logoutbtn)
        self.assertEqual(self.pageMap["page1"].logoutbtn["text"], "Logout")

    def test_logout(self):
        loginManager = LoginManager()
        self.pageMap["StartPage"] = MagicMock()
        self.pageMap["StartPage"].label = MagicMock()
        loginManager.logout(self.controller, self.pageMap["page1"])
        self.assertIsNone(DataVault.loggedinID)
        self.assertIsNone(DataVault.type)
        self.assertIsNone(DataVault.globallog)
        self.assertIsNone(self.pageMap["page1"].log)
        self.assertIsNone(self.pageMap["page1"].logoutbtn)
        self.pageMap["StartPage"].label.__setitem__.assert_called_once_with('text', 'You have been logged out \n Are you a member or librarian?')
        self.controller.show_frame.assert_called_once_with("StartPage")

if __name__ == '__main__':
    unittest.main()