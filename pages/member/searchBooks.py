import time
import tkinter as tk

import data.dumps
from data.dataVault import DataVault
from util.kinterUtilities import KinterUtilities
import app
import logging

from util.memberSQL import Member

logger = logging.getLogger()


class SearchBooks(tk.Frame):

    def __init__(self, parent, controller):
        DataVault.searchBooks = self
        self.tkutil = KinterUtilities(parent)
        self.controller = controller
        t = time.time()
        self.app = app.App()
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
        self.opts.set(data.dumps.filters[0])
        options = tk.OptionMenu(self, self.opts, *data.dumps.filters)
        options.pack(side=tk.LEFT, padx=10)
        logger.info("SearchBooks ready. Took " + str(time.time() - t) + " seconds")

        # set filters and search buttons
        self.inputvalues = {}
        setfilter = tk.Button(self, text="Set Filter", command=lambda: self.addFilters(controller))
        setfilter.pack(pady=5, padx=10, side=tk.RIGHT)
        search = tk.Button(self, text="Search", command=lambda: self.preloadResults(controller))
        search.pack(pady=5, padx=10, side=tk.RIGHT)

        # clearfilters
        clear = tk.Button(self, text="Clear Filters", command=lambda: self.clearFilters())
        clear.pack(pady=5, padx=10, side=tk.RIGHT)

        view = tk.Button(self, text="Back", command=lambda: self.goBack(controller))
        view.pack(pady=5, padx=10, side=tk.LEFT)

    def goBack(self, controller):
        controller.show_frame(DataVault.bookborrows_prev)
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
        document = Member(DataVault.mem_id, DataVault.searchRes.app).searchDocument(DataVault.inputvalues, "Books")
        DataVault.populateResults(DataVault, controller, document)
        controller.show_frame("SearchResults")
