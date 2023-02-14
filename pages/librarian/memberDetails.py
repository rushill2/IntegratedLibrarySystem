import datetime
import sys
import time
import tkinter as tk
import traceback

from app import App
from config import smtpConfig
from data.dataVault import DataVault
from pages.librarian.staffActions import logger
from util.smtpUtil import SMTPUtil


class MemberDetails(tk.Frame):
    def __init__(self, parent, controller):
        self.placeholder_color = None
        t = time.time()
        self.app = App()
        self.log = None
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
