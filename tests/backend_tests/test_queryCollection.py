import unittest
from unittest.mock import MagicMock, patch
from datetime import datetime, timedelta
from query_collection import QueryCollection

from util.dataVault import DataVault


class TestQueryCollection(unittest.TestCase):

    @patch('query_collection.mysql.connector.connect')
    def test_connectDB(self, mock_connect):
        mock_db = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = (mock_db, mock_cursor)
        QueryCollection.connectDB(QueryCollection)
        mock_connect.assert_called_once_with(
            user='external_user',
            password='mock_password',
            host='103.90.163.100',
            port=3306
        )
        mock_cursor.assert_called_once()
        mock_db.close.assert_not_called()

    @patch('query_collection.logger')
    @patch('query_collection.mysql.connector.connect')
    def test_connectDB_exception(self, mock_connect, mock_logger):
        mock_connect.side_effect = Exception()
        with self.assertRaises(SystemExit):
            QueryCollection.connectDB(QueryCollection)
        mock_logger.error.assert_called_once()

    def test_getDocCount(self):
        # TODO: test getDocCount function
        pass

    @patch('query_collection.mysql.connector.connect')
    def test_getIssuebyDocId(self, mock_connect):
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = ('mock_issue',)
        mock_connect.return_value = (MagicMock(), mock_cursor)
        result = QueryCollection.getIssuebyDocId(QueryCollection, 'mock_doc_id')
        mock_cursor.execute.assert_called_once_with(
            "SELECT * FROM Issues WHERE Doc_Id='mock_doc_id'"
        )
        self.assertEqual(result, 'mock_issue')

    @patch('query_collection.logger')
    @patch('query_collection.mysql.connector.connect')
    def test_getIssuebyDocId_exception(self, mock_connect, mock_logger):
        mock_connect.side_effect = Exception()
        with self.assertRaises(SystemExit):
            QueryCollection.getIssuebyDocId(QueryCollection, 'mock_doc_id')
        mock_logger.error.assert_called_once()

    @patch('query_collection.mysql.connector.connect')
    def test_alterCopyCount(self, mock_connect):
        mock_cursor = MagicMock()
        mock_cursor.rowcount = 1
        mock_connect.return_value = (MagicMock(), mock_cursor)
        QueryCollection.alterCopyCount(QueryCollection, 5, 'Documents', 'mock_doc_id')
        mock_cursor.execute.assert_called_once_with(
            "UPDATE Documents SET Copies = 5, Member_Id=1 WHERE doc_id = mock_doc_id;"
        )
        mock_cursor.connection.commit.assert_called_once()
        mock_cursor.connection.close.assert_called_once()
        mock_cursor.connection.rollback.assert_not_called()

    @patch('query_collection.logger')
    @patch('query_collection.mysql.connector.connect')
    def test_alterCopyCount_exception(self, mock_connect, mock_logger):
        mock_connect.side_effect = Exception()
        with self.assertRaises(SystemExit):
            QueryCollection.alterCopyCount(QueryCollection, 5, 'Documents', 'mock_doc_id')
        mock_logger.error.assert_called_once()
