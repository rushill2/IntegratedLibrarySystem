import datetime

import mysql.connector
import dbconfig as dbcfg
import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *



class App:


    def __init__(self):
        self.mydb = None
        self.mycursor = None
        self.password = None

    def populate(self, passkey):
        # create librarian db if it doesn't exist
        self.mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password=passkey,
        )
        self.mycursor = self.mydb.cursor(buffered=True)
        self.mycursor.execute("SHOW DATABASES")
        create = any(db for db in self.mycursor if db == ('librarian',))

        if not create:
            self.mycursor.execute("CREATE DATABASE Librarian")

        self.createTables()


    def createTables(self):
        # if table does not exist, create it
        creates = dbcfg.createtable
        tables = dbcfg.tables
        for k,v in creates.items():
            try:
                self.mycursor.execute("USE librarian")
                self.mycursor.execute(v)
            except Exception as e:
                sys.exit(-2)

    def validateLogin(self, id):
        sql = dbcfg.sql['memberlogin'].replace('{_id}', str(id))
        try:
            self.mycursor.execute(sql)
            self.mycursor.fetchall()
            print(sql)
            if self.mycursor.rowcount == 0:
                print("0 count")
                return False
            else:
                print("Found rows")
                return True
        except Exception as e:
            print("Validate Error", e)


    # class Librarian:
    #     def __init__(self, id):
    #         self.lib_id = id
    #
    #     def addDocument(self, doctype):
    #
    #     def editDocument(self, doctype):
    #
    #     def deleteDocument(self, doctype):
    #
    #     def viewDocument(self, doctype, task):
    #         # Check overdue issues
    #
    #     def manageUsers(self, doctype):
    #         # TO-DO: Add or remove members
    #

    class Member:

        def __init__(self, id, app):
            self.mem_id = id
            self.cursor = app.mydb.cursor(buffered=True)

        def searchDocument(self, params, doctype, app):
            sql = dbcfg.sql['searchDocs'].replace("{_tbl}", doctype)
            i = len(list(params.values()))-1
            for k,v in params.items():
                if len(v)==0:
                    continue
                if i != 0:
                    if k == "Publication_Date":
                        vals = v.split('-')
                        date = datetime.datetime(int(vals[0]), int(vals[1]), int(vals[2]))
                        sql += k + " = " + str(date) + ' AND '
                    if k == "Authors" or k == "Keywords" or k == "Contributors":
                            sql += k + " LIKE " + "'%" + v + "%'" + ' AND '
                    else:
                            sql += k + " = " + '"'+ v + '"' + ' AND '
                else:
                    if k == "Publication_Date":
                        vals = v.split('-')
                        date = datetime.date(int(vals[0]), int(vals[1]), int(vals[2]))
                        sql += k + " = " + str(date) + ' AND '
                    if k == "Authors" or k == "Keywords" or k == "Contributors":
                            sql += k + " LIKE " + "'%" + v + "%'"
                    else:
                            sql += k + " = " + '"'+ v + '"'
                i -= 1

            try:
                print(sql)
                nosql = "SELECT * FROM librarian.Books WHERE Book_Title = 'name1';"
                self.cursor.execute(sql)
                self.cursor.fetchall()
                if self.cursor.rowcount==0:
                    return ""
                names = ""
                for r in self.cursor._rows:
                    names += r[1] +','
                return names[:-1]

            except Exception as e:
                print("SEARCH ERROR", e)

        def getRecords(self, name, type):
            name = '"' + name + '"'
            if type == "Books":
                sql = "SELECT * FROM librarian.{_tbl} where Book_Title = {_title}".replace("{_tbl}", type).replace("{_title}", name)

            elif type == "Magazines":
                sql = "SELECT * FROM librarian.{_tbl} where Title = {_title}".replace("{_tbl}", type).replace("{_title}", name)

            else:
                sql = "SELECT * FROM librarian.{_tbl} where Book_Title = {_title}".replace("{_tbl}", type).replace("{_title}", name)

            print(sql)
            self.cursor.execute(sql)
            self.cursor.fetchall()
            data = self.cursor._rows[0]
            print(data)
            return data
        def borrowDocument(self, doctype, id):

            # if copies > 0 documents + decrement copies
            # Issues table insert new field
            # Increment Members # of issues SELECT Member number of issues, +1 and then update
            pass

        def returnDocument(self, doctype, id):
            # delete from issues table
            # increment copy count
            # decrement user's no of issues
            pass