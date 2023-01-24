import time
import tkinter as tk

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
        label = tk.Label(self, text="View Members or Look for Document", font=controller.title_font)
        label.pack(side="top", fill="x", pady=20, padx=20)
        button = tk.Button(self, text="Home",
                           command=lambda: controller.show_frame("StartPage"))
        button.pack(pady=20, padx=10)
        logger.info("LibrarianHome ready. Took " + str(time.time() - t) + " seconds")
