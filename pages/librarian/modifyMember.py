import datetime
import time
import tkinter as tk
import traceback

from app import App, Librarian
from data.dataVault import DataVault
from pages.librarian.staffActions import logger
from util.memberSQL import Member
from util.precomputeTables import PrecomputeTables


class ModifyMember(tk.Frame):
    def __init__(self, parent, controller):
        t = time.time()
        self.app = App()
        self.log = None
        self.logoutbtn = None
        self.member = Member(DataVault.mem_id, self.app)
        logger.info("Opening SearchHome...")
        tk.Frame.__init__(self, parent)
        self.staff = Librarian()
        DataVault.pageMap["ModifyMember"] = self
        self.controller = controller

        self.back = tk.Button(self, text="Back", command=lambda: self.reloadMembers(controller))
        self.back.grid(row=2, column=8)

    def reloadMembers(self, controller):
        rows = self.staff.viewMembers()
        DataVault.viewMemberList = rows
        PrecomputeTables.populateMembers(PrecomputeTables,controller)
        controller.show_frame('ViewMembers')