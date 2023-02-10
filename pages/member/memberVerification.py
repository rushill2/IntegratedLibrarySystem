import hashlib
import time
import tkinter as tk

import logging
from data.dataVault import DataVault
logger = logging.getLogger()
import app


class MemberVerification(tk.Frame):
    clickCnt = 0
    def __init__(self, parent, controller):
        t = time.time()
        logger.info("Opening LibrarianHome...")
        tk.Frame.__init__(self, parent)
        self.app = app.App()
        self.app.populate()
        self.controller = controller

        # description text
        self.label = tk.Label(self, text="Enter your Member ID", font=controller.title_font)
        self.label.grid(row=1, column=2)
        self.idlabel = tk.Label(self, text="Phone/Email", font=controller.title_font)
        self.passlabel = tk.Label(self, text="Password", font=controller.title_font)
        # buttons
        home = tk.Button(self, text="Home",
                         command=lambda: controller.show_frame("StartPage"))
        # get value from entry when pressed
        submit = tk.Button(self, text="Submit",
                           command=lambda: self.get_member_id(controller))
        member_id = tk.StringVar()
        passvar = tk.StringVar()
        # textbox
        self.id_entry = tk.Entry(self, textvariable=member_id, font=('calibre', 10, 'normal'))

        # displaying everything
        self.id_entry.grid(row=2, column=3)
        self.idlabel.grid(row=2, column=2)
        self.pass_entry = tk.Entry(self, textvariable=passvar, font=('calibre', 10, 'normal'), show="*")
        showpass = tk.Button(self, text="Show Password",
                             command=lambda: self.password_visible(self.pass_entry, showpass))
        showpass.grid(row=3, column=4, ipadx=10)
        # displaying everything
        self.pass_entry.grid(row=3, column=3)
        self.passlabel.grid(row=3, column=2)
        submit.grid(row=6, column=0)
        home.grid(row=6, column=5)
        logger.info("MemberVerification ready. Took " + str(time.time() - t) + " seconds")

        #  value getter for member id that validates with db

    def get_member_id(self, controller):
        entry = self.id_entry.get()
        passw = self.pass_entry.get()
        if all(s.isdigit() for s in entry):
            login_type = "Phone"
        else:
            login_type = "Email"

        # now compute password hash
        hash = hashlib.md5(passw.encode("utf-8")).hexdigest()
        values = (login_type, str(entry), str(hash))
        logger.info("Validating Member ID: " + entry + '...')
        memid, valid = self.app.validateLogin(values)
        if valid:
            logger.info("Validation Successful! Welcome member " + str(memid))
            # setMember(entry)
            DataVault.mem_id = memid
            controller.show_frame('SearchHome')
        else:
            logger.error("Validation Failed. Try again.")
            self.label['text'] = "Validation Failed.Try again."

    def password_visible(self, passw, showpass):
        MemberVerification.clickCnt += 1

        if MemberVerification.clickCnt % 2 == 0:
            showpass.config(text='Show Password')
            passw.config(show="*")
        else:
            showpass.config(text='Hide Password')
            passw.config(show="")
