import logging
import sys
import time
import tkinter as tk
import traceback
from tkinter import font as tkfont
from app import App
from kinterUtilities import KinterUtilities

logger = logging.getLogger()

import config.data
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


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        app = App()
        app.populate()
        logger.info("DB connection successful!")
        t = time.time()
        logger.info("Opening StartPage...")
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Are you a member or librarian?", font=controller.title_font)
        label.pack(side="top", fill="x", pady=20, padx=20)

        button1 = tk.Button(self, text="Member",
                            command=lambda: controller.show_frame("MemberVerification"))
        button2 = tk.Button(self, text="Librarian",
                            command=lambda: controller.show_frame("LibrarianHome"))
        button1.pack(pady=0, padx=10)
        button2.pack(pady=10, padx=10)
        logger.info("StartPage ready. Took " + str(time.time() - t) + " seconds")


class LibrarianHome(tk.Frame):

    def __init__(self, parent, controller):
        t = time.time()
        self.app = app
        logger.info("Opening LibrarianHome...")
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="View Members or Look for Document", font=controller.title_font)
        label.pack(side="top", fill="x", pady=20, padx=20)
        button = tk.Button(self, text="Home",
                           command=lambda: controller.show_frame("StartPage"))
        button.pack(pady=20, padx=10)
        logger.info("LibrarianHome ready. Took " + str(time.time() - t) + " seconds")


class MemberVerification(tk.Frame):
    mem_id = None
    def __init__(self, parent, controller):
        t = time.time()
        logger.info("Opening LibrarianHome...")
        tk.Frame.__init__(self, parent)
        global app
        self.app = app
        self.app.populate()
        self.controller = controller

        # description text
        self.label = tk.Label(self, text="Enter your Member ID", font=controller.title_font)
        self.label.pack(side="top", fill="x", pady=20, padx=20)

        # buttons
        home = tk.Button(self, text="Home",
                         command=lambda: controller.show_frame("StartPage"))
        # get value from entry when pressed
        submit = tk.Button(self, text="Submit",
                           command=lambda: self.get_member_id(controller))
        member_id = tk.StringVar()

        # textbox
        self.id_entry = tk.Entry(self, textvariable=member_id, font=('calibre', 10, 'normal'))

        # displaying everything
        self.id_entry.pack()
        submit.pack(pady=5, padx=10)
        home.pack(pady=5, padx=10)
        logger.info("MemberVerification ready. Took " + str(time.time() - t) + " seconds")

        #  value getter for member id that validates with db

    def get_member_id(self, controller):
        entry = self.id_entry.get()
        logger.info("Validating Member ID: " + entry + '...')
        if self.app.validateLogin(entry):
            logger.info("Validation Successful! Welcome member " + entry)
            setMember(entry)
            MemberVerification.mem_id = entry
            controller.show_frame('SearchHome')
        else:
            logger.error("Validation Failed. Try again.")
            self.label['text'] = "Validation Failed.Try again."


class SearchHome(tk.Frame):
    def __init__(self, parent, controller):
        t = time.time()
        self.app = app
        logger.info("Opening SearchHome...")
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Welcome! \n Pick the type of document", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10, padx=10)
        books = tk.Button(self, text="Books", command=lambda: controller.show_frame("SearchBooks"))
        books.pack(pady=1, padx=10)
        journals = tk.Button(self, text="Journals", command=lambda: controller.show_frame("StartPage"))
        journals.pack(pady=1, padx=10)
        mags = tk.Button(self, text="Magazines", command=lambda: controller.show_frame("StartPage"))
        mags.pack(pady=1, padx=10)
        button = tk.Button(self, text="Home", command=lambda: controller.show_frame("StartPage"))
        button.pack(pady=10, padx=10)
        logger.info("SearchHome ready. Took " + str(time.time() - t) + " seconds")


class SearchBooks(tk.Frame):
    inputvalues = {}

    def __init__(self, parent, controller):
        self.tkutil = KinterUtilities(parent)
        self.controller = controller
        t = time.time()
        self.app = app
        logger.info("Opening SearchBooks...")
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.label = tk.Label(self, text="Set filters and search:", font=controller.title_font)
        self.label.pack(side="top", fill="x", pady=10, padx=10)

        member_id = tk.StringVar()
        # textbox
        self.filter_entry = tk.Entry(self, textvariable=member_id, font=('calibre', 10, 'normal'))
        self.filter_entry.pack(side=tk.LEFT, padx=10)
        # options menu
        self.opts = tk.StringVar(self)
        self.opts.set(config.data.filters[0])
        options = tk.OptionMenu(self, self.opts, *config.data.filters)
        options.pack(side=tk.LEFT, padx=10)
        logger.info("SearchBooks ready. Took " + str(time.time() - t) + " seconds")

        # set filters and search buttons
        self.inputvalues = {}
        setfilter = tk.Button(self, text="Set Filter", command=lambda: self.addFilters(controller))
        setfilter.pack(pady=5, padx=10, side=tk.RIGHT)
        search = tk.Button(self, text="Next", command=lambda: controller.show_frame("SearchResults"))
        search.pack(pady=5, padx=10, side=tk.RIGHT)

        # clearfilters
        clear = tk.Button(self, text="Clear Filters", command=lambda: self.clearFilters())
        clear.pack(pady=5, padx=10, side=tk.BOTTOM)

    def clearFilters(self):
        self.inputvalues = {}
        SearchBooks.inputvalues = {}
        self.label['text'] = "Set filters and search:"

    def addFilters(self, controller):
        self.inputvalues[self.opts.get()] = self.filter_entry.get()
        SearchBooks.inputvalues[self.opts.get()] = self.filter_entry.get()
        filters_set = list(self.inputvalues.keys())
        if len(filters_set) > 0:
            self.label['text'] = "Filters Set: " + str(filters_set)
        else:
            self.label['text'] = "Set filters and search:"

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


class SearchResults(tk.Frame):
    def __init__(self, parent, controller):
        t = time.time()
        self.tkutil = KinterUtilities(parent)
        self.app = App()
        logger.info("Opening SearchResults...")
        tk.Frame.__init__(self, parent)
        self.controller = controller
        logger.info("SearchResults ready. Took " + str(time.time() - t) + " seconds")
        filters = SearchBooks.inputvalues
        self.view = tk.Button(self, text="Results", command=lambda: self.populateResults(filters))
        self.view.grid(ipady=5, ipadx=10)


    def populateResults(self, filters):
        self.view.grid_forget()
        document = self.app.Member(MemberVerification.mem_id, app).searchDocument(SearchBooks.inputvalues, "Books")
        logger.info("Results: " + str(document) + " for string filters: " + str(filters))
        cells={}
        for i in range(len(document)):  # Rows
            borrow = tk.Button(self, text="Borrow")
            retbook = tk.Button(self, text="Return")
            for j in range(len(document[0])):  # Columns
                try:
                    b = tk.Entry(self)

                    b.grid(row=i, column=j)
                    b.insert(tk.END, str(document[i][j]))
                    cells[(i, j)] = b
                except Exception as e:
                    logger.error("Error in populateTable: " + str(e) + traceback.format_exc())
                    sys.exit(-1)
            if i!=0:
                borrow.grid(row=i, column=j+1)
                retbook.grid(row=i, column=j+2)


# TODO: Need to figure listener so wecan remove the button Results