import time
import tkinter as tk

from app import App
import logging
from data.dataVault import DataVault

logger = logging.getLogger()


class LibrarianHome(tk.Frame):

    def __init__(self, parent, controller):
        t = time.time()
        self.app = App()
        logger.info("Opening LibrarianHome...")
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.label = tk.Label(self, text="Login or Create Account", font=controller.title_font)

        DataVault.pageMap["LibrarianHome"] = self
        self.log = None
        self.login = tk.Button(self, text="Login",
                          command=lambda: controller.show_frame("LoginLibrarian"))

        self.create = tk.Button(self, text="Create",
                           command=lambda: self.preloadLibCreate(controller))

        self.button = tk.Button(self, text="Home",
                           command=lambda: controller.show_frame("StartPage"))
        self.label.grid(sticky='ew', columnspan=10)
        self.button.grid(row=2, columnspan=5, pady=5)
        self.create.grid(row=3, columnspan=5, pady=5)
        self.login.grid(row=4, columnspan=5, pady=5)
        self.grid_columnconfigure((0, 4), weight=1)

        logger.info("LibrarianHome ready. Took " + str(time.time() - t) + " seconds")

    def preloadLibCreate(self, controller):
        DataVault.loggedIn(DataVault, "Librarian", DataVault.loggedinID, "CreateLibrarian")
        controller.show_frame("CreateLibrarian")





