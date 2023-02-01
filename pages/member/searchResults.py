import sys
import time
import tkinter as tk
import traceback

from app import App
from util.kinterUtilities import KinterUtilities
from pages.member.memberVerification import MemberVerification
from pages.member.searchBooks import SearchBooks
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
        self.view = tk.Button(self, text="Results", command=lambda: self.populateResults(filters, controller))
        self.view.grid(ipady=5, ipadx=10)
        self.labelvar = tk.StringVar()
        self.label = tk.Label(self, font=controller.title_font, textvariable=self.labelvar)
        self.borrowbuttons = []
        self.member = self.app.Member(MemberVerification.mem_id, self.app)

    def populateResults(self, filters, controller):
        self.view.grid_forget()
        self.view = tk.Button(self, text="Back", command=lambda: controller.show_frame("SearchBooks"))
        self.view.grid(ipady=5, ipadx=10)
        document = self.app.Member(MemberVerification.mem_id, self.app).searchDocument(SearchBooks.inputvalues, "Books")
        logger.info("Results: " + str(document) + " for string filters: " + str(filters))
        cells={}
        for i in range(len(document)):  # Rows
            self.borrow = tk.Button(self, text="Borrow", command= lambda i=i: self.checkBorrows(document[i], self.controller, i))
            self.retbook = tk.Button(self, text="Return", command= lambda i=i: self.returnBook(document[i], self.controller, i))
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
                self.borrow.grid(row=i, column=j+1)
                self.borrowbuttons.append(self.borrow)
                self.retbook.grid(row=i, column=j+2)

    # TODO: figure how to get reference to specific button clicked for erasure and borrowing
    def checkBorrows(self, data, controller, row):
        self.borrowbuttons[row-1].grid_forget()
        borrowable = self.member.borrowDocument("Books", data[0], data[1], data, MemberVerification.mem_id)
        if borrowable == 0:
            self.labelvar.set('No copies left.')
            self.label.grid(sticky=tk.N)

        elif borrowable == 1:
            self.labelvar.set('Book already borrowed!')
            self.label.grid(sticky=tk.NE)
            self.borrow.grid_forget()

        else:
            controller.show_frame("BookBorrows")


    def returnBook(self, data, controller, row):
        doc_id = data[0]
        book_id = data[1]
        self.member.returnDocument("Books", )
