import sys
import time
import tkinter as tk
import traceback

from app import App
from pages.member.booksBorrowed import BookBorrows
from util import memberSQL
from util.kinterUtilities import KinterUtilities
from pages.member.memberVerification import MemberVerification
from pages.member.searchBooks import SearchBooks
import logging
from data.dataVault import DataVault
from util.memberSQL import Member

logger = logging.getLogger()

class SearchResults(tk.Frame):

    def __init__(self, parent, controller):
        t = time.time()
        DataVault.searchRes = self
        self.tkutil = KinterUtilities(parent)
        self.app = App()
        logger.info("Opening SearchResults...")
        tk.Frame.__init__(self, parent)
        self.controller = controller
        logger.info("SearchResults ready. Took " + str(time.time() - t) + " seconds")
        filters = DataVault.inputvalues
        self.labelvar = tk.StringVar()
        self.label = tk.Label(self, font=controller.title_font, textvariable=self.labelvar)
        self.member = memberSQL.Member(DataVault.mem_id, self.app)



    # TODO: figure how to get reference to specific button clicked for erasure and borrowing
    def checkBorrows(self, data, controller, row):

        borrowable = self.member.borrowDocument("Books", data[0], data[1], data, DataVault.mem_id)
        if borrowable == 0:
            self.labelvar.set('No copies left.')
            self.label.grid(sticky=tk.N)

        elif borrowable == 1:
            self.labelvar.set('Book already borrowed!')
            self.label.grid(sticky=tk.NE)

        elif borrowable == 2:
            self.labelvar.set('Cannot borrow more than 5 books')
            self.label.grid(sticky=tk.NE)

        elif borrowable == 3:
            self.labelvar.set('No books borrowed to return!')
            self.label.grid(sticky=tk.NE)

        else:
            DataVault.issues = Member(DataVault.mem_id, self.app).getIssuesbyMemId(DataVault.mem_id)
            DataVault.populateIssues(DataVault, controller)
            DataVault.borrowbuttons[row - 1]['state'] = 'disabled'
            DataVault.bookborrows_msg.set("Book borrowed! \n" + DataVault.bookborrows_msg.get())
            DataVault.bookborrows_prev = "SearchResults"
            controller.show_frame("BookBorrows")



