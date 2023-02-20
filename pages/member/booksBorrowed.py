import time
import tkinter as tk

from app import App
from util.dataVault import DataVault
import logging
from util.memberSQL import Member
from util.precomputeTables import PrecomputeTables

logger = logging.getLogger()


class BookBorrows(tk.Frame):

    def __init__(self, parent, controller):
        DataVault.bookborrows_msg = tk.StringVar()
        DataVault.bookborrows_msg.set("Here are your borrows:")
        t = time.time()
        DataVault.BBorrows = self
        self.app = App()
        logger.info("Opening SearchResults...")
        tk.Frame.__init__(self, parent)
        DataVault.pageMap["BookBorrows"] = self
        self.controller = controller
        logger.info("BookBorrows ready. Took " + str(time.time() - t) + " seconds")
        filters = DataVault.inputvalues
        self.label = tk.Label(self, textvariable=DataVault.bookborrows_msg, font=controller.title_font)
        self.label.grid(ipady=10, ipadx=10)
        self.member = Member(DataVault.mem_id, self.app)
        self.view = tk.Button(self, text="Back", command=lambda: controller.show_frame(DataVault.bookborrows_prev))
        self.view.grid(ipady=5, ipadx=10)
        self.controller = controller

    def returnBook(self, data, controller, row):
        DataVault.bookborrows_msg.set("Document returned!")
        # DataVault.borrowbuttons[row]['state'] = 'active'
        doc_id = data[1]
        self.member.returnDocument("Books", doc_id, row)
        DataVault.issues = Member(DataVault.mem_id, self.app).getIssuesbyMemId(DataVault.mem_id)
        PrecomputeTables.populateIssues(PrecomputeTables,controller)