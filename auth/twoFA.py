import time
import tkinter as tk

from app import App
from data.dataVault import DataVault
from pages.librarian.staffActions import logger
from util.queryCollection import QueryCollection
from util.twoFAUtil import TwoFactor


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
        self.resend = tk.Button(self, text="Resend", command=lambda: TwoFactor.send_code(TwoFactor))
        self.resend.grid(sticky='ew', columnspan=2)

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
