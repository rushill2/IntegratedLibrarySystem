import time
import tkinter as tk

import app
import logging
logger = logging.getLogger()


class SearchHome(tk.Frame):
    def __init__(self, parent, controller):
        t = time.time()
        self.app = app.App()
        logger.info("Opening SearchHome...")
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Welcome! \n Pick the type of document", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10, padx=10)
        books = tk.Button(self, text="Books", command=lambda: controller.show_frame("SearchBooks"))
        books.pack(pady=1, padx=10)
        journals = tk.Button(self, text="Journals", command=lambda: controller.show_frame("StartPage"))
        journals.pack(pady=1, padx=10)
        mags = tk.Button(self, text="Magazines", command=lambda: controller.show_frame("StartPage"))
        mags.pack(pady=1, padx=10)
        button = tk.Button(self, text="Home", command=lambda: controller.show_frame("StartPage"))
        button.pack(pady=10, padx=10)
        logger.info("SearchHome ready. Took " + str(time.time() - t) + " seconds")
