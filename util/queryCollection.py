import sys
import traceback
from datetime import datetime, timedelta
from random import randint
from config import dbconfig as dbcfg
from util.dataVault import DataVault
import logging, mysql.connector

from util.twoFAUtil import TwoFactor
from security.dataSecurity import AESPasswEncryption

# mydb = mysql.connector.connect(host="103.90.163.100", user="root", password=security.dumps.password, autocommit=True)
# mycursor = mydb.cursor(buffered=True)
logger = logging.getLogger()


class QueryCollection:
    # checks if no docs of that id present, else returns count

    def connectDB(self):
        try:
            passw = AESPasswEncryption.decrypt(AESPasswEncryption).decode()
            mydb = mysql.connector.connect(
                    user='external_user',
                    password=passw,
                    host='103.90.163.100',
                    port=3306,
            )
            mycursor = mydb.cursor(buffered=True)
            return mydb, mycursor
        except Exception as e:
            logger.error("Error in connectDB: " + str(e) + traceback.format_exc())
            sys.exit(-1)

    def getDocCount(self, doc_id):
        sql = dbcfg.sql['getDocDetails'].replace('{_id}', str(doc_id))
        logger.info("borrowDocument getDocDetails SQL: " + sql)
        try:
            mydb, mycursor = QueryCollection.connectDB(QueryCollection)
            mycursor.execute(sql)
            try:
                rows = mycursor.fetchall()
                mydb.close()
                if len(rows) > 0:
                    return rows[0][1]

            except Exception as e:
                logger.error("Other error " + str(e) + traceback.format_exc())
                sys.exit(-1)

        except Exception as e:
            logger.error("Error in getting document details: " + str(e) + traceback.format_exc())
            sys.exit(-1)

    # gets from issue table via docid
    def getIssuebyDocId(self, doc_id):
        sql = dbcfg.sql['selectbyId'].replace('{_tbl}', "Issues").replace('{_idtype}', "Doc_Id").replace("{_id}",
                                                                                                         doc_id)
        logger.info("SelectbyId for Issues Doc_id: " + sql)
        try:
            mydb, mycursor = QueryCollection.connectDB(QueryCollection)
            mycursor.execute(sql)
            issuedata = mycursor.fetchone()
            mydb.close()
            return issuedata[0]

        except Exception as e:
            logger.error("Error in issuedata acquisition: " + str(e) + traceback.format_exc())
            sys.exit(-1)
        # Issues table insert new field

    # decrement copies from documents table
    def alterCopyCount(self, copies, table, doc_id):
        sql = dbcfg.sql['update'].replace('{_tbl}', "Documents") + "Copies = " + str(copies) + ', Member_Id=' + str(
            DataVault.mem_id) + " WHERE doc_id = " + str(doc_id) + ';'

        try:
            mydb, mycursor = QueryCollection.connectDB(QueryCollection)
            mycursor.execute(sql)
            mydb.commit()
            mydb.close()
            logger.info("Updated the copies of " + str(mycursor.rowcount) + " rows.")

        except Exception as e:
            logger.error("Error in Decrement Copies for Documents " + str(e) + traceback.format_exc())
            sys.exit(-1)

    def insertIssue(self, choice, doc_id):
        date = datetime.today() + timedelta(days=14)
        returndate = str(date.strftime('%Y-%m-%d'))
        issuedate = str(datetime.today().strftime('%Y-%m-%d'))
        sql = dbcfg.sql['insertIssues'].replace('{_ttl}', '"' + choice[1] + '"').replace('{_date}',
                                                                                         '"' + issuedate + '"').replace(
            '{_due}', '"' + returndate + '"').replace("{_docid}", str(doc_id)).replace('{_memid}',
                                                                                       str(DataVault.mem_id))
        logger.info("Issues SQL Insert: " + sql)
        try:
            mydb, mycursor = QueryCollection.connectDB(QueryCollection)
            mycursor.execute(sql)
            mydb.commit()
            logger.info("Inserted " + str(mycursor.rowcount) + " rows into Issues ")
            mydb.close()
        except Exception as e:
            logger.error("Error in Issues SQL: " + str(e) + traceback.format_exc())
            sys.exit(-1)

        # increments present borrow count and adds to books_borrowed

    def updateMemberBorrows(self, doc_id, mem_id, action):
        # cpde 2 : too many borrows
        # code 3 : mot enough books borrowed
        sql = dbcfg.sql['selectMembers'].replace('{_memid}', str(mem_id))
        issuelist = None
        try:
            mydb, mycursor = QueryCollection.connectDB(QueryCollection)
            mycursor.execute(sql)
            rows = mycursor.fetchall()[0]
            numissues = rows[5]
            issues = rows[4]
            mydb.close()
            if action == 'borrow':
                if numissues + 1 > 5:
                    return 2
                numissues += 1
            else:
                if numissues - 1 < 0:
                    return 3
                numissues -= 1
            if not issues:
                if action == 'borrow':
                    issues = str(doc_id) + ','
                    issuelist = issues
                else:
                    return 3
            else:
                if action == 'borrow':
                    if str(doc_id) in issues.split(','):
                        return 1
                    if len(issues) == 0:
                        issues += str(doc_id) +','
                    else:
                        issues += str(doc_id) + ','
                    issuelist = issues
                else:
                    issuearr = issues.split(',')
                    idx = issuearr.index(str(doc_id))
                    del issuearr[idx]
                    newissues = ','.join(issuearr)
                    if len(newissues) == 0:
                        issuelist = ''

                    elif newissues[-1] == ',':
                        issuelist = newissues[:-1]
                    else:
                        issuelist = newissues

            sql = dbcfg.sql['updateMemberIssues']
            values = [numissues, issuelist, str(mem_id)]
            logger.info('updateMembers SQL; ' + sql)
            try:
                mydb, mycursor = QueryCollection.connectDB(QueryCollection)
                mycursor.execute(sql, values)
                mydb.commit()
                logger.info("Updated copies and books borrowed for member id: " + str(mem_id))
                mydb.close()
            except Exception as e:
                logger.error("Error in updateMembers" + str(e) + traceback.format_exc())
                sys.exit(-1)
        except Exception as e:
            logger.error("Error in selectMembers" + str(e) + traceback.format_exc())
            sys.exit(-1)

    # checks if book already borrowed
    def alreadyBorrowed(self, doc_id, mem_id):
        sql = dbcfg.sql['memberIssued'].replace('{_id}', str(doc_id)).replace('{_memid}', str(mem_id))
        try:
            mydb, mycursor = QueryCollection.connectDB(QueryCollection)
            mycursor.execute(sql)
            rows = mycursor.fetchall()
            mydb.close()
            if len(rows) > 0:
                if len(rows[0]) > 0:
                    return 1


        except Exception as e:
            logger.error("Error in getMemberBorrows: " + str(e) + traceback.format_exc())
            sys.exit(-1)

    def deleteIssues(self, doc_id):
        sql = dbcfg.sql['deleteIssues'].replace('{_id}', str(doc_id))
        try:
            mydb, mycursor = QueryCollection.connectDB(QueryCollection)
            mycursor.execute(sql)
            mydb.commit()
            logger.info("Deleted " + str(mycursor.rowcount) + " rows from Issues with ItemId: " + str(doc_id))
            mydb.close()

        except Exception as e:
            logger.error("Error in returnDocument Member: " + str(e) + traceback.format_exc())
            sys.exit(-1)

    def validateStaff(self, values):
        try:
            mydb, mycursor = QueryCollection.connectDB(QueryCollection)
            sql = dbcfg.sql['loginStaff'].replace('{_login}', values[0]).replace('{_input}', '"'+ values[1] + '"').replace('{_pass}', '"' + values[2] + '"')
            mycursor.execute(sql)
            rows = mycursor.fetchall()
            if len(rows) == 0:
                return None, False, None
            else:
                TwoFactor.Phone = rows[0][4]
                return rows[0][-1], True, rows[0][0]

        except Exception as e:
            logger.error("Error in validateLogin for Staff: " + str(e) + traceback.format_exc())
            sys.exit(-1)

    def update2FABool(self, id, type):
        sql = "UPDATE Librarian." + type + ' SET TwoFA = 1 WHERE Member_Id = ' + str(id) + ';'
        try:
            mydb, mycursor = QueryCollection.connectDB(QueryCollection)
            mycursor.execute(sql)
            mydb.commit()
        except Exception as e:
            logger.error("Error in update 2FA for " + type + str(e) + traceback.format_exc())
            sys.exit(-1)

    def checkEmailExists(self, email, table):
        sql = dbcfg.sql['emailExists'].replace('{_table}', table).replace('{_email}', '"' + email + '"')
        try:
            mydb, mycursor = QueryCollection.connectDB(QueryCollection)
            mycursor.execute(sql)
            rows = mycursor.fetchone()
            if rows:
                return True
            else:
                return False
        except Exception as e:
            logger.error("Error in checkEmailExists " + str(e) + traceback.format_exc())
            sys.exit(-1)

    def updateMemberInfo(self):
        sql = dbcfg.sql['updateMember']
        viewMems = DataVault.pageMap['ViewMembers']
        values = (viewMems.firstname.get(), viewMems.lastname.get(), viewMems.dob.get(), viewMems.phone.get(), viewMems.email.get(), viewMems.memberid)
        try:
            mydb, mycursor = QueryCollection.connectDB(QueryCollection)
            mycursor.execute(sql, values)
            mydb.commit()
            mydb.close()
            logger.info("updateMemberInfo updated : " + str(mycursor.rowcount) + " rows")
        except Exception as e:
            logger.error("Error in updateMemberInfo " + str(e) + traceback.format_exc())
            sys.exit(-1)

    def insertBooks(self, formlabel):
        insertBook = DataVault.pageMap['InsertBook']
        for i,v in enumerate(insertBook.variables):
            insertBook.variables[i] = v.get()
        book_id = ''.join(["{}".format(randint(0, 9)) for num in range(0, 5)])
        doc_id = ''.join(["{}".format(randint(0, 9)) for num in range(0, 5)])
        insertBook.variables.insert(0, doc_id)
        insertBook.variables.insert(0, book_id)
        if any(v is None for v in insertBook.variables):
            return 0
        sql = dbcfg.sql['insertBook']

        try:
            mydb, mycursor = QueryCollection.connectDB(QueryCollection)
            mycursor.execute(sql, insertBook.variables)
            mydb.commit()
            mydb.close()
            return 1
        except Exception as e:
            logger.error("Error in insertBook QueryCollection " + str(e) + traceback.format_exc())
            sys.exit(-1)

    def allBooks(self):
        sql = dbcfg.sql['allBooks']
        try:
            mydb, mycursor = QueryCollection.connectDB(QueryCollection)
            mycursor.execute(sql)
            rows = mycursor.fetchall()
            mydb.close()
            return rows

        except Exception as e:
            logger.error("Error in allBooks QueryCollection " + str(e) + traceback.format_exc())
            sys.exit(-1)

    def issueData(self, doc_id):
        copies = self.getDocCount(QueryCollection, doc_id)
        sql = "SELECT Member_Id from Librarian.Issues WHERE Item_Id =" + str(doc_id) + ';'

        try:
            mydb, mycursor = QueryCollection.connectDB(QueryCollection)
            mycursor.execute(sql)
            rows = mycursor.fetchall()
            mydb.close()
            if len(rows)==0:
                return None, copies
            else:
                return rows[0], copies
        except Exception as e:
            logger.error("Error in issueData QueryCollection " + str(e) + traceback.format_exc())
            sys.exit(-1)
