import logging
import time
import tkinter as tk
from tkinter import font as tkfont
from app import App
from kinterUtilities import KinterUtilities

logger = logging.getLogger()
import config.data
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
        for F in (StartPage, LibrarianHome, MemberVerification, SearchHome,SearchBooks,SearchResults):
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
        logger.info("StartPage ready. Took " + str(time.time()-t) + " seconds")


class LibrarianHome(tk.Frame):

    def __init__(self, parent, controller):
        t = time.time()
        self.app = App()
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
    def __init__(self, parent, controller):
        t = time.time()
        logger.info("Opening LibrarianHome...")
        tk.Frame.__init__(self, parent)
        self.app = App()
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
            config.data.memberid = entry
            controller.show_frame('SearchHome')
        else:
            logger.error("Validation Failed. Try again.")
            self.label['text'] = "Validation Failed.Try again."

class SearchHome(tk.Frame):
    def __init__(self, parent, controller):
        t = time.time()
        self.app = App()
        logger.info("Opening SearchHome...")
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Welcome! \n Pick the type of document", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10, padx=10)
        books = tk.Button(self, text="Books",command=lambda: controller.show_frame("SearchBooks"))
        books.pack(pady=1, padx=10)
        journals = tk.Button(self, text="Journals",command=lambda: controller.show_frame("StartPage"))
        journals.pack(pady=1, padx=10)
        mags = tk.Button(self, text="Magazines", command=lambda: controller.show_frame("StartPage"))
        mags.pack(pady=1, padx=10)
        button = tk.Button(self, text="Home",command=lambda: controller.show_frame("StartPage"))
        button.pack(pady=10, padx=10)
        logger.info("SearchHome ready. Took " + str(time.time() - t) + " seconds")


class SearchBooks(tk.Frame):
    def __init__(self, parent, controller):
        self.tkutil = KinterUtilities(parent)
        self.controller = controller
        t = time.time()
        self.app = App()
        logger.info("Opening SearchBooks...")
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.label = tk.Label(self, text="Set filters and search:", font=controller.title_font)
        self.label.pack(side="top", fill="x", pady=10, padx=10)

        member_id = tk.StringVar()
        # textbox
        self.filter_entry = tk.Entry(self, textvariable=member_id, font=('calibre', 10, 'normal'))
        self.filter_entry.pack(side=tk.LEFT, padx = 10)
        # options menu
        self.opts = tk.StringVar(self)
        self.opts.set(config.data.filters[0])
        options = tk.OptionMenu(self, self.opts, *config.data.filters)
        options.pack(side=tk.LEFT, padx = 10)
        logger.info("SearchBooks ready. Took " + str(time.time() - t) + " seconds")

        # set filters and search buttons
        self.inputvalues = {}
        setfilter = tk.Button(self, text="Set Filter", command=lambda: self.addFilters(controller))
        setfilter.pack(pady=5, padx=10, side=tk.RIGHT)
        search = tk.Button(self, text="Search", command=lambda: self.searchDoc("Books"))
        search.pack(pady=5, padx=10, side=tk.RIGHT)

        # clearfilters
        clear = tk.Button(self, text="Clear Filters", command=lambda: self.clearFilters())
        clear.pack(pady=5, padx=10, side=tk.BOTTOM)

    def clearFilters(self):
        self.inputvalues = {}
        self.label['text'] = "Set filters and search:"

    def addFilters(self, controller):
        self.inputvalues[self.opts.get()]=self.filter_entry.get()
        filters_set = list(self.inputvalues.keys())
        if len(filters_set)>0:
            self.label['text'] = "Filters Set: " +str(filters_set)
        else:
            self.label['text'] = "Set filters and search:"

    def searchDoc(self, type):
        logger.info("member id : " + self.app.getMemberId())
        member = self.app.Member(self.app.getMemberId(), self.app)
        document = member.searchDocument(self.inputvalues, type)

        if document == '':
            self.label['text'] = "No document found"
            return
        self.controller.show_frame("SearchResults")

class SearchResults(tk.Frame):
    def __init__(self, parent, controller):
        t = time.time()
        self.app = App()
        logger.info("Opening SearchResults...")
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="View Members or Look for Document", font=controller.title_font)
        label.pack(side="top", fill="x", pady=20, padx=20)
        button = tk.Button(self, text="Home",
                           command=lambda: controller.show_frame("StartPage"))
        button.pack(pady=20, padx=10)
        logger.info("LibrarianHome ready. Took " + str(time.time() - t) + " seconds")



