import time
import tkinter as tk

from app import App
from util.dataVault import DataVault
from pages.librarian.staffActions import logger
from util.queryCollection import QueryCollection
from util.stateUtil import LoginManager
from util.twoFAUtil import TwoFactor


class TwoFALogin(tk.Frame):
    def __init__(self, parent, controller):
        self.placeholder_color = None
        t = time.time()
        self.log = None
        self.logoutbtn = None
        self.app = App()
        logger.info("Opening LibrarianHome...")
        tk.Frame.__init__(self, parent)
        self.otpval = tk.StringVar()
        DataVault.pageMap["TwoFALogin"] = self
        # TODO: add input validation
        self.formlabel = tk.Label(self, text="Please Enter the OTP sent to your mobile", font=controller.title_font)
        self.formlabel.grid(sticky='ew', columnspan=10)
        self.otp = tk.StringVar()
        self.no = tk.Entry(self, textvariable=self.otp)
        self.no.grid(sticky='ew', columnspan=2)
        self.btn = tk.Button(self, text="Verify", command=lambda:self.goToSearchHome(controller))
        self.btn.grid(sticky='ew', columnspan=2)
        self.resend = tk.Button(self, text="Resend", command=lambda: TwoFactor.send_code(TwoFactor, self, controller))
        self.resend.grid(sticky='ew', columnspan=2)
        self.errorlabel = None

    def goToSearchHome(self, controller):
        if TwoFactor.authenticate(TwoFactor, self.no.get()):
            # make 2FA enabled in db
            self.resend.grid_forget()
            self.btn.grid_forget()
            self.formlabel['text'] = "Verification Successful!"
            self.no.grid_forget()
            self.back = tk.Button(self, text='Proceed', command=lambda: controller.show_frame(DataVault.twofa_back))
            self.back.grid(sticky='ew', columnspan=5)
            time.sleep(1.7)
            controller.show_frame("SearchHome")
        else:
            self.formlabel['text'] = "Incorrect OTP, try again"

    def serviceOutage(self, controller):
        DataVault.pageMap['StaffActions'].label['text'] = "TwoFA service is down, account created without TwoFA!"
        time.sleep(2)
        controller.show_frame("SearchHome")



class TwoFACreate(tk.Frame):
    def __init__(self, parent, controller):
        self.placeholder_color = None
        t = time.time()
        self.app = App()
        logger.info("Opening LibrarianHome...")
        tk.Frame.__init__(self, parent)
        self.otpval = tk.StringVar()
        self.log = None
        self.logoutbtn = None
        DataVault.pageMap["TwoFACreate"] = self
        # TODO: add input validation
        self.formlabel = tk.Label(self, text="Would you like to set up Two-Factor Authentication?", font=controller.title_font)
        self.formlabel.grid(sticky='ew', columnspan=10)
        self.yes = tk.Button(self, text="Yes", command=lambda: self.verifyOTP(controller))
        self.yes.grid(sticky='nsew', columnspan=5)
        self.no = tk.Button(self, text="No", command=lambda: self.noLoader(controller))
        self.no.grid(sticky='nsew', columnspan=5)

    def noLoader(self, controller):
        DataVault.pageMap['StaffActions'].formlabel['text'] = "Account Created without 2FA"
        DataVault.pageMap['CreateMember'].createForm()
        LoginManager.loginManager(LoginManager, DataVault.pageMap, 'Librarian', DataVault.createdStaffId, "StaffActions", controller)
        controller.show_frame(DataVault.twofa_origin)
    def verifyOTP(self, controller):
        self.yes.grid_forget()
        self.no.grid_forget()
        TwoFactor.send_code(TwoFactor, self, controller)
        self.formlabel['text'] = "Enter your OTP"
        self.otpentry = tk.Entry(self, textvariable=self.otpval)
        self.otpentry.grid(columnspan=5)
        self.verifybtn = tk.Button(self, text='Verify', command=lambda:self.accountCreated2FA(controller))
        self.verifybtn.grid(columnspan=5)
        self.resend = tk.Button(self, text="Resend", command=lambda: TwoFactor.send_code(TwoFactor, self, controller))
        self.resend.grid(columnspan=5)
        self.grid_columnconfigure((0, 4), weight=1)

    def accountCreated2FA(self, controller):
        if TwoFactor.authenticate(TwoFactor, self.otpentry.get()):
            # make 2FA enabled in db
            QueryCollection.update2FABool(TwoFactor, DataVault.twoFAid, DataVault.twoFAtype)
            self.verifybtn.grid_forget()
            self.otpentry.grid_forget()
            self.resend.grid_forget()
            self.formlabel['text'] = "2FA Set up! Hit back to do other things"
            self.back = tk.Button(self, text='Back', command=lambda: self.returnToActions(controller))
            self.back.grid(sticky='ns', columnspan=5)
        else:
            self.formlabel['text'] = "Incorrect OTP"

    def returnToActions(self, controller):
        LoginManager.loginManager(LoginManager, DataVault.pageMap, "Librarian", DataVault.twoFAid, "StaffActions", controller)
        controller.show_frame('StaffActions')

    def serviceOutage(self, controller):
        DataVault.pageMap['StaffActions'].label['text'] = "TwoFA service is down, account created without TwoFA!"
        time.sleep(2)
        LoginManager.loginManager(LoginManager, DataVault.pageMap, "Librarian", DataVault.twoFAid, "StaffActions", controller)
        controller.show_frame("StaffActions")