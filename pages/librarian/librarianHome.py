import time
import tkinter as tk

from app import App
import logging
from util.dataVault import DataVault
from util.stateUtil import LoginManager

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
        self.logoutbtn = None
        self.login = tk.Button(self, text="Login",
                          command=lambda: self.preloadLogin(controller))

        self.create = tk.Button(self, text="Create",
                           command=lambda: self.preloadLibCreate(controller))

        self.button = tk.Button(self, text="Home",
                           command=lambda: self.preloadHome(controller))
        self.label.grid(sticky='ew', columnspan=10)
        self.login.grid(row=2, columnspan=5, pady=5)
        self.create.grid(row=3, columnspan=5, pady=5)
        self.button.grid(row=4, columnspan=5, pady=5)

        self.grid_columnconfigure((0, 4), weight=1)

        logger.info("LibrarianHome ready. Took " + str(time.time() - t) + " seconds")

    def preloadLibCreate(self, controller):
        LoginManager.loginManager(LoginManager,DataVault.pageMap, "Librarian", DataVault.loggedinID, "CreateLibrarian",controller)
        DataVault.pageMap['CreateLibrarian'].loginForm()
        controller.show_frame("CreateLibrarian")

    def preloadLogin(self, controller):
        page = DataVault.pageMap['LoginLibrarian']
        page.id_entry.delete(0, tk.END)
        page.passw.delete(0, tk.END)
        page.label['text'] = "Enter your details:"
        controller.show_frame("LoginLibrarian")
    def preloadHome(self, controller):
        DataVault.pageMap['StartPage'].label['text'] = "Are you a member or librarian?"
        controller.show_frame("StartPage")




