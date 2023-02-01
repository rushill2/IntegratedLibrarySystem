import time
import tkinter as tk

import app
from app import App
import logging

logger = logging.getLogger()


class LibrarianHome(tk.Frame):

    def __init__(self, parent, controller):
        t = time.time()
        self.app = App()
        logger.info("Opening LibrarianHome...")
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Login or Create Account", font=controller.title_font)
        label.pack(side="top", fill="x", pady=20, padx=20)

        login = tk.Button(self, text="Login",
                           command=lambda: controller.show_frame("LoginLibrarian"))
        login.pack(pady=5, padx=10)
        create = tk.Button(self, text="Create",
                           command=lambda: controller.show_frame("CreateLibrarian"))
        create.pack(pady=5, padx=10)
        button = tk.Button(self, text="Home",
                           command=lambda: controller.show_frame("StartPage"))
        button.pack(pady=5, padx=10)
        logger.info("LibrarianHome ready. Took " + str(time.time() - t) + " seconds")

class LoginLibrarian(tk.Frame):
    mem_id = None
    def __init__(self, parent, controller):
        t = time.time()
        logger.info("Opening LibrarianHome...")
        tk.Frame.__init__(self, parent)
        self.app = app.App()
        self.app.populate()
        self.controller = controller

        # description text
        self.label = tk.Label(self, text="Enter your Librarian ID", font=controller.title_font)
        self.label.pack(side="top", fill="x", pady=20, padx=20)

        # buttons
        home = tk.Button(self, text="Home",
                         command=lambda: controller.show_frame("StartPage"))
        # get value from entry when pressed
        lib_id = tk.StringVar()
        submit = tk.Button(self, text="Submit",
                           command=lambda: self.login(controller, lib_id), textvariable=lib_id)
        member_id = tk.StringVar()

        # textbox
        self.id_entry = tk.Entry(self, textvariable=member_id, font=('calibre', 10, 'normal'))

        # displaying everything
        self.id_entry.pack()
        submit.pack(pady=5, padx=10)
        home.pack(pady=5, padx=10)
        logger.info("LoginLibrarian ready. Took " + str(time.time() - t) + " seconds")

    def login(self, controller, lib_id):
        # SQL will be : SELECT * FROM Librarian.Staff WHERE id = lib_id
        # if rowcount is 0, then say it's a bad login
        # else if 1, good login, next page, view members or books (and for each member can view issues)

        pass


class CreateLibrarian(tk.Frame):
    def __init__(self, parent, controller):
        t = time.time()
        logger.info("Opening LibrarianHome...")
        tk.Frame.__init__(self, parent)
        self.app = app.App()
        self.app.populate()
        self.controller = controller

        # description text
        self.label = tk.Label(self, text="Enter your Librarian ID", font=controller.title_font)
        self.label.pack(side="top", fill="x", pady=20, padx=20)

        # buttons
        home = tk.Button(self, text="Home",
                         command=lambda: controller.show_frame("StartPage"))
        # get value from entry when pressed
        submit = tk.Button(self, text="Submit",
                           command=lambda: self.createLibrarian(controller))
        member_id = tk.StringVar()

        # textbox
        self.id_entry = tk.Entry(self, textvariable=member_id, font=('calibre', 10, 'normal'))

        # displaying everything
        self.id_entry.pack()
        submit.pack(pady=5, padx=10)
        home.pack(pady=5, padx=10)
        logger.info("LoginLibrarian ready. Took " + str(time.time() - t) + " seconds")