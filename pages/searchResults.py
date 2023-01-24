import sys
import time
import tkinter as tk
import traceback

from app import App
from kinterUtilities import KinterUtilities
from pages.memberVerification import MemberVerification
from pages.searchBooks import SearchBooks
import logging

logger = logging.getLogger()

class SearchResults(tk.Frame):
    def __init__(self, parent, controller):
        t = time.time()
        self.tkutil = KinterUtilities(parent)
        self.app = App()
        logger.info("Opening SearchResults...")
        tk.Frame.__init__(self, parent)
        self.controller = controller
        logger.info("SearchResults ready. Took " + str(time.time() - t) + " seconds")
        filters = SearchBooks.inputvalues
        self.view = tk.Button(self, text="Results", command=lambda: self.populateResults(filters))
        self.view.grid(ipady=5, ipadx=10)


    def populateResults(self, filters):
        self.view.grid_forget()
        document = self.app.Member(MemberVerification.mem_id, self.app).searchDocument(SearchBooks.inputvalues, "Books")
        logger.info("Results: " + str(document) + " for string filters: " + str(filters))
        cells={}
        for i in range(len(document)):  # Rows
            borrow = tk.Button(self, text="Borrow", command= lambda: self.checkBorrows(document[i], self.controller))
            retbook = tk.Button(self, text="Return")
            for j in range(1, len(document[1])):  # Columns
                try:
                    b = tk.Entry(self,justify=tk.CENTER)
                    b.grid(row=i, column=j)
                    b.insert(tk.END, str(document[i][j]))
                    cells[(i, j)] = b
                except Exception as e:
                    logger.error("Error in populateTable: " + str(e) + traceback.format_exc())
                    sys.exit(-1)
            if i!=0:
                borrow.grid(row=i, column=j+1)
                retbook.grid(row=i, column=j+2)

    def checkBorrows(self, data, controller):
        borrowable = self.app.Member(MemberVerification.mem_id, self.app).borrowDocument("Books", data[0], data[1], data)
        if borrowable == 0:
            label = tk.Label(self, text="There are no copies left to borrow \n Please wait till it is returned", font=controller.title_font)
            label.pack(side="bottom", fill="x", pady=10, padx=10)

        # else:
