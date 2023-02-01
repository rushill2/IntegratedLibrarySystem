import sys
import time
import tkinter as tk
import traceback

from app import App
from pages.member.memberVerification import MemberVerification
from pages.member.searchBooks import SearchBooks
from pages.member.searchResults import logger
from util.kinterUtilities import KinterUtilities


class BookBorrows(tk.Frame):
    def __init__(self, parent, controller):
        t = time.time()
        self.tkutil = KinterUtilities(parent)
        self.app = App()
        logger.info("Opening SearchResults...")
        tk.Frame.__init__(self, parent)
        self.controller = controller
        logger.info("BookBorrows ready. Took " + str(time.time() - t) + " seconds")
        filters = SearchBooks.inputvalues
        label = tk.Label(self, text="Book Borrowed Succesfully! \n Here are your borrows: ",
                         font=controller.title_font)
        label.grid(ipady=10, ipadx=10)

        self.button = tk.Button(self, text='View Issues', command=lambda:self.populateIssues(controller))
        self.view = tk.Button(self, text="Back", command=lambda: controller.show_frame("SearchResults"))
        self.view.grid(ipady=5, ipadx=10)
        self.button.grid()


    def populateIssues(self, controller):
        issues = self.app.Member(MemberVerification.mem_id, self.app).getIssuesbyMemId(MemberVerification.mem_id)
        cells = {}
        issues.append(("Num1", "Num2", "Title", "Date Issued", "Date Due"))
        issues.reverse()
        if len(issues)==0:
            pass

        for i in range(len(issues)):
            for j in range(2, len(issues[0])):
                try:
                    b = tk.Entry(self,justify=tk.CENTER)
                    b.grid(row=i, column=j)
                    b.insert(tk.END, str(issues[i][j]))
                    cells[(i, j)] = b
                except Exception as e:
                    logger.error("Error in populateTable: " + str(e) + traceback.format_exc())
                    sys.exit(-1)