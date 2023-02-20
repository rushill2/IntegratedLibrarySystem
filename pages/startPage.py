import time
import tkinter as tk

from app import App
import logging

from util.dataVault import DataVault

logger = logging.getLogger()


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        app = App()
        app.populate()
        logger.info("DB connection successful!")
        t = time.time()
        DataVault.pageMap["StartPage"] = self
        logger.info("Opening StartPage...")
        self.log = None
        self.logoutbtn = None
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.label = tk.Label(self, text="Are you a member or librarian?", font=controller.title_font)
        self.label.pack(side="top", fill="x", pady=20, padx=20)

        button1 = tk.Button(self, text="Member",
                            command=lambda: self.pregridMemHome(controller))
        button2 = tk.Button(self, text="Librarian",
                            command=lambda: self.pregridLibHome(controller))
        button1.pack(pady=0, padx=10)
        button2.pack(pady=10, padx=10)
        logger.info("StartPage ready. Took " + str(time.time() - t) + " seconds")

    def pregridLibHome(self, controller):
        page = DataVault.pageMap['LibrarianHome']
        dims = page.grid_size()

        controller.show_frame("LibrarianHome")

    def pregridMemHome(self, controller):
        DataVault.pageMap['MemberVerification'].memberlogin(controller)
        controller.show_frame("MemberVerification")

