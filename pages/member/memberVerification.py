import time
import tkinter as tk

import logging
from data.dataVault import DataVault
logger = logging.getLogger()
import app


class MemberVerification(tk.Frame):
    def __init__(self, parent, controller):
        t = time.time()
        logger.info("Opening LibrarianHome...")
        tk.Frame.__init__(self, parent)
        self.app = app.App()
        self.app.populate()
        self.controller = controller

        # description text
        self.label = tk.Label(self, text="Enter your Member ID", font=controller.title_font)
        self.label.pack(side="top", fill="x", pady=20, padx=20)

        # buttons
        home = tk.Button(self, text="Home",
                         command=lambda: controller.show_frame("StartPage"))
        # get value from entry when pressed
        submit = tk.Button(self, text="Submit",
                           command=lambda: self.get_member_id(controller))
        member_id = tk.StringVar()

        # textbox
        self.id_entry = tk.Entry(self, textvariable=member_id, font=('calibre', 10, 'normal'))

        # displaying everything
        self.id_entry.pack()
        submit.pack(pady=5, padx=10)
        home.pack(pady=5, padx=10)
        logger.info("MemberVerification ready. Took " + str(time.time() - t) + " seconds")

        #  value getter for member id that validates with db

    def get_member_id(self, controller):
        entry = self.id_entry.get()
        logger.info("Validating Member ID: " + entry + '...')
        if self.app.validateLogin(entry):
            logger.info("Validation Successful! Welcome member " + entry)
            # setMember(entry)
            DataVault.mem_id = entry
            controller.show_frame('SearchHome')
        else:
            logger.error("Validation Failed. Try again.")
            self.label['text'] = "Validation Failed.Try again."
