import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import time
import dbconfig as dbcfg
from app import App


class UI(QWidget):

    def __init__(self):
        self.type = None
        self.gobutton = None
        self.button1 = None
        self.textbox1 = None
        self.button2 = None
        self.set_btn = None
        self.status = None
        self.text = None
        self.searchdict = {}
        self.app = None
        self.lib_btn = None
        self.mem_btn = None
        super().__init__()
        self.title = 'PyQt5 button - pythonspot.com'
        self.left = 760
        self.top = 270
        self.id = None
        self.width = 400
        self.homebtn = None
        self.height = 270
        self.statusquery = None
        self.searchstring = ''
        self.sqlpass()

    def sqlpass(self):
        self.homebtn = QPushButton("Return Home", self)
        self.homebtn.move(250, 200)
        self.setWindowTitle("Enter your mysql password")
        self.setGeometry(self.left, self.top, self.width, self.height)
        w = QWidget(self)
        self.statusquery = QLabel(w)
        # self.label = QLabel("My text")
        # self.layout.addWidget(self.label)
        self.statusquery.setText("Please enter your mysql server password")
        self.statusquery.move(50, 25)
        self.statusquery.show()
        self.textbox1 = QLineEdit(self)
        self.gobutton = QPushButton('Go', self)
        self.gobutton.move(200, 100)
        self.textbox1.move(100, 100)
        self.text = self.textbox1.text()
        self.gobutton.clicked.connect(self.on_click_enter)
        self.textbox1.textChanged.connect(self.textchanged)
        self.homebtn.clicked.connect(self.on_click_return)
        self.show()


    def initUI(self):

        self.setWindowTitle("Are you a librarian or a member?")
        self.setGeometry(self.left, self.top, self.width, self.height)
        w = QWidget(self)
        self.statusquery = QLabel(w)
        # self.label = QLabel("My text")
        # self.layout.addWidget(self.label)
        self.statusquery.setText("Are you a librarian or a member?")
        self.statusquery.move(95, 25)
        self.statusquery.show()
        self.lib_btn = QPushButton('Librarian', self)
        self.mem_btn = QPushButton('Member', self)

        self.lib_btn.move(100, 100)
        self.mem_btn.move(200, 100)

        self.lib_btn.clicked.connect(self.on_click_lib)
        self.mem_btn.clicked.connect(self.on_click_mem)
        self.homebtn.clicked.connect(self.on_click_return)
        self.show()


    def memberidUI(self):
        self.setWindowTitle("Enter your member ID")
        self.setGeometry(self.left, self.top, self.width, self.height)
        w = QWidget(self)
        self.statusquery = QLabel(w)
        # self.label = QLabel("My text")
        # self.layout.addWidget(self.label)
        self.statusquery.setText("Enter your member ID (only positive integers)")
        self.statusquery.move(50, 25)
        self.statusquery.show()

        self.textbox1 = QLineEdit(self)
        self.gobutton = QPushButton('Go', self)
        self.gobutton.move(200, 100)
        self.textbox1.move(100, 100)
        self.text = self.textbox1.text()
        self.gobutton.clicked.connect(self.on_click_go)
        self.textbox1.textChanged.connect(self.textchanged)
        self.homebtn.clicked.connect(self.on_click_return)
        self.show()

    def memactionUI(self):
        self.setWindowTitle("Search or Return?")
        self.setGeometry(self.left, self.top, self.width, self.height)
        w = QWidget(self)
        self.statusquery = QLabel(w)
        # self.label = QLabel("My text")
        # self.layout.addWidget(self.label)
        self.statusquery.setText("Search or Return?")
        self.statusquery.move(150, 25)
        self.statusquery.show()
        self.button1 = QPushButton('Search', self)
        self.button2 = QPushButton('Return', self)

        self.button1.move(100, 100)
        self.button2.move(200, 100)
        self.homebtn.clicked.connect(self.on_click_return)
        self.button1.clicked.connect(self.on_click_memsearch)
        self.button2.clicked.connect(self.on_click_memreturn)
        self.show()

    def memsearchUI(self):
        self.setWindowTitle("Which Type of Document are you looking for")
        self.setGeometry(self.left, self.top, self.width, self.height)
        w = QWidget(self)
        self.statusquery = QLabel(w)
        # self.label = QLabel("My text")
        # self.layout.addWidget(self.label)
        self.statusquery.setText("Which Type of Document are you looking for?")
        self.statusquery.move(65, 25)
        self.statusquery.show()
        self.button1 = QPushButton('Books', self)
        self.button2 = QPushButton('Magazines', self)
        self.button3 = QPushButton('Journals', self)

        self.button1.move(50, 100)
        self.button2.move(150, 100)
        self.button3.move(250, 100)

        self.button1.clicked.connect(self.go_to_book)
        self.button2.clicked.connect(self.go_to_mags)
        self.button2.clicked.connect(self.go_to_journ)
        self.show()

    def memsearchbook(self):
        layout = QHBoxLayout()
        self.drop = QComboBox()
        for e in dbcfg.template["Books"].values():
            self.drop.addItem(e)
        layout.addWidget(self.drop)
        self.textbox1 = QLineEdit(self)
        self.set_btn = QPushButton("Set", self)
        self.search_btn = QPushButton("Search", self)

        self.textbox1.move(260, 120)
        self.drop.setFixedSize(110, 20)
        self.setLayout(layout)
        self.drop.move(0, 200)
        self.setWindowTitle("Search Filters")
        self.set_btn.move(30, 100)
        self.search_btn.move(30, 140)
        self.text = ''
        self.set_btn.clicked.connect(self.on_click_set)
        self.search_btn.clicked.connect(self.on_click_search)
        # self.statusquery.setText("Search Filters - Hit set to set filters and Go when done")
        self.show()

    def memsearchmags(self):
        layout = QHBoxLayout()
        self.drop = QComboBox()
        for e in dbcfg.template["Mags"].values():
            self.drop.addItem(e)
        layout.addWidget(self.drop)
        self.textbox1 = QLineEdit(self)
        self.set_btn = QPushButton("Set", self)
        self.search_btn = QPushButton("Search", self)

        self.textbox1.move(260, 120)
        self.drop.setFixedSize(110, 20)
        self.setLayout(layout)
        self.drop.move(0, 200)
        self.setWindowTitle("Search Filters")
        self.set_btn.move(30, 100)
        self.search_btn.move(30, 140)
        self.text = ''
        self.set_btn.clicked.connect(self.on_click_set)
        self.search_btn.clicked.connect(self.on_click_search)
        # self.statusquery.setText("Search Filters - Hit set to set filters and Go when done")
        self.show()

    def memsearchjourn(self):
        layout = QHBoxLayout()
        self.drop = QComboBox()
        for e in dbcfg.template["Journs"].values():
            self.drop.addItem(e)
        layout.addWidget(self.drop)
        self.textbox1 = QLineEdit(self)
        self.set_btn = QPushButton("Set", self)
        self.search_btn = QPushButton("Search", self)

        self.textbox1.move(260, 120)
        self.drop.setFixedSize(110, 20)
        self.setLayout(layout)
        self.drop.move(0, 200)
        self.setWindowTitle("Search Filters")
        self.set_btn.move(30, 100)
        self.search_btn.move(30, 140)
        self.text = ''
        self.set_btn.clicked.connect(self.on_click_set)
        self.search_btn.clicked.connect(self.on_click_search)
        # self.statusquery.setText("Search Filters - Hit set to set filters and Go when done")
        self.show()

    def searchresults(self, result):
        for e in result:
            self.drop.addItem(e)
        self.lookup_btn = QPushButton("Details", self)

        self.drop.setFixedSize(110, 20)
        self.drop.move(0, 200)
        self.setWindowTitle("Search Results")

        self.lookup_btn.move(30, 140)
        self.text = ''
        self.lookup_btn.clicked.connect(self.on_click_lookup)
        # self.statusquery.setText("Search Filters - Hit set to set filters and Go when done")
        self.show()

    def displaydetails(self, data):
        # # TODO: to create a visual output for the book data
        # have a borrow button and onclick - onclick_borrow



    @pyqtSlot()
    def on_click_go(self):
        if self.text.isnumeric():
            if not self.app.validateLogin(self.text):
                self.statusquery.setText("Account does not exist. Contact a Librarian")
            else:
                self.id = self.text
                self.gobutton.hide()
                self.close()
                self.textbox1.hide()
                self.statusquery.setText('')
                self.memactionUI()

    def textchanged(self, text):
        self.text = text

    def on_click_lib(self):
        self.status = "Member"
        self.lib_btn.hide()
        self.mem_btn.hide()


    def on_click_mem(self):
        self.status = "Member"
        self.state = "memberlogin"
        self.close()
        self.lib_btn.hide()
        self.mem_btn.hide()
        self.statusquery.setText('')
        self.memberidUI()

    def on_click_memsearch(self):
        self.close()
        self.statusquery.setText('')
        self.button1.hide()
        self.button2.hide()
        self.textbox1.hide()
        self.memsearchUI()

    def on_click_memreturn(self):
        print("Return")

    def on_click_return(self):
        self.close()
        self.statusquery.setText('')
        self.sqlpass()

    def on_click_enter(self):

        try:
            self.app = App()
            self.app.populate(self.text)
            self.close()
            self.statusquery.setText('')
            self.gobutton.hide()
            self.textbox1.hide()
            self.initUI()
        except Exception as e:
            self.statusquery.setText("Incorrect Password. Please review the text")

    def on_click_go_book(self):
        print("HIU")

    def go_to_book(self):
        self.type = self.button1.text()
        self.button1.hide()
        self.button2.hide()
        self.button3.hide()
        self.statusquery.setText('')
        self.close()
        self.memsearchbook()

    def go_to_mags(self):
        self.type = self.button2.text()
        self.button1.hide()
        self.button2.hide()
        self.button3.hide()
        self.statusquery.setText('')
        self.memsearchmags()

    def go_to_journ(self):
        self.type = self.button3.text()
        self.button1.hide()
        self.button2.hide()
        self.button3.hide()
        self.statusquery.setText('')
        self.memsearchjourn()


    def on_click_set(self):
        key = self.drop.currentText()
        self.searchdict[key] = self.textbox1.text()

    def on_click_search(self):
        mem = self.app.Member(self.id, self.app)
        names = mem.searchDocument(self.searchdict, self.type, self.app)
        namelist = names.split(',')
        self.close()
        self.set_btn.hide()
        self.search_btn.hide()
        self.textbox1.hide()
        self.drop.clear()
        self.searchresults(namelist)

    def on_click_lookup(self):
        mem = self.app.Member(self.id, self.app)
        rows = mem.getRecords(self.drop.currentText(), self.type)
        ## here call ur next function
        # do the hides/closes for widgets
        self.displaydetails(rows)

    def onclick_borrow(self):
        mem = self.app.Member(self.id, self.app)
        mem.borrowDocument(self.type,self.id)
