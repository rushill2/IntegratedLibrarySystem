import traceback
from random import randint

import data.dumps
from config import dbconfig as dbcfg
import sys
import logging

from util.queryCollection import QueryCollection

logger = logging.getLogger()
mem_id = None


class App:
    def __init__(self):
        self.mydb = None
        self.mycursor = None
        self.password = data.dumps.password
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
            mydb, mycursor = QueryCollection.connectDB(QueryCollection)
            try:
                mycursor.execute("SHOW DATABASES")
                dblist = []
                for db in mycursor:
                    dblist.append(db)
                logger.info("Currently we have databases: " + str(dblist))
                if not ('Librarian',) in dblist:
                    mycursor.execute("CREATE DATABASE Librarian")
                    mydb.close()
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
        tables = data.dumps.tables
        for k, v in creates.items():
            try:
                mydb, mycursor = QueryCollection.connectDB(QueryCollection)
                mycursor.execute("USE Librarian")
                mycursor.execute(v)
                mydb.close()
            except Exception as e:
                logger.error("Error in createTables: " + str(e) + traceback.format_exc())
                sys.exit(-2)

    def validateLogin(self, id):
        sql = dbcfg.sql['memberlogin'].replace('{_id}', str(id))
        try:
            mydb, mycursor = QueryCollection.connectDB(QueryCollection)
            mycursor.execute(sql)
            mycursor.fetchall()
            self.setMemberId(id)
            logger.info("Validation SQL: " + sql)
            logger.info("Found " + str(mycursor.rowcount) + " rows")
            mydb.close()
            return True
        except Exception as e:
            logger.error("Validate Error" + str(e) + traceback.format_exc())
            return False

class Librarian:
    def __init__(self):
        self.lib_id = None

    def createStaffAccount(self, data):
        # random 6 digit int as ID
        self.lib_id = ''.join(["{}".format(randint(0, 9)) for num in range(0, 5)])
        data[0] = self.lib_id

        sql = dbcfg.sql['insertStaff']
        try:
            mydb, mycursor = QueryCollection.connectDB(QueryCollection)
            mycursor.execute(sql, data)
            mydb.commit()
            logger.info("Inserted into Staff number of rows: " + str(mycursor.rowcount))
            mydb.close()
        except Exception as e:
            logger.error("Error in insertStaff : " + str(e) + traceback.format_exc())
            sys.exit(-1)


        # def addDocument(self, doctype):
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



