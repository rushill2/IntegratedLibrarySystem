import tkinter as tk
from data.dataVault import DataVault


class LoginManager:
    def loginManager(self, pageMap, type, id, page, controller):
        fragment = pageMap[page]
        if fragment.log:
            fragment.log.grid_forget()
        if fragment.logoutbtn:
            fragment.logoutbtn.grid_forget()
        if id is None:
            ltext = "Not Logged in yet"
            if fragment.log is None:
                fragment.log = tk.Label(fragment, text=ltext)
                fragment.log.config(fg="gray")

                fragment.log.grid(sticky="ew", columnspan=10)
        else:
            ltext = "Logged in as " + type + ": " + str(id)
            if fragment.log is None:
                fragment.log = tk.Label(fragment, text=ltext)
                fragment.log.config(fg="gray")
                fragment.logoutbtn = tk.Button(fragment, text="Logout", command= lambda: self.logout(LoginManager, controller, fragment))
                fragment.logoutbtn.grid(columnspan=10)
                fragment.log.grid(sticky="ew", columnspan=10)
                fragment.grid_columnconfigure((0, 4), weight=1)

    def logout(self, controller, fragment):
        fragment.log = None
        DataVault.type = None
        DataVault.globallog = None
        DataVault.loggedinID = None
        DataVault.pageMap['StartPage'].label['text'] = "You have been logged out \n Are you a member or librarian?"
        controller.show_frame("StartPage")