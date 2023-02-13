import datetime
import time
import tkinter as tk
import traceback

from app import App, Librarian
from data.dataVault import DataVault
from pages.librarian.staffActions import logger
from util.memberSQL import Member


class ViewMembers(tk.Frame):
    def __init__(self, parent, controller):
        t = time.time()
        DataVault.viewMems = self
        self.app = App()
        self.member = Member(DataVault.mem_id, self.app)
        logger.info("Opening SearchHome...")
        tk.Frame.__init__(self, parent)
        self.staff = Librarian()
        DataVault.pageMap["ViewMembers"] = self

        self.controller = controller

        self.back = tk.Button(self, text="Back", command=lambda: controller.show_frame('StaffView'))
        self.back.grid(row=2, column=8)

    # TODO: Preload the overdues and issues for members
    def preloadIssues(self, controller, row):
        # display member information
        try:
            DataVault.currMem = DataVault.viewMemberList[row]
            issues = self.member.getIssuesbyMemId(DataVault.currMem[0])
            # display title, date of issue, due date and option to notify via email
            # TODO: Change all populate data from DataVault variables to fn params
            DataVault.issues = issues
            for i in range(len(issues)):
                today = datetime.date.today()
                if today < issues[i][4]:
                    issues[i] += ("Overdue",)
                else:
                    issues[i] += ("On Time",)

            issues += (("Issue Id", "Document Id", "Title", "Issue Date", "Due Date","Memid", "Status"),)
            issues.reverse()
            DataVault.loggedIn(DataVault, "Librarian", DataVault.loggedinID, "MemberDetails")
            DataVault.populateDetails(DataVault, controller, issues)
            controller.show_frame("MemberDetails")
        except Exception as e:
            logger.error("Error in preloadIssues: " + str(e) + traceback.format_exc())


    def modifyMembers(self, controller, row):
        pass

    def deleteMember(self, controller, row):
        memid = DataVault.viewMemberList[row][0]
        Member.deleteMember(Member, memid)
        DataVault.viewMemberList = self.staff.viewMembers()
        DataVault.populateMembers(DataVault, controller)
        pass
