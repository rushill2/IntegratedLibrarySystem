import datetime
import sys
import time
import tkinter as tk
import traceback

from app import App, Librarian
from util.dataVault import DataVault
from pages.librarian.staffActions import logger
from util.inputValidation import Validation
from util.memberSQL import Member
from util.precomputeTables import PrecomputeTables
from util.queryCollection import QueryCollection


class ViewMembers(tk.Frame):
    def __init__(self, parent, controller):
        t = time.time()
        DataVault.viewMems = self
        self.app = App()
        self.log = None
        self.logoutbtn = None
        self.member = Member(DataVault.mem_id, self.app)
        logger.info("Opening SearchHome...")
        tk.Frame.__init__(self, parent)
        self.staff = Librarian()
        DataVault.pageMap["ViewMembers"] = self

        self.controller = controller

        self.back = tk.Button(self, text="Back", command=lambda: controller.show_frame('StaffActions'))
        self.back.grid(row=2, column=8)

    # TODO: Preload the overdues and issues for members
    def preloadIssues(self, controller, row):
        # display member information
        try:
            DataVault.currMem = DataVault.viewMemberList[row-1]
            issues = self.member.getIssuesbyMemId(DataVault.currMem[0])
            # display title, date of issue, due date and option to notify via email
            # TODO: Change all populate security from DataVault variables to fn params
            DataVault.issues = issues
            if not issues or len(issues)==0:
                DataVault.pageMap['MemberDetails'].formlabel['text'] = "No Books issued!"
                return
            for i in range(len(issues)):
                today = datetime.date.today()
                if today < issues[i][4]:
                    issues[i] += ("Overdue",)
                else:
                    issues[i] += ("On Time",)

            issues += (("Issue Id", "Document Id", "Title", "Issue Date", "Due Date","Memid", "Status"),)
            issues.reverse()
            PrecomputeTables.populateDetails(PrecomputeTables,controller, issues)
            controller.show_frame("MemberDetails")
        except Exception as e:
            logger.error("Error in preloadIssues: " + str(e) + traceback.format_exc())
            sys.exit(-1)


    def modifyMembers(self, controller, row):
        self.firstname = tk.StringVar()
        self.lastname = tk.StringVar()
        self.dob = tk.StringVar()
        self.phone = tk.StringVar()
        self.email = tk.StringVar()
        document = []
        self.memberid = DataVault.viewMemberList[row-1][0]

        # don't want books borrowed field and password
        for i,e in enumerate(DataVault.viewMemberList):
            if i == 0 or i == row:
                result = ()
                for k,v in enumerate((e)):
                    if k == 4 or k == 5 or k==0:
                        continue
                    else:
                        result += (v,)
                document.append(result)
        # cant loop since we need a reference to each. better on space this way avoiding array
        # first the columns
        for i in range(len(document[0])):
            b = tk.Entry(DataVault.pageMap['ModifyMember'], justify=tk.CENTER)
            b.grid(row=2, column=i)
            b.insert(tk.END, str(document[0][i]))
        j = 0
        i = 1

        self.fname = tk.Entry(DataVault.pageMap["ModifyMember"], justify=tk.CENTER, textvariable=self.firstname)
        self.fname.grid(row=i+2, column=j)
        self.fname.insert(tk.END, str(document[i][j]))
        j += 1

        self.lname = tk.Entry(DataVault.pageMap["ModifyMember"], justify=tk.CENTER, textvariable=self.lastname)
        self.lname.grid(row=i+2, column=j)
        self.lname.insert(tk.END, str(document[i][j]))
        j += 1

        self.birth = tk.Entry(DataVault.pageMap["ModifyMember"], justify=tk.CENTER, textvariable=self.dob)
        self.birth.grid(row=i+2, column=j)
        self.birth.insert(tk.END, str(document[i][j]))
        j += 1

        self.contact = tk.Entry(DataVault.pageMap["ModifyMember"], justify=tk.CENTER, textvariable=self.phone)
        self.contact.grid(row=i+2, column=j)
        self.contact.insert(tk.END, str(document[i][j]))
        j += 1

        self.mail = tk.Entry(DataVault.pageMap["ModifyMember"], justify=tk.CENTER, textvariable=self.email)
        self.mail.grid(row=i+2, column=j)
        self.mail.insert(tk.END, str(document[i][j]))
        j += 1
        formlabel = tk.Label(DataVault.pageMap['ModifyMember'], text='Modify Details and update')
        formlabel.grid(sticky='ew', columnspan=10, row = 0)
        update = tk.Button(DataVault.pageMap['ModifyMember'], text="Update",
                      command=lambda: self.validateInput(controller, formlabel, row))
        update.grid(row=i+2, column=j+2)

        controller.show_frame("ModifyMember")

    def validateInput(self, controller, formlabel, row):
        firstname = self.firstname.get()
        lastname = self.lastname.get()
        dob = self.dob.get()
        phone = self.phone.get()
        email = self.email.get()
        valid_input, hash = Validation.inputValidation(Validation, formlabel, email=email, phone=phone,dob=dob)
        # TODO: Test, input validation function may autoreject
        if valid_input:
            QueryCollection.updateMemberInfo(QueryCollection)
            # self.fname.grid_forget()
            # self.lname.grid_forget()
            # self.mail.grid_forget()
            # self.contact.grid_forget()
            formlabel['text'] = "Information updated!"


    def deleteMember(self, controller, row):
        memid = DataVault.viewMemberList[row-1][0]
        Member.deleteMember(Member, memid)
        DataVault.viewMemberList = self.staff.viewMembers()
        DataVault.deetbtnarr[row-1].grid_forget()
        DataVault.modbtnarr[row-1].grid_forget()
        PrecomputeTables.populateMembers(PrecomputeTables,controller)
        pass
