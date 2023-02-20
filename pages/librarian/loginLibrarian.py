import hashlib
import time
import tkinter as tk

import app
from util.dataVault import DataVault
import logging

from util.stateUtil import LoginManager
from util.twoFAUtil import TwoFactor

logger = logging.getLogger()

class LoginLibrarian(tk.Frame):
    mem_id = None
    clickCnt = 0

    def __init__(self, parent, controller):
        t = time.time()
        logger.info("Opening LibrarianHome...")
        tk.Frame.__init__(self, parent)
        self.app = app.App()
        self.app.populate()
        DataVault.pageMap["LoginLibrarian"] = self
        self.logoutbtn = None
        self.controller = controller
        self.label = tk.Label(self, text="Enter your details:", font=controller.title_font)
        self.label.grid(row = 0, column = 3)
        # description text
        # buttons
        home = tk.Button(self, text="Home",
                         command=lambda: controller.show_frame("StartPage"))
        # get value from entry when pressed
        a = tk.Label(self, text="Email/Phone")
        a.grid(row=2, column=2)
        b = tk.Label(self, text="Password")
        b.grid(row=3, column=2)
        passw_var = tk.StringVar()
        submit = tk.Button(self, text="Submit",
                           command=lambda: self.login(controller, lib_id, passw_var))
        lib_id = tk.StringVar()
        self.id_entry = tk.Entry(self, textvariable=lib_id, font=('calibre', 10, 'normal'))

        # displaying everything
        self.id_entry.grid(row=2, column=3)

        self.passw = tk.Entry(self, textvariable=passw_var, font=('calibre', 10, 'normal'), show='*')
        showpass = tk.Button(self, text="Show Password",
                           command=lambda: self.password_visible(self.passw, showpass))
        # displaying everything
        self.passw.grid(row=3, column=3)
        submit.grid(row=4, column=2)
        showpass.grid(row=3, column=4, ipadx=5)
        home.grid(row=4, column=3)
        self.grid_columnconfigure((0, 4), weight=1)
        logger.info("LoginLibrarian ready. Took " + str(time.time() - t) + " seconds")

    def login(self, controller, lib_id, passw):
        # SQL will be : SELECT * FROM Librarian.Staff WHERE id = lib_id
        # if rowcount is 0, then say it's a bad login
        # else if 1, good login, next page, view members or books (and for each member can view issues)

        # first check if email or phone
        if all(s.isdigit() for s in lib_id.get()):
            login_type = "Phone"
        else:
            login_type = "Email"

        # now compute password hash
        hash = hashlib.sha256(passw.get().encode("utf-8")).hexdigest()
        values = (login_type, str(lib_id.get()), str(hash))
        auth_enabled, valid, id = app.Librarian().validateLogin(values)
        DataVault.loggedinID = id
        if valid:
            DataVault.globallog = True
            # successful login, transition to other page
            # next page should have options for view members (and modify once you're in the view) - same with documents
            LoginManager.loginManager(LoginManager, DataVault.pageMap, "Librarian", id, "StaffActions", controller)
            DataVault.loggedinID = id
            DataVault.type = "Librarian"
            if auth_enabled == 1:
                DataVault.twofa_origin = "LoginLibrarian"
                DataVault.twofa_back = "StaffActions"
                TwoFactor.send_code(TwoFactor)
                controller.show_frame('TwoFALogin')
            else:
                controller.show_frame("StaffActions")
        else:
            # failed login, get fucked
            logger.error("Validation Staff login Failed. Try again.")
            self.label['text'] = "Invalid login, try again"

    def password_visible(self, passw, showpass):
        LoginLibrarian.clickCnt += 1

        if LoginLibrarian.clickCnt % 2 == 0:
            showpass.config(text='Show Password')
            passw.config(show="*")
        else:
            showpass.config(text='Hide Password')
            passw.config(show="")
