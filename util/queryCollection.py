import sys
import traceback
from datetime import datetime, timedelta
from config import dbconfig as dbcfg
from pages.member.memberVerification import MemberVerification
import logging, mysql
import data.data

mydb = mysql.connector.connect(host="103.90.163.100", user="root", password=data.data.password, )
mycursor = mydb.cursor(buffered=True)
logger = logging.getLogger()


class QueryCollection:
    # checks if no docs of that id present, else returns count
    def checkZeroDocs(self,doc_id):
        sql = dbcfg.sql['getDocDetails'].replace('{_id}', str(doc_id))
        logger.info("borrowDocument getDocDetails SQL: " + sql)
        try:
            mycursor.execute(sql)
            try:
                rows = mycursor.fetchall()
                if rows[0][1] == 0:
                    return 0
                else:
                    return rows[0][1]
            except Exception as e:
                logger.error("Other error " + str(e) + traceback.format_exc())
                sys.exit(-1)

        except Exception as e:
            logger.error("Error in getting document details: " + str(e) + traceback.format_exc())
            sys.exit(-1)

    # gets from issue table via docid
    def getIssuebyDocId(self,doc_id):
        sql = dbcfg.sql['selectbyId'].replace('{_tbl}', "Issues").replace('{_idtype}', "Doc_Id").replace("{_id}",
                                                                                                         doc_id)
        logger.info("SelectbyId for Issues Doc_id: " + sql)
        try:
            mycursor.execute(sql)
            issuedata = mycursor.fetchone()
            return issuedata[0]

        except Exception as e:
            logger.error("Error in issuedata acquisition: " + str(e) + traceback.format_exc())
            sys.exit(-1)
        # Issues table insert new field

    # decrement copies from documents table
    def alterCopyCount(self, copies, table, doc_id):
        sql = dbcfg.sql['update'].replace('{_tbl}', "Documents") + "Copies = " + str(copies) + " WHERE doc_id = " + str(doc_id) + ';'

        try:
            mycursor.execute(sql)
            mydb.commit()
            logger.info("Updated the copies of " + str(mycursor.rowcount) + " rows.")

        except Exception as e:
            logger.error("Error in Decrement Copies for Documents " + str(e) + traceback.format_exc())
            sys.exit(-1)

    def insertIssue(self, choice, doc_id):
        date = datetime.today() + timedelta(days=14)
        returndate = str(date.strftime('%Y-%m-%d'))
        issuedate = str(datetime.today().strftime('%Y-%m-%d'))
        sql = dbcfg.sql['insertIssues'].replace('{_ttl}','"' + choice[2] + '"').replace('{_date}','"' + issuedate + '"').replace(
            '{_due}', '"' + returndate + '"').replace("{_docid}", str(doc_id)).replace('{_memid}', MemberVerification.mem_id)
        logger.info("Issues SQL Insert: " + sql)
        try:
            mycursor.execute(sql)
            mydb.commit()
            logger.info("Inserted " + str(mycursor.rowcount) + " rows into Issues ")
        except Exception as e:
            logger.error("Error in Issues SQL: " + str(e) + traceback.format_exc())
            sys.exit(-1)

         # increments present borrow count and adds to books_borrowed
    def updateMemberBorrows(self, doc_id, mem_id, action):
        sql = dbcfg.sql['selectMembers'].replace('{_memid}', mem_id)
        try:
            mycursor.execute(sql)
            rows = mycursor.fetchall()[0]
            issuenums = rows[5]
            issues = rows[4]
            if action == 'borrow':
                issuenums += 1
            else:
                issuenums -= 1
            if not issues:
                if action == 'borrow':
                    issues = str(doc_id)
            else:
                if action == 'borrow':
                    if len(issues)==0:
                        issues += str(doc_id)
                    else:
                        issues += ',' + str(doc_id)
                    if str(doc_id) in issues:
                        return 1
                else:
                    issues.replace(',' + str(doc_id), "")

            sql = dbcfg.sql['update'].replace('{_tbl}', "Member").replace("{_idtype}", "Member_Id").replace("{_id}",mem_id)
            sql += "No_of_Borrows = " + str(
                issuenums) + ",  Books_Borrowed = " + '"' + issues + '"' + " WHERE Member_Id = " + mem_id + ';'
            logger.info('updayeMembers SQL; ' + sql)
            try:
                mycursor.execute(sql)
                mydb.commit()
                logger.info("Updated copies and books borrowed for member id: " + str(mem_id))
            except Exception as e:
                logger.error("Error in updateMembers" + str(e) + traceback.format_exc())
                sys.exit(-1)
        except Exception as e:
            logger.error("Error in selectMembers" + str(e) + traceback.format_exc())
            sys.exit(-1)

    # checks if book already borrowed
    def alreadyBorrowed(self, doc_id, mem_id):
        sql = dbcfg.sql['getMemberBorrows'].replace('{_id}', mem_id)
        try:
            mycursor.execute(sql)
            rows = mycursor.fetchall()
            if rows[0][1] > 0:
                if str(doc_id) in rows[0][0]:
                    return 1

        except Exception as e:
            logger.error("Error in getMemberBorrows: " + str(e) + traceback.format_exc())
            sys.exit(-1)

    def deleteIssues(self, doc_id):
        sql = dbcfg.sql['deleteIssues'].replace('{_id}', str(doc_id))
        try:
            mycursor.execute(sql)
            mydb.commit()
            logger.info("Deleted " + str(mycursor.rowcount) + " rows from Issues with ItemId: " + str(doc_id))

        except Exception as e:
            logger.error("Error in returnDocument Member: " + str(e) + traceback.format_exc())
            sys.exit(-1)
