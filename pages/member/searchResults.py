import time
import tkinter as tk

from app import App
from util import memberSQL
import logging
from util.dataVault import DataVault
from util.memberSQL import Member
from util.precomputeTables import PrecomputeTables

logger = logging.getLogger()

class SearchResults(tk.Frame):

    def __init__(self, parent, controller):
        t = time.time()
        DataVault.searchRes = self
        self.app = App()
        self.view = None
        DataVault.pageMap["SearchResults"] = self
        logger.info("Opening SearchResults...")
        self.log = None
        self.logoutbtn = None
        tk.Frame.__init__(self, parent)
        self.controller = controller
        logger.info("SearchResults ready. Took " + str(time.time() - t) + " seconds")
        filters = DataVault.inputvalues
        self.labelvar = tk.StringVar()
        self.label = tk.Label(self, font=controller.title_font, textvariable=self.labelvar)
        self.member = memberSQL.Member(DataVault.mem_id, self.app)



    # TODO: figure how to get reference to specific button clicked for erasure and borrowing
    def checkBorrows(self, data, controller, row):
        DataVault.bookborrows_prev = "SearchHome"
        borrowable = self.member.borrowDocument("Books", data[0], data[1], data, DataVault.mem_id)
        if borrowable == 0:
            self.labelvar.set('No copies left.')
            DataVault.borrowbuttons[row-1]['state'] = 'disabled'
            self.label.grid(sticky=tk.N)

        elif borrowable == 1:
            self.labelvar.set('Book already borrowed!')
            DataVault.borrowbuttons[row-1]['state'] = 'disabled'
            self.label.grid(sticky=tk.NE)

        elif borrowable == 2:
            self.labelvar.set('Cannot borrow more than 5 books')
            for i in range(len(DataVault.borrowbuttons)):
                DataVault.borrowbuttons[i-1]['state'] = 'disabled'
            self.label.grid(sticky=tk.NE)

        elif borrowable == 3:
            self.labelvar.set('No books borrowed to return!')
            self.label.grid(sticky=tk.NE)

        else:
            DataVault.issues = Member(DataVault.mem_id, self.app).getIssuesbyMemId(DataVault.mem_id)
            PrecomputeTables.populateIssues(PrecomputeTables,controller)
            DataVault.borrowbuttons[row - 1]['state'] = 'disabled'
            DataVault.bookborrows_msg.set("Book borrowed! \n" + DataVault.bookborrows_msg.get())
            DataVault.bookborrows_prev = "SearchResults"
            DataVault.borrowbuttons[row - 1]['state'] = 'disabled'
            controller.show_frame("BookBorrows")



