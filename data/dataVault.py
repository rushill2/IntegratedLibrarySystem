import sys
import traceback
import logging
logger = logging.getLogger()
import tkinter as tk


class DataVault:
    mem_id = None
    member = None
    borrowbuttons = []
    bookborrows_msg = None
    bookborrows_prev = "SearchResults"
    lib_login = False
    issues = []
    borrowarr = []
    returnarr = []
    retbook = None
    BBorrows = None
    searchBooks = None
    inputvalues = {}
    searchRes = None
    viewMems = None
    viewMemberList = []


    def populateIssues(self, controller):
        if DataVault.issues is None:
            DataVault.bookborrows_msg.set("No Issues yet!")
            return

        cells = {}
        DataVault.issues.append(("Num1", "Num2", "Title", "Date Issued", "Date Due"))
        DataVault.issues.reverse()

        for i in range(len(DataVault.borrowarr)):
            if i < len(DataVault.returnarr):
                DataVault.returnarr[i].grid_forget()
                DataVault.borrowarr[i].grid_forget()

        for i in range(len(DataVault.issues)):
            if i > 0:
                DataVault.retbook = tk.Button(DataVault.BBorrows, text="Return", command=lambda i=i: DataVault.BBorrows.returnBook(DataVault.issues[i], DataVault.BBorrows.controller, i))
            for j in range(2, len(DataVault.issues[0])):
                try:
                    b = tk.Entry(DataVault.BBorrows,justify=tk.CENTER)
                    b.grid(row=i, column=j)
                    b.insert(tk.END, str(DataVault.issues[i][j]))
                    cells[(i, j)] = b
                    if i > 0:
                        if DataVault.retbook is not None:
                            DataVault.retbook.grid(row=i, column=j + 2)
                        DataVault.borrowarr.append(DataVault.retbook)
                        DataVault.returnarr.append(b)
                except Exception as e:
                    logger.error("Error in populateTable: " + str(e) + traceback.format_exc())
                    sys.exit(-1)

    def populateResults(self, controller, document):
        DataVault.searchRes.view = tk.Button(DataVault.searchRes, text="Back", command=lambda: controller.show_frame("SearchBooks"))
        DataVault.searchRes.view.grid(ipady=5, ipadx=10)
        logger.info("Results: " + str(document))
        cells={}
        for i in range(len(document)):  # Rows
            DataVault.searchRes.borrow = tk.Button(DataVault.searchRes, text="Borrow", command= lambda i=i: DataVault.searchRes.checkBorrows(document[i], DataVault.searchRes.controller, i))
            for j in range(1, len(document[1])):  # Columns
                try:
                    b = tk.Entry(DataVault.searchRes,justify=tk.CENTER)
                    b.grid(row=i, column=j)
                    b.insert(tk.END, str(document[i][j]))
                    cells[(i, j)] = b
                except Exception as e:
                    logger.error("Error in populateTable: " + str(e) + traceback.format_exc())
                    sys.exit(-1)
            if i!=0:
                DataVault.searchRes.borrow.grid(row=i, column=j+1)
                DataVault.borrowbuttons.append(DataVault.searchRes.borrow)

    def populateMembers(self, controller, data):
        for i in range(len(data)):  # Rows
            DataVault.viewMems.details = tk.Button(DataVault.viewMems, text="Details", command=lambda i=i: DataVault.viewMems.preloadIssues(controller, i))
            DataVault.viewMems.modify = tk.Button(DataVault.viewMems, text="Modify",
                                                   command=lambda: self.viewMems.modifyMembers(controller))
            for j in range(1, len(data[1])):  # Columns
                try:
                    b = tk.Entry(DataVault.viewMems, justify=tk.CENTER)
                    b.grid(row=i, column=j)
                    b.insert(tk.END, str(data[i][j]))
                except Exception as e:
                    logger.error("Error in populateIssues: " + str(e) + traceback.format_exc())
                    sys.exit(-1)
            if i != 0:
                DataVault.viewMems.details.grid(row=i, column= len(data[1]) + 1)
                DataVault.viewMems.modify.grid(row=i, column=len(data[1]) + 2)

