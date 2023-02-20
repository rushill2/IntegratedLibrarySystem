import time
import tkinter as tk
from util.inputValidation import Validation

import app
from app import App
from util.dataVault import DataVault
from pages.librarian.staffActions import logger
from util.twoFAUtil import TwoFactor


class CreateMember(tk.Frame):
    clickcnt = 0
    # TODO: add passwords and confirm password fields after input validation
    def __init__(self, parent, controller):
        self.placeholder_color = None
        t = time.time()
        self.app = App()
        logger.info("Opening LibrarianHome...")
        tk.Frame.__init__(self, parent)
        # TODO: add input validation
        self.firstname = tk.StringVar()
        self.dob = tk.StringVar()
        DataVault.pageMap["CreateMember"] = self
        self.log = None
        self.logoutbtn = None
        self.lastname = tk.StringVar()
        self.email = tk.StringVar()
        self.phone = tk.StringVar()
        self.password = tk.StringVar()
        self.retype_pass = tk.StringVar()
        self.twoFA = tk.StringVar()
        self.otpval = tk.StringVar()

        formlabel = tk.Label(self, text="Enter your details: ", font=controller.title_font)
        formlabel.grid(row=0, column=3)
        self.createForm()
        submit = tk.Button(self, text="Submit",
                           command=lambda: self.validateStaffAccount(formlabel, controller))
        back = tk.Button(self, text="Back",
                           command=lambda: controller.show_frame("StaffActions"))
        submit.grid(sticky=tk.E)
        back.grid(sticky=tk.E)

    def validateStaffAccount(self, formlabel, controller):
        password = self.password.get()
        retype_pass = self.retype_pass.get()
        phone = self.phone.get()
        email = self.email.get()
        dob = self.dob.get()
        first = self.firstname.get()
        last = self.lastname.get()

        valid_input, hash = Validation.inputValidation(Validation, formlabel, password=password, email=email, phone=phone, retype_pass=retype_pass, dob=dob, first=first, last=last)
        if valid_input:
            data = [None, first, last, dob, phone, email, hash]
            app.Librarian().createMemberAccount(data)
            formlabel['text'] = "Account Created! "
            self.createForm()
            TwoFactor.Phone = phone
            DataVault.twofa_back = "StaffActions"
            DataVault.twofa_origin = "CreateMember"
            controller.show_frame("TwoFACreate")

    def createForm(self):
        a = tk.Label(self, text="First Name")
        a.grid(row=1, column=2)
        b = tk.Label(self, text="Last Name")
        b.grid(row=2, column=2)
        c = tk.Label(self, text="Email Id")
        c.grid(row=3, column=2)
        d = tk.Label(self, text="Contact Number")
        d.grid(row=4, column=2)
        g = tk.Label(self, text="Date of Birth")
        g.grid(row=5, column=2)
        e = tk.Label(self, text="Password")
        e.grid(row=6, column=2)
        e = tk.Label(self, text="Confirm Password")
        e.grid(row=7, column=2)
        # e.grid(row=8, column=2)
        a1 = tk.Entry(self, textvariable=self.firstname)
        a1.grid(row=1, column=3)
        b1 = tk.Entry(self, textvariable=self.lastname)
        b1.grid(row=2, column=3)
        c1 = tk.Entry(self, textvariable=self.email)
        c1.grid(row=3, column=3)
        d1 = tk.Entry(self, textvariable=self.phone)
        d1.grid(row=4, column=3)
        self.e1 = tk.Entry(self, textvariable=self.dob)
        self.placeholder = "YYYY-MM-DD"
        try:
            self.e1.delete('0', 'end')
        except Exception as e:
            logger.error("CreateLibrarian loginForm: No text in e1 to delete")
        self.e1.bind('<FocusIn>', self.foc_in)
        self.e1.bind('<FocusOut>', self.foc_out)
        self.placeholder_color = 'grey'
        self.default_fg_color = self.e1['fg']
        self.foc_in()
        self.foc_out()
        self.e1.grid(row=5, column=3)
        f1 = tk.Entry(self, textvariable=self.password, show="*")
        f1.grid(row=6, column=3)
        g1 = tk.Entry(self, textvariable=self.retype_pass, show="*")
        g1.grid(row=7, column=3)
        showpass = tk.Button(self, text="Show Password",
                             command=lambda: self.password_visible(f1, g1, showpass))
        showpass.grid(row=6, column=4, ipadx = 10)

    def password_visible(self, passw, retype, showpass):
        CreateMember.clickcnt += 1

        if CreateMember.clickcnt % 2 == 0:
            showpass.config(text='Show Password')
            passw.config(show="*")
            retype.config(show="*")
        else:
            showpass.config(text='Hide Password')
            passw.config(show="")
            retype.config(show="")

    def erase(self, e1):
        e1.delete(0, 'end')

    def add(self, e1):
        e1.insert(0, 'YYYY-MM-DD')

    def put_placeholder(self):
        self.e1.insert(0, self.placeholder)
        self.e1['fg'] = self.placeholder_color

    def foc_in(self, *args):
        if self.e1['fg'] == self.placeholder_color:
            self.e1.delete('0', 'end')
            self.e1['fg'] = self.default_fg_color

    def foc_out(self, *args):
        if not self.e1.get():
            self.put_placeholder()
