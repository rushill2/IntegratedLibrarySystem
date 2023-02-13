import time
import tkinter as tk

import app
import logging

from data.dataVault import DataVault
from pages.member.booksBorrowed import BookBorrows
from util.memberSQL import Member

logger = logging.getLogger()


class SearchHome(tk.Frame):
    def __init__(self, parent, controller):
        t = time.time()
        self.app = app.App()
        logger.info("Opening SearchHome...")
        tk.Frame.__init__(self, parent)
        self.controller = controller
        DataVault.pageMap["SearchHome"] = self
        self.log = None
        label = tk.Label(self, text="Welcome! \n Pick the type of document", font=controller.title_font)
        dims = self.grid_size()
        label.grid(columnspan=10, sticky='ew')
        books = tk.Button(self, text="Books", command=lambda: controller.show_frame("SearchBooks"))
        books.grid(columnspan=5)
        journals = tk.Button(self, text="Journals", command=lambda: controller.show_frame("StartPage"))
        journals.grid(columnspan=5)
        mags = tk.Button(self, text="Magazines", command=lambda: controller.show_frame("StartPage"))
        mags.grid(columnspan=5)
        button = tk.Button(self, text="Home", command=lambda: controller.show_frame("StartPage"))
        button.grid(columnspan=5)
        DataVault.bookborrows_prev = "SearchHome"
        issuebtn = tk.Button(self, text="View Issues", command=lambda: self.preloadIssues(controller))
        issuebtn.grid(columnspan=5)
        self.grid_columnconfigure((0, 4), weight=1)
        logger.info("SearchHome ready. Took " + str(time.time() - t) + " seconds")

    def preloadIssues(self, controller):
        DataVault.issues = Member(DataVault.mem_id, self.app).getIssuesbyMemId(DataVault.mem_id)
        DataVault.populateIssues(DataVault, controller)
        DataVault.loggedIn(DataVault, "Member", DataVault.mem_id, "SearchBooks")
        controller.show_frame("BookBorrows")
