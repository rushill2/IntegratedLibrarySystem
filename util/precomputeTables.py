import sys
import tkinter
import traceback

from data.dataVault import DataVault, logger
import tkinter as tk

from util.stateUtil import LoginManager


class PrecomputeTables:
    def populateResults(self, controller, document):
        for i in range(len(DataVault.bookdatafields)):
            DataVault.bookdatafields[i].grid_forget()
        logger.info("Results: " + str(document))
        for i in range(len(document)):  # Rows
            if DataVault.type == "Member":
                DataVault.searchRes.borrow = tk.Button(DataVault.searchRes, text="Borrow", command= lambda i=i: DataVault.searchRes.checkBorrows(document[i], DataVault.searchRes.controller, i))
            for j in range(len(document[1])):  # Columns
                try:
                    if DataVault.type == "Member" and (j == len(document[1])-1 or j == len(document[1])-2):
                        continue
                    b = tk.Entry(DataVault.searchRes,justify=tk.CENTER)
                    b.grid(row=i, column=j)
                    b.insert(tk.END, str(document[i][j]))
                    DataVault.bookdatafields.append(b)
                except Exception as e:
                    logger.error("Error in populateTable: " + str(e) + traceback.format_exc())
                    sys.exit(-1)
            if i!=0 and DataVault.type == "Member":
                DataVault.searchRes.borrow.grid(row=i, column=j+1)
                DataVault.borrowbuttons.append(DataVault.searchRes.borrow)
        if DataVault.searchRes.view is None:
            DataVault.searchRes.view = tk.Button(DataVault.searchRes, text="Back", command=lambda: controller.show_frame("SearchBooks"))
            DataVault.searchRes.view.grid(columnspan=10)
            DataVault.pageMap['SearchBooks'].grid_columnconfigure((0, 4), weight=1)
        LoginManager.loginManager(LoginManager,DataVault.pageMap, DataVault.type, DataVault.loggedinID, "SearchResults", controller)


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


    def populateMembers(self, controller):
        data = DataVault.viewMemberList
        viewMems = DataVault.pageMap['ViewMembers']
        # deletes the deleted value (refreshes the table each time fn is called)
        for i in range(len(DataVault.delarr)):
            if i < len(DataVault.memberarr):
                DataVault.memberarr[i].grid_forget()
                DataVault.delarr[i].grid_forget()

        # TODO: FIX modify and details button not hiding on delete

        for i in range(len(data)):  # Rows
            DataVault.viewMems.details = tk.Button(viewMems, text="Details", command=lambda i=i: viewMems.preloadIssues(controller, i))
            DataVault.viewMems.modify = tk.Button(viewMems, text="Modify",
                                                   command=lambda i=i: viewMems.modifyMembers(controller,i))
            DataVault.viewMems.delete = tk.Button(viewMems, text="Delete",
                                                  command=lambda i=i: viewMems.deleteMember(controller, i))
            for j in range(len(data[0])):  # Columns
                try:
                    b = tk.Entry(viewMems, justify=tk.CENTER)
                    b.grid(row=i+2, column=j)
                    b.insert(tk.END, str(data[i][j]))
                    if i > 0:
                        DataVault.memberarr.append(b)
                        DataVault.deetbtnarr.append(viewMems.details)
                        DataVault.modbtnarr.append(viewMems.modify)
                        DataVault.delarr.append(viewMems.delete)
                        DataVault.viewMems.details.grid(row=i+2, column=len(data[1]) + 1)
                        DataVault.viewMems.modify.grid(row=i+2, column=len(data[1]) + 2)
                        DataVault.viewMems.delete.grid(row=i+2, column=len(data[1]) + 3)
                except Exception as e:
                    logger.error("Error in populateIssues: " + str(e) + traceback.format_exc())
                    sys.exit(-1)
        LoginManager.loginManager(LoginManager,DataVault.pageMap, "Librarian", DataVault.loggedinID, "ViewMembers",controller)


    def populateDetails(self, controller, document):
        memDetails = DataVault.pageMap['MemberDetails']
        if len(document) > 1:
            memDetails.formlabel['text'] = "Issues for selected member"
        else:
            memDetails.formlabel['text'] = "No Issues for member"
        for i in range(len(document)):
            result = []
            for j in range(len(document[i])):
                if j <2 or j == 5:
                    continue
                else:
                    result.append(document[i][j])
            document[i] = result

        for i in range(len(document)):
            DataVault.notify = tk.Button(memDetails, text="Remind Member", command=lambda i=i: DataVault.memDetails.sendEmail(DataVault.issues[i], DataVault.BBorrows.controller, i))
            for j in range(len(document[0])):
                try:
                    b = tk.Entry(memDetails,justify=tk.CENTER)
                    b.grid(row=i+2, column=j)
                    b.insert(tk.END, str(document[i][j]))
                    if DataVault.notify is not None and i > 0:
                        DataVault.notify.grid(row=i+1, column=j + 3)
                except Exception as e:
                    logger.error("Error in populateTable: " + str(e) + traceback.format_exc())
                    sys.exit(-1)

        LoginManager.loginManager(LoginManager,DataVault.pageMap, "Librarian", DataVault.loggedinID, "MemberDetails", controller)