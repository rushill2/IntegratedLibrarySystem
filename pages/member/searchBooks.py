import time
import tkinter as tk

import security.dumps
from util.dataVault import DataVault
import app
import logging

from util.memberSQL import Member
from util.precomputeTables import PrecomputeTables
from util.queryCollection import QueryCollection

logger = logging.getLogger()


class SearchBooks(tk.Frame):

    def __init__(self, parent, controller):
        DataVault.searchBooks = self
        self.controller = controller
        t = time.time()
        self.app = app.App()
        self.log = None
        self.logoutbtn = None
        logger.info("Opening SearchBooks...")
        tk.Frame.__init__(self, parent)
        self.controller = controller
        dims = self.grid_size()
        self.label = tk.Label(self, text="Set filters and search:", font=controller.title_font)
        self.label.grid(row=2, columnspan = 10)
        DataVault.pageMap["SearchBooks"] = self


        member_id = tk.StringVar()

        # textbox
        self.filter_entry = tk.Entry(self, textvariable=member_id, font=('calibre', 10, 'normal'))
        self.filter_entry.grid(row=3, columnspan=5)
        # options menu
        self.opts = tk.StringVar(self)
        self.opts.set(security.dumps.filters[0])
        options = tk.OptionMenu(self, self.opts, *security.dumps.filters)
        options.grid(row=4, columnspan=5)
        logger.info("SearchBooks ready. Took " + str(time.time() - t) + " seconds")

        # set filters and search buttons
        self.inputvalues = {}
        setfilter = tk.Button(self, text="Set Filter", command=lambda: self.addFilters(controller))
        setfilter.grid(row=5, columnspan=5)
        search = tk.Button(self, text="Search", command=lambda: self.preloadResults(controller))
        search.grid(row=6, columnspan=5)

        # clearfilters
        clear = tk.Button(self, text="Clear Filters", command=lambda: self.clearFilters())
        clear.grid(row=7, columnspan=5)

        view = tk.Button(self, text="Back", command=lambda: self.goBack(controller))
        view.grid(row=8, columnspan=5)
        self.grid_columnconfigure((0, 4), weight=1)

    def goBack(self, controller):
        if DataVault.type == "Member":
            controller.show_frame("SearchHome")
        else:
            controller.show_frame("StaffActions")
    def clearFilters(self):
        self.inputvalues = {}
        DataVault.inputvalues = {}
        self.label['text'] = "Set filters and search:"

    def addFilters(self, controller):
        self.inputvalues[self.opts.get()] = self.filter_entry.get()
        DataVault.inputvalues[self.opts.get()] = self.filter_entry.get()
        filters_set = list(self.inputvalues.keys())
        if len(filters_set) > 0:
            self.label['text'] = "Filters Set: " + str(filters_set)
        else:
            self.label['text'] = "Set filters and search:"

    def preloadResults(self, controller):
        if DataVault.type == "Member":
            DataVault.bookborrows_prev = "SearchHome"
        else:
            DataVault.bookborrows_prev = 'StaffActions'

        if len(DataVault.inputvalues) == 0:
            DataVault.pageMap['SearchResults'].label['text'] = "No filters set. All books shown."
            document = QueryCollection.allBooks(QueryCollection)
        else:
            document = Member(DataVault.mem_id, DataVault.searchRes.app).searchDocument(DataVault.inputvalues, "Books")

        # here, loop through the doc ids and get # copies and members
        document.insert(0, ("Id", "Title", "Edition", "Keywords", "Genre", "Authors", "Publication Date", "Issued By", "#Copies"))
        for i in range(len(document)):
            if i == 0:
                continue
            issued_by, copies = QueryCollection.issueData(QueryCollection, document[i][0])
            if issued_by is None:
                document[i] += (None, copies)
            else:
                document[i] += (issued_by[0], copies)
        PrecomputeTables.populateResults(PrecomputeTables,controller, document)
        controller.show_frame("SearchResults")
