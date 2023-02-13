import time
import tkinter as tk
from app import App, Librarian
from data.dataVault import DataVault
import logging

logger = logging.getLogger()

class StaffActions(tk.Frame):
    def __init__(self, parent, controller):
        t = time.time()
        self.app = App()
        logger.info("Opening SearchHome...")
        tk.Frame.__init__(self, parent)
        self.staff = Librarian()
        self.controller = controller
        dims = self.grid_size()
        DataVault.pageMap["StaffActions"] = self

        self.label = tk.Label(self, text="Welcome! \n Pick your action", font=controller.title_font)
        self.log = None
        self.books = tk.Button(self, text="View Documents", command=lambda: self.goToSearch(controller))
        self.view_mem = tk.Button(self, text="View Members", command=lambda: self.preloadMembers(controller))
        self.create_mem = tk.Button(self, text="Create Member", command=lambda: self.preloadCreate(controller))
        self.button = tk.Button(self, text="Home", command=lambda: controller.show_frame("StartPage"))
        DataVault.bookborrows_prev = "SearchHome"
        self.label.grid(sticky="ew", columnspan=10)
        self.books.grid(row=2, columnspan=5, pady=5)
        self.view_mem.grid(row=4, columnspan=5, pady=5)
        self.create_mem.grid(row=6, columnspan=5, pady=5)
        self.button.grid(row=8, columnspan=5, pady=5)
        self.grid_columnconfigure((0, 4), weight=1)

        logger.info("SearchHome ready. Took " + str(time.time() - t) + " seconds")

    def goToSearch(self, controller):
        DataVault.bookborrows_prev = "StaffActions"
        controller.show_frame("SearchBooks")

    def preloadMembers(self, controller):
        rows = self.staff.viewMembers()
        DataVault.viewMemberList = rows
        DataVault.populateMembers(DataVault, controller)
        controller.show_frame("ViewMembers")

    def preloadCreate(self, controller):
        DataVault.loggedIn(DataVault, "Librarian", DataVault.loggedinID, "CreateMember")
        controller.show_frame("CreateMember")


