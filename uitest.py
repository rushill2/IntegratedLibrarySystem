import logging
import tkinter as tk
from tkinter import font as tkfont
from app import App
from pages.librarianHome import LibrarianHome
from pages.memberVerification import MemberVerification
from pages.searchBooks import SearchBooks
from pages.searchHome import SearchHome
from pages.searchResults import SearchResults
from pages.startPage import StartPage

logger = logging.getLogger()

app = App()
global member_logged
member_logged=None

def setMember(id):
    global member_logged
    member_logged = app.Member(id,app)

def getMember(id):
    global member_logged
    return member_logged

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
        for F in (StartPage, LibrarianHome, MemberVerification, SearchHome, SearchBooks, SearchResults):
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


# class FilteredOptions(tk.Frame):
#     dropdown=0
#     def __init__(self, parent, controller):
#         t = time.time()
#         self.tkutil = KinterUtilities(parent)
#         self.app = App()
#         logger.info("Opening SearchResults...")
#         tk.Frame.__init__(self, parent)
#         self.controller = controller
#         FilteredOptions.filt = tk.StringVar()
#         # try:
#         #     self.filt.trace("w", lambda *args: self.createDropDown(parent))
#         # except Exception as e:
#         #     logger.error(str(e) + traceback.format_exc())
#         if names:
#             document = self.app.Member(MemberVerification.mem_id, app).searchDocument(SearchBooks.inputvalues, "Books")
#             names = []
#             for i in range(len(document)):
#                 names.append(document[i][2])
#             selection = tk.StringVar()
#             w = tk.OptionMenu(parent, selection, *names)
#             w.pack()
#
#     # def createDropDown(self, parent):
#


# TODO: Need to figure listener so we can remove the button Results