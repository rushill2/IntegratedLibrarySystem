import time
import tkinter as tk

from app import App
import logging

from data.dataVault import DataVault

logger = logging.getLogger()


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        app = App()
        app.populate()
        logger.info("DB connection successful!")
        t = time.time()
        logger.info("Opening StartPage...")
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Are you a member or librarian?", font=controller.title_font)
        label.pack(side="top", fill="x", pady=20, padx=20)

        button1 = tk.Button(self, text="Member",
                            command=lambda: controller.show_frame("MemberVerification"))
        button2 = tk.Button(self, text="Librarian",
                            command=lambda: self.pregridLibHome(controller))
        button1.pack(pady=0, padx=10)
        button2.pack(pady=10, padx=10)
        logger.info("StartPage ready. Took " + str(time.time() - t) + " seconds")

    def pregridLibHome(self, controller):
        page = DataVault.pageMap['LibrarianHome']
        dims = page.grid_size()

        controller.show_frame("LibrarianHome")


