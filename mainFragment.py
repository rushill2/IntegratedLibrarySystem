import logging
import tkinter as tk
from tkinter import font as tkfont
from app import App
from pages.librarian.librarianHome import LibrarianHome
from pages.librarian.modifyMember import ModifyMember
from pages.librarian.staffActions import StaffActions, InsertBook
from auth.twoFA import TwoFALogin, TwoFACreate
from pages.librarian.memberDetails import MemberDetails
from pages.librarian.viewMembers import ViewMembers
from pages.member.memberVerification import MemberVerification
from pages.member.searchBooks import SearchBooks
from pages.member.searchHome import SearchHome
from pages.member.searchResults import SearchResults
from pages.member.booksBorrowed import BookBorrows
from pages.librarian.loginLibrarian import LoginLibrarian
from pages.librarian.createLibrarian import CreateLibrarian
from pages.librarian.createMember import CreateMember

from pages.startPage import StartPage

logger = logging.getLogger()

app = App()
global member_logged
member_logged=None

# def setMember(id):
#     global member_logged
#     member_logged = app.Member(id,app)
#
# def getMember(id):
#     global member_logged
#     return member_logged

class SampleApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title_font = tkfont.Font(family='Calibri', size=12)

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage, LibrarianHome, MemberVerification, SearchHome, SearchBooks, SearchResults, BookBorrows, CreateLibrarian, LoginLibrarian,
                  StaffActions, ViewMembers, CreateMember, MemberDetails, TwoFACreate, TwoFALogin, ModifyMember, InsertBook):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()


