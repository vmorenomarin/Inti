"""
Application author details.

author="Colav",
author_email="colav@udea.edu.co".
"""

import unittest
import json
from pymongo import MongoClient
from inti.SCIELO.ScieloRequest import ScieloRequest


class TestScieloRequest(unittest.TestCase):
    """Testing class."""

    def setUp(self):
        """Test setup."""
        self.scielorequest = ScieloRequest(db='scielo', host=None)

    # def test__scielorequest_initialization(self):
    #     """Test class initialization."""
    #     self.assertEqual(self.scielorequest.db, 'scielo')
    #     self.assertEqual(self.scielorequest.host, None)

    def test__get_collections(self):
        """Test get_collections method."""
        collections = ''
        f = open('tests/collections.json')
        collections = json.load(f)
        self.assertNotEqual(collections, '')
        self.scielorequest.get_collections()

        self.client = MongoClient()
        self.db = self.client['scielo']
        s_cols = self.db['collections'].find()

        for col, s_col in zip(collections, s_cols):
            for key in col.keys():
                self.assertEqual(col[key], s_col[key])

    def test__get_journals(self):
        """Test get_journals method."""
        journals = ''
        f = open('tests/journals.json')
        journals = json.load(f)
        self.assertNotEqual(journals, '')
        self.scielorequest.get_journals()

        self.client = MongoClient()
        self.db = self.client['scielo']
        s_jrls = self.db['journals'].find()

        for jrl, s_jrl in zip(journals, s_jrls):
            for key in jrl.keys():
                self.assertEqual(jrl[key], s_jrl[key])


if __name__ == '__main__':
    unittest.main()
