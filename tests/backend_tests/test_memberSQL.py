import unittest
from unittest.mock import MagicMock, patch
from datetime import datetime
from my_module import Member

class TestMember(unittest.TestCase):

    def setUp(self):
        self.member = Member(1, app)

    def test_setSearchResults(self):
        self.member.setSearchResults(['result1', 'result2'])
        self.assertEqual(self.member.getSearchResults(), ['result1', 'result2'])

    def test_searchDocument(self):
        with patch('my_module.QueryCollection.connectDB') as mock_conn:
            mock_cursor = MagicMock()
            mock_conn.return_value = (None, mock_cursor)
            mock_cursor.rowcount = 1
            mock_cursor.fetchall.return_value = [('doc1', 'title1'), ('doc2', 'title2')]

            params = {'Author': 'John', 'Publication_Date': '2022-01-01'}
            doctype = 'Books'
            results = self.member.searchDocument(params, doctype)

            mock_conn.assert_called_once()
            mock_cursor.execute.assert_called_with(
                'SELECT * FROM Librarian.Books where Author LIKE "%John%" AND Publication_Date = 2022-01-01')
            self.assertEqual(results, [('doc1', 'title1'), ('doc2', 'title2')])

    def test_getRecords(self):
        with patch('my_module.QueryCollection.connectDB') as mock_conn:
            mock_cursor = MagicMock()
            mock_conn.return_value = (None, mock_cursor)
            mock_cursor._rows = [('doc1', 'title1'), ('doc2', 'title2')]

            name = 'book1'
            doctype = 'Books'
            data = self.member.getRecords(name, doctype)

            mock_conn.assert_called_once()
            mock_cursor.execute.assert_called_with(
                'SELECT * FROM Librarian.Books where Book_Title = "book1"')
            self.assertEqual(data, ('doc1', 'title1'))

    def test_borrowDocument(self):
        with patch('my_module.QueryCollection.alreadyBorrowed') as mock_borrowed, \
             patch('my_module.QueryCollection.getDocCount') as mock_count, \
             patch('my_module.QueryCollection.alterCopyCount') as mock_alter, \
             patch('my_module.QueryCollection.insertIssue') as mock_issue, \
             patch('my_module.QueryCollection.updateMemberBorrows') as mock_borrows:

            mock_borrowed.return_value = 0
            mock_count.return_value = 2

            doctype = 'Books'
            doc_id = 'doc1'
            book_id = 'book1'
            data = datetime.now()
            mem_id = 1

            result = self.member.borrowDocument(doctype, doc_id, book_id, data, mem_id)

            mock_borrowed.assert_called_once_with(doc_id, mem_id)
            mock_count.assert_called_once_with(doc_id)
            mock_alter.assert_called_once_with(mock_count.return_value - 1, 'Documents', doc_id)
            mock_issue.assert_called_once_with(data, doc_id)
            mock_borrows.assert_called_once_with(doc_id, mem_id, 'borrow')

            self.assertEqual(result, mock_borrows.return_value)

    def test_returnDocument(self):
        with patch('my_module.QueryCollection.deleteIssues') as mock_delete, \
             patch('my_module.QueryCollection.getDocCount') as mock_count, \
             patch('my_module.QueryCollection.updateMemberBorrows') as mock_borrows, \
             patch('my_module.QueryCollection.alterCopyCount') as mock_alter:

            doc_id = 'doc1'
            row = 2

            self.member.returnDocument