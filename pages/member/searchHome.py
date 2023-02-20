import time
import tkinter as tk

import app
import logging

from data.dataVault import DataVault
from pages.member.booksBorrowed import BookBorrows
from util.memberSQL import Member
from util.precomputeTables import PrecomputeTables
from util.stateUtil import LoginManager

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
        self.logoutbtn = None
        label = tk.Label(self, text="Welcome! \n Pick the type of document", font=controller.title_font)
        label.grid(columnspan=10, sticky='ew')
        books = tk.Button(self, text="Books", command=lambda: self.preloadSearch(controller))
        books.grid(columnspan=5)
        DataVault.bookborrows_prev = "SearchHome"
        issuebtn = tk.Button(self, text="View Issues", command=lambda: self.preloadIssues(controller))
        issuebtn.grid(columnspan=5)
        self.grid_columnconfigure((0, 4), weight=1)
        logger.info("SearchHome ready. Took " + str(time.time() - t) + " seconds")

    def preloadIssues(self, controller):
        DataVault.issues = Member(DataVault.mem_id, self.app).getIssuesbyMemId(DataVault.mem_id)
        if len(DataVault.issues) > 0:
            DataVault.pageMap['BookBorrows'].label['text'] = "Here are your borrows:"
        else:
            DataVault.pageMap['BookBorrows'].label['text'] = "Nothing issued yet!"

        PrecomputeTables.populateIssues(PrecomputeTables,controller)
        LoginManager.loginManager(LoginManager,DataVault.pageMap, "Member", DataVault.mem_id, "SearchBooks", controller)
        controller.show_frame("BookBorrows")

    def preloadSearch(self, controller):
        page = DataVault.pageMap['SearchBooks']
        LoginManager.loginManager(LoginManager,DataVault.pageMap, DataVault.type, DataVault.loggedinID, "SearchBooks",controller)
        page.inputvalues = {}
        page.label['text'] = "Set filters and search:"
        controller.show_frame("SearchBooks")
