import datetime
import traceback

import mysql.connector

import config.data
from config import dbconfig, dbconfig as dbcfg
import sys
import logging

logger = logging.getLogger()
mem_id = None
mydb = mysql.connector.connect(host="103.90.163.100", user="root", password=config.data.password, )
mycursor = mydb.cursor(buffered=True)


class App:
    def __init__(self):
        self.mydb = None
        self.mycursor = None
        self.password = config.data.password
        self.member_id = None

    def setMemberId(self, id):
        global mem_id
        mem_id = id

    def getMemberId(self):
        global mem_id
        return mem_id

    def populate(self):
        try:
            # create librarian db if it doesn't exist
            global mydb
            global mycursor
            self.mydb = mydb
            self.mycursor = mycursor

            try:
                self.mycursor.execute("SHOW DATABASES")
                dblist = []
                for db in self.mycursor:
                    dblist.append(db)
                logger.info("Currently we have databases: " + str(dblist))
                if not ('Librarian',) in dblist:
                    self.mycursor.execute("CREATE DATABASE Librarian")
                self.createTables()
            except Exception as e:
                logger.error("Error in creating cursor: " + str(e) + traceback.format_exc())
                sys.exit(-1)
        except Exception as e:
            logger.error("Error in populate: " + str(e) + traceback.format_exc())
            sys.exit(-1)

    def createTables(self):
        # if table does not exist, create it
        creates = dbcfg.createtable
        tables = config.data.tables
        for k, v in creates.items():
            try:
                self.mycursor.execute("USE Librarian")
                self.mycursor.execute(v)
            except Exception as e:
                logger.error("Error in createTables: " + str(e) + traceback.format_exc())
                sys.exit(-2)

    def validateLogin(self, id):
        sql = dbcfg.sql['memberlogin'].replace('{_id}', str(id))
        try:
            self.mycursor.execute(sql)
            self.mycursor.fetchall()
            self.setMemberId(id)
            logger.info("Validation SQL: " + sql)
            logger.info("Found " + str(self.mycursor.rowcount) + " rows")
            return True
        except Exception as e:
            logger.error("Validate Error" + str(e) + traceback.format_exc())
            return False

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
            global mycursor
            self.cursor = mycursor

        def searchDocument(self, params):
            type = "Books"
            sql = dbcfg.sql['searchDocs'].replace("{_tbl}", type)

            for i, (k, v) in enumerate(params.items()):
                if len(v) == 0:
                    continue
                if k == "Publication_Date":
                    vals = v.split('-')
                    date = datetime.datetime(int(vals[0]), int(vals[1]), int(vals[2]))
                    sql += k + " = " + str(date)
                if k == "Authors" or k == "Keywords" or k == "Contributors":
                        sql += k + " LIKE " + "'%" + v + "%'"

                # title
                else:
                    sql += k + " = " + '"' + v + '"'

                if i < len(list(params.values())) - 1:
                    sql += " AND "



            try:
                logger.info("searchDocument SQL: " + sql)
                self.cursor.execute(sql)
                self.cursor.fetchall()
                if self.cursor.rowcount == 0:
                    return ""
                names = ""
                for r in self.cursor._rows:
                    names += r[2] + ','
                return names[:-1]

            except Exception as e:
                logger.error("searchDocument Error: " + str(e) + traceback.format_exc())
                sys.exit(-1)

        def getRecords(self, name, type):
            name = '"' + name + '"'
            if type == "Books":
                sql = "SELECT * FROM Librarian.{_tbl} where Book_Title = {_title}".replace("{_tbl}", type).replace(
                    "{_title}", name)

            elif type == "Magazines":
                sql = "SELECT * FROM Librarian.{_tbl} where Title = {_title}".replace("{_tbl}", type).replace(
                    "{_title}", name)

            else:
                sql = "SELECT * FROM Librarian.{_tbl} where Book_Title = {_title}".replace("{_tbl}", type).replace(
                    "{_title}", name)

            logger.info("getRecords SQL: " + sql)
            self.cursor.execute(sql)
            self.cursor.fetchall()
            data = self.cursor._rows[0]
            logger.info("getRecords Data: " + str(data))
            return data

        def borrowDocument(self, doctype, id):

            # if copies > 0 documents + decrement copies
            sql = dbcfg.sql.getDocDetails.replace('{_tbl}', doctype)

            try:
                self.mycursor.execute(sql)
                rows = self.mycursor.fetchall()
                for r in rows:
                    pass

            except Exception as e:
                logger.error("Error in getting document details: " + str(e) + traceback.format_exc())
                sys.exit(-1)

            # Issues table insert new field
            # Increment Members # of issues SELECT Member number of issues, +1 and then update

            pass

        def returnDocument(self, doctype, id):
            # delete from issues table
            # increment copy count
            # decrement user's no of issues
            pass
