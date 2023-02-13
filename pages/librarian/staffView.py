import hashlib
import sys
import time
import tkinter as tk
import traceback
import datetime
import data.dumps as d
import app
import util.smtpUtil
from util.queryCollection import QueryCollection
from util.twoFAUtil import TwoFactor
from app import App, Librarian
from config import smtpConfig
from data.dataVault import DataVault
import logging
from util.smtpUtil import SMTPUtil

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
        dims = self.grid_size()
        DataVault.pageMap["StaffView"] = self

        self.label = tk.Label(self, text="Welcome! \n Pick your action", font=controller.title_font)
        self.log = None
        self.books = tk.Button(self, text="View Documents", command=lambda: self.goToSearch(controller))
        self.view_mem = tk.Button(self, text="View Members", command=lambda: self.preloadMembers(controller))
        self.create_mem = tk.Button(self, text="Create Member", command=lambda: self.preloadCreate(controller))
        self.button = tk.Button(self, text="Home", command=lambda: controller.show_frame("StartPage"))
        DataVault.bookborrows_prev = "SearchHome"
        self.label.grid(sticky="ew", columnspan=10)
        self.books.grid(row=2, columnspan=5, pady=5)
        self.view_mem.grid(row=4, columnspan=5, pady=5)
        self.create_mem.grid(row=6, columnspan=5, pady=5)
        self.button.grid(row=8, columnspan=5, pady=5)
        self.grid_columnconfigure((0, 4), weight=1)

        logger.info("SearchHome ready. Took " + str(time.time() - t) + " seconds")

    def goToSearch(self, controller):
        DataVault.bookborrows_prev = "StaffView"
        controller.show_frame("SearchBooks")

    def preloadMembers(self, controller):
        rows = self.staff.viewMembers()
        DataVault.viewMemberList = rows
        DataVault.populateMembers(DataVault, controller)
        controller.show_frame("ViewMembers")

    def preloadCreate(self, controller):
        DataVault.loggedIn(DataVault, "Librarian", DataVault.loggedinID, "CreateMember")
        controller.show_frame("CreateMember")


class ViewMembers(tk.Frame):
    def __init__(self, parent, controller):
        t = time.time()
        DataVault.viewMems = self
        self.app = App()
        self.member = Member(DataVault.mem_id, self.app)
        logger.info("Opening SearchHome...")
        tk.Frame.__init__(self, parent)
        self.staff = Librarian()
        DataVault.pageMap["ViewMembers"] = self

        self.controller = controller

        self.back = tk.Button(self, text="Back", command=lambda: controller.show_frame('StaffView'))
        self.back.grid(row=2, column=8)

    # TODO: Preload the overdues and issues for members
    def preloadIssues(self, controller, row):
        # display member information
        try:
            DataVault.currMem = DataVault.viewMemberList[row]
            issues = self.member.getIssuesbyMemId(DataVault.currMem[0])
            # display title, date of issue, due date and option to notify via email
            # TODO: Change all populate data from DataVault variables to fn params
            DataVault.issues = issues
            for i in range(len(issues)):
                today = datetime.date.today()
                if today < issues[i][4]:
                    issues[i] += ("Overdue",)
                else:
                    issues[i] += ("On Time",)

            issues += (("Issue Id", "Document Id", "Title", "Issue Date", "Due Date","Memid", "Status"),)
            issues.reverse()
            DataVault.loggedIn(DataVault, "Librarian", DataVault.loggedinID, "MemberDetails")
            DataVault.populateDetails(DataVault, controller, issues)
            controller.show_frame("MemberDetails")
        except Exception as e:
            logger.error("Error in preloadIssues: " + str(e) + traceback.format_exc())


    def modifyMembers(self, controller, row):
        pass

    def deleteMember(self, controller, row):
        memid = DataVault.viewMemberList[row][0]
        Member.deleteMember(Member, memid)
        DataVault.viewMemberList = self.staff.viewMembers()
        DataVault.populateMembers(DataVault, controller)
        pass


class MemberDetails(tk.Frame):
    def __init__(self, parent, controller):
        self.placeholder_color = None
        t = time.time()
        self.app = App()
        logger.info("Opening LibrarianHome...")
        tk.Frame.__init__(self, parent)
        DataVault.memDetails = self
        DataVault.pageMap["MemberDetails"] = self
        # TODO: add input validation
        self.formlabel = tk.Label(self, text="", font=controller.title_font)
        self.formlabel.grid(row=0, column=3)
        self.back = tk.Button(self, text="Back", command=lambda: controller.show_frame('ViewMembers'))
        self.back.grid(row=0, column=8)

    def sendEmail(self, row, controller, i):


        # Open a plain text file for reading.  For this example, assume that
        # the text file contains only ASCII characters.
        # Create a text/plain message
        duedelta = row[4] - datetime.date.today()
        if duedelta > datetime.timedelta(0):
            # due in x days
            ptext = smtpConfig.templates['reminder'].replace('{_title}', row[2]).replace("{_days}", str(duedelta))
        elif duedelta < datetime.timedelta(0):
            ptext = smtpConfig.templates['overdue'].replace('{_title}', row[2]).replace("{_days}", str(duedelta))
        else:
            ptext = smtpConfig.templates['today'].replace('{_title}', row[2])

        try:
            SMTPUtil.sendEmailSSL(SMTPUtil, ptext, 'Regarding Your Recent ILS Book Issue', DataVault.currMem[7])
            self.formlabel['text'] = "Email Sent!"
        except Exception as e:
            logger.error("Error in MemberDetails sendEmail: " +str(e) +traceback.format_exc())
            sys.exit(-1)



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
        self.lastname = tk.StringVar()
        self.email = tk.StringVar()
        self.phone = tk.StringVar()
        self.password = tk.StringVar()
        self.retype_pass = tk.StringVar()
        self.twoFA = tk.IntVar()
        self.otpval = tk.IntVar()

        formlabel = tk.Label(self, text="Enter your details: ", font=controller.title_font)
        formlabel.grid(row=0, column=3)
        self.loginForm()
        submit = tk.Button(self, text="Submit",
                           command=lambda: self.validateStaffAccount(formlabel, controller))
        back = tk.Button(self, text="Back",
                           command=lambda: controller.show_frame("StaffView"))
        submit.grid(sticky=tk.E)
        back.grid(sticky=tk.E)

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
            formatted_dob = datetime.datetime.strptime(dob, "%Y-%m-%d")
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
            self.loginForm()
            TwoFactor.Phone = phone
            DataVault.twofa_back = "StaffView"
            DataVault.twofa_origin = "CreateMember"
            controller.show_frame("TwoFA")

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


class TwoFACreate(tk.Frame):
    def __init__(self, parent, controller):
        self.placeholder_color = None
        t = time.time()
        self.app = App()
        logger.info("Opening LibrarianHome...")
        tk.Frame.__init__(self, parent)
        DataVault.memDetails = self
        self.otpval = tk.IntVar()
        DataVault.pageMap["TwoFACreate"] = self
        # TODO: add input validation
        self.formlabel = tk.Label(self, text="Would you like to set up Two-Factor Authentication?", font=controller.title_font)
        self.formlabel.grid(sticky='ew', columnspan=10)
        self.yes = tk.Button(self, text="Yes", command=lambda: self.verifyOTP(controller))
        self.yes.grid(sticky='ew', columnspan=2)
        self.no = tk.Button(self, text="No", command=lambda: self.noLoader(controller))
        self.no.grid(sticky='ew', columnspan=2)
    def noLoader(self, controller):
        self.formlabel['text'] = "Account Created without 2FA"
        controller.show_frame(DataVault.twofa_origin)
    def verifyOTP(self, controller):
        self.yes.grid_forget()
        self.no.grid_forget()
        TwoFactor.send_code(TwoFactor)
        self.formlabel['text'] = "Enter your OTP"
        self.otpentry = tk.Entry(self, textvariable=self.otpval)
        self.otpentry.grid(sticky='ew', columnspan=5)
        self.verifybtn = tk.Button(self, text='Verify', command=lambda:self.accountCreated2FA(controller))
        self.verifybtn.grid(sticky='ew', columnspan=5)

    def accountCreated2FA(self, controller):
        if TwoFactor.authenticate(TwoFactor, self.otpentry.get()):
            # make 2FA enabled in db
            QueryCollection.update2FABool(TwoFactor,TwoFactor.id, "Member")
            self.verifybtn.grid_forget()
            self.otpentry.grid_forget()
            self.back = tk.Button(self, text='Back', command=lambda: controller.show_frame(DataVault.twofa_back))
            self.back.grid(sticky='ew', columnspan=5)
        else:
            self.formlabel['text'] = "Incorrect OTP"


    # TwoFactor.send_code(TwoFactor, phone)
    # otp = tk.Label(self, text="Enter Mobile OTP")
    # val = tk.Entry(self, textvariable=self.otpval)
    # auth = tk.Button(self, text="Verify", command=lambda: TwoFactor.authenticate(TwoFactor, self.otpval.get()))
    # otp.grid(row=5, column=5)
    # val.grid(row=5, column=6)
    # auth.grid(row=6, column=5)


class TwoFALogin(tk.Frame):
    def __init__(self, parent, controller):
        self.placeholder_color = None
        t = time.time()
        self.app = App()
        logger.info("Opening LibrarianHome...")
        tk.Frame.__init__(self, parent)
        DataVault.memDetails = self
        self.otpval = tk.IntVar()
        DataVault.pageMap["TwoFALogin"] = self
        # TODO: add input validation
        self.formlabel = tk.Label(self, text="Please Enter the OTP sent to your mobile", font=controller.title_font)
        self.formlabel.grid(sticky='ew', columnspan=10)
        self.otp = tk.IntVar()
        self.no = tk.Entry(self, textvariable=self.otp)
        self.no.grid(sticky='ew', columnspan=2)
        self.btn = tk.Button(self, text="Verify", command=lambda:self.goToSearchHome(controller))
        self.btn.grid(sticky='ew', columnspan=2)
        self.resend = tk.Button(self, text="Resend", command=lambda: TwoFactor.send_code(TwoFactor))
        self.resend.grid(sticky='ew', columnspan=2)

    def goToSearchHome(self, controller):
        if TwoFactor.authenticate(TwoFactor, self.no.get()):
            # make 2FA enabled in db
            self.resend.grid_forget()
            self.btn.grid_forget()
            self.formlabel['text'] = "Verification Successful!"
            self.no.grid_forget()
            self.back = tk.Button(self, text='Proceed', command=lambda: controller.show_frame(DataVault.twofa_back))
            self.back.grid(sticky='ew', columnspan=5)
        else:
            self.formlabel['text'] = "Incorrect OTP, try again"
