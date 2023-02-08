import hashlib
import time
import tkinter as tk
import traceback
from datetime import datetime
import data.dumps as d

import app
from app import App, Librarian
from data.dataVault import DataVault
import logging

from util.memberSQL import Member

logger = logging.getLogger()

class StaffView(tk.Frame):
    def __init__(self, parent, controller):
        t = time.time()
        self.app = App()
        logger.info("Opening SearchHome...")
        tk.Frame.__init__(self, parent)
        self.staff = Librarian()
        self.controller = controller
        label = tk.Label(self, text="Welcome! \n Pick your action", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10, padx=10)
        books = tk.Button(self, text="View Documents", command=lambda: self.goToSearch(controller))
        books.pack(pady=1, padx=10)
        view_mem = tk.Button(self, text="View Members", command=lambda: self.preloadMembers(controller))
        view_mem.pack(pady=1, padx=10)
        create_mem = tk.Button(self, text="Create Member", command=lambda: self.controller.show_frame("CreateMember"))
        create_mem.pack(pady=1, padx=10)
        button = tk.Button(self, text="Home", command=lambda: controller.show_frame("StartPage"))
        button.pack(pady=10, padx=10, side=tk.LEFT)
        DataVault.bookborrows_prev = "SearchHome"
        logger.info("SearchHome ready. Took " + str(time.time() - t) + " seconds")

    def goToSearch(self, controller):
        DataVault.bookborrows_prev = "StaffView"
        controller.show_frame("SearchBooks")

    def preloadMembers(self, controller):
        rows = self.staff.viewMembers()
        DataVault.viewMemberList = rows
        DataVault.populateMembers(DataVault, controller, rows)
        controller.show_frame("ViewMembers")


class ViewMembers(tk.Frame):
    def __init__(self, parent, controller):
        t = time.time()
        DataVault.viewMems = self
        self.app = App()
        self.member = Member(DataVault.mem_id, self.app)
        logger.info("Opening SearchHome...")
        tk.Frame.__init__(self, parent)
        self.staff = Librarian()
        self.controller = controller
        self.back = tk.Button(self, text="Back", command=lambda: controller.show_frame('StaffView'))
        self.back.grid(row=0, column=8)

    # TODO: Preload the overdues and issues for members
    def preloadIssues(self, controller, row):
        issues = self.member.getIssuesbyMemId(DataVault.viewMemberList[row][0])
        pass

    def modifyMembers(self, controller):
        pass

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
        self.lastname = tk.StringVar()
        self.email = tk.StringVar()
        self.phone = tk.StringVar()
        self.password = tk.StringVar()
        self.retype_pass = tk.StringVar()
        formlabel = tk.Label(self, text="Enter your details: ", font=controller.title_font)
        formlabel.grid(row=0, column=3)
        self.loginForm()
        submit = tk.Button(self, text="Submit",
                           command=lambda: self.validateStaffAccount(formlabel, controller))
        submit.grid(sticky=tk.E)

    def validateStaffAccount(self, formlabel, controller):
        # 3 components: check names for numbers, check email ID for @ and .com
        # Check contact number for alpha-special
        # check password for special and nums, need both + length > 8 and store hash
        # TODO: Add support for .edu and other emails
        dobbool = False
        passbool = False
        namebool = False
        emailbool = False
        phonebool = False
        password = self.password.get()
        retype_pass = self.retype_pass.get()
        phone = self.phone.get()
        email = self.email.get()
        dob = self.dob.get()
        first = self.firstname.get()
        last = self.lastname.get()

        # first, password

        # check 1 , are they equal
        if password == retype_pass:
            if any(s in d.specials for s in password) and any(s.isalnum() for s in password):
                passbool = True
                hash = hashlib.md5(password.encode("utf-8")).hexdigest()
            else:
                formlabel['text'] = "Passwords must be alphanumeric and contain special chatracters"
        else:
            formlabel['text'] = "Passwords do not match"

        # check name
        if first.isalpha() and last.isalpha():
            namebool = True
        else:
            formlabel['text'] = "Names must only contain alphabets"

        # check email, must contain @ and .com, and length > 5
        if any(s == "@" for s in email) and ".com" in email and len(email) > 5:
            emailbool = True
        else:
            formlabel['text'] = "Not a valid email"

        # check contact num - all nums and length = 10
        if phone.isnumeric():
            if len(phone) == 10:
                phonebool = True
            else:
                formlabel['text'] = "Invalid phone number length"
        else:
            formlabel['text'] = "Only numbers allowed in Contact"

        # validate dob
        # credit : https://stackoverflow.com/questions/16870663/how-do-i-validate-a-date-string-format-in-python

        try:
            formatted_dob = datetime.strptime(dob, "%Y-%m-%d")
            if dob == formatted_dob.strftime('%Y-%m-%d'):
                dobbool = True
            else:
                formlabel['text'] = "Date must be in YYYY-MM-DD form"
        except ValueError as e:
            formlabel['text'] = "Date must be in YYYY-MM-DD form"
            logger.error("Error in dob input validation: " + str(e) + traceback.format_exc())

        if phonebool and emailbool and namebool and passbool and dobbool:
            data = [None, first, last, dob, phone, email, hash]
            app.Librarian().createMemberAccount(data)
            formlabel['text'] = "Account Created! "

    def loginForm(self):
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