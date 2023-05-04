import sys
import time
import tkinter as tk
import traceback

from app import App, Librarian
from util.dataVault import DataVault
import logging

from util.inputValidation import Validation
from util.precomputeTables import PrecomputeTables
from util.queryCollection import QueryCollection
from util.stateUtil import LoginManager

logger = logging.getLogger()

class StaffActions(tk.Frame):
    def __init__(self, parent, controller):
        t = time.time()
        self.app = App()
        logger.info("Opening StaffActions...")
        tk.Frame.__init__(self, parent)
        self.staff = Librarian()
        self.controller = controller
        DataVault.pageMap["StaffActions"] = self
        self.label = tk.Label(self, text="Welcome! \n Pick your action", font=controller.title_font)
        self.log = None
        self.logoutbtn = None
        self.insertbook = tk.Button(self, text="Insert Book",
                                    command=lambda: self.preloadBookInsert(controller))
        self.books = tk.Button(self, text="View Books", command=lambda: self.goToSearch(controller))
        self.view_mem = tk.Button(self, text="View Members", command=lambda: self.preloadMembers(controller))
        self.create_mem = tk.Button(self, text="Create Member", command=lambda: self.preloadCreate(controller))
        DataVault.bookborrows_prev = "SearchHome"
        self.label.grid(sticky="ew", columnspan=10)
        self.books.grid(row=2, columnspan=5, pady=5)
        self.view_mem.grid(row=4, columnspan=5, pady=5)
        self.create_mem.grid(row=6, columnspan=5, pady=5)
        self.insertbook.grid(row=8, columnspan=5, pady=5)
        self.grid_columnconfigure((0, 4), weight=1)

        logger.info("SearchHome ready. Took " + str(time.time() - t) + " seconds")

    def goToSearch(self, controller):
        LoginManager.loginManager(LoginManager, DataVault.pageMap, "Librarian", DataVault.loggedinID, "SearchBooks", controller)
        DataVault.bookborrows_prev = "StaffActions"
        controller.show_frame("SearchBooks")

    def preloadBookInsert(self, controller):
        document = []
        cols = ("Title", "Edition", "Keywords", "Genre", "Authors", "Publication Date")
        entry = ("", "", "", "", "", "")
        document.append(cols)
        document.append(entry)
        insertBook = DataVault.pageMap['InsertBook']
        insertBook.variables = [tk.StringVar(), tk.StringVar(), tk.StringVar(), tk.StringVar(), tk.StringVar(), tk.StringVar()]
        insertBook.label = tk.Label(insertBook, text="If multiple values in a field, use commas")
        insertBook.label.grid(sticky='ew')
        for i in range(len(document)):
            if i > 0:
                DataVault.notify = tk.Button(insertBook, text="Insert", command = lambda: QueryCollection.insertBooks(QueryCollection, insertBook.label))
            for j in range(len(document[0])):
                try:
                    if i > 0:
                        b = tk.Entry(insertBook,justify=tk.CENTER, textvariable=insertBook.variables[j])
                    else:
                        b = tk.Entry(insertBook, justify=tk.CENTER)
                    b.grid(row=i+2, column=j, sticky='w')
                    b.insert(tk.END, str(document[i][j]))
                    if i > 0:
                        DataVault.notify.grid(row=i+1, column=j + 3, sticky='w')
                except Exception as e:
                    logger.error("Error in populateTable: " + str(e) + traceback.format_exc())
                    sys.exit(-1)

        LoginManager.loginManager(LoginManager,DataVault.pageMap, "Librarian", DataVault.loggedinID, "InsertBook", controller)
        back = tk.Button(insertBook, text="Back",
                                     command=lambda: controller.show_frame('StaffActions'))
        back.grid(row=i + 2, column=j+2)

        controller.show_frame("InsertBook")

    def transitionToInsert(self, controller, formlabel):
        insertBook = DataVault.pageMap['InsertBook']
        Validation.inputValidation(Validation, formlabel, dob=insertBook.variables[-1].get())
        if type(insertBook.variables[1]) != int:
            formlabel['text'] = 'Edition must be integer'
        else:
            result = QueryCollection.insertBooks(QueryCollection)
            if result == 0:
                formlabel['text'] = "All fields must have values"
            else:
                formlabel['text'] = "Book Inserted!"

    def preloadMembers(self, controller):
        rows = self.staff.viewMembers()
        DataVault.viewMemberList = rows
        PrecomputeTables.populateMembers(PrecomputeTables,controller)
        controller.show_frame("ViewMembers")

    def preloadCreate(self, controller):
        DataVault.pageMap['CreateMember'].createForm()
        LoginManager.loginManager(LoginManager,DataVault.pageMap, "Librarian", DataVault.loggedinID, "CreateMember", controller)

        controller.show_frame("CreateMember")

class InsertBook(tk.Frame):
    def __init__(self, parent, controller):
        t = time.time()
        self.app = App()
        self.logoutbtn = None
        logger.info("Opening SearchHome...")
        tk.Frame.__init__(self, parent)
        self.staff = Librarian()
        self.controller = controller
        DataVault.pageMap["InsertBook"] = self
        self.log = None
        logger.info("InsertBook ready. Took " + str(time.time() - t) + " seconds")

