import time
import tkinter as tk

import data.data
from util.kinterUtilities import KinterUtilities
import app
import logging

logger = logging.getLogger()


class SearchBooks(tk.Frame):
    inputvalues = {}

    def __init__(self, parent, controller):
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
        self.opts.set(data.data.filters[0])
        options = tk.OptionMenu(self, self.opts, *data.data.filters)
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
