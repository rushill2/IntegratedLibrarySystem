import sys
import traceback
from datetime import datetime

from config import dbconfig as dbcfg
from data.dataVault import DataVault
from util.queryCollection import QueryCollection
import logging

logger = logging.getLogger()


class Member:

    def __init__(self, id, app):
        self.mem_id = id
        DataVault.member = self

    def setSearchResults(self, results):
        self.search_results = results

    def getSearchResults(self):
        return self.search_results

    def searchDocument(self, params, doctype):
        sql = dbcfg.sql['searchDocs'].replace("{_tbl}", doctype)

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
            mydb, mycursor = QueryCollection.connectDB(QueryCollection)
            mycursor.execute(sql)
            rows = mycursor.fetchall()
            if mycursor.rowcount == 0:
                return ""
            mydb.close()
            return rows

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
        mydb, mycursor = QueryCollection.connectDB(QueryCollection)
        mycursor.execute(sql)
        mycursor.fetchall()
        data = self.cursor._rows[0]
        logger.info("getRecords Data: " + str(data))
        mydb.close()
        return data

    def borrowDocument(self, doctype, doc_id, book_id, data, mem_id):
        if QueryCollection.alreadyBorrowed(QueryCollection, doc_id, mem_id) == 1:
            return 1
        copies = QueryCollection.getDocCount(QueryCollection, doc_id)
        if copies == 0:
            return 0
        copies -= 1
        QueryCollection.alterCopyCount(QueryCollection, copies, "Documents", doc_id)
        QueryCollection.insertIssue(QueryCollection, data, doc_id)
        return QueryCollection.updateMemberBorrows(QueryCollection, doc_id, mem_id, 'borrow')


    def returnDocument(self, doctype, doc_id , row):
        # delete from issues table
        QueryCollection.deleteIssues(QueryCollection, doc_id)

        # increment copy count in documents
        copies = QueryCollection.getDocCount(QueryCollection, doc_id)
        copies += 1

        # decrement user's no of issues and remove title from string of borrowed books
        QueryCollection.updateMemberBorrows(QueryCollection, doc_id, DataVault.mem_id, 'return')
        QueryCollection.alterCopyCount(QueryCollection, copies, "Documents", doc_id)
        if len(DataVault.borrowbuttons)>0:
            DataVault.borrowbuttons[row - 1]['state'] = 'active'



    def getIssuesbyMemId(self, mem_id):
        sql = dbcfg.sql['getMemberIssues'].replace('{_memid}', str(mem_id))
        logger.info("getIssuesbyMemId sql: " + sql)
        try:
            mydb, mycursor = QueryCollection.connectDB(QueryCollection)
            mycursor.execute(sql)
            rows = mycursor.fetchall()
            mydb.close()
            return rows

        except Exception as e:
            logger.error("Error in getIssuesbyMemId : " + str(e) + traceback.format_exc())

    def deleteMember(self, id):
        sql = dbcfg.sql['deleteMember'].replace('{_memid}', str(id))
        try:
            mydb, mycursor = QueryCollection.connectDB(QueryCollection)
            mycursor.execute(sql)
            mydb.commit()
            mydb.close()
        except Exception as e:
            logger.error("Error in deleteMember : " + str(e) + traceback.format_exc())
            sys.exit(-1)



