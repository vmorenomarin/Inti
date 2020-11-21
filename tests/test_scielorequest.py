import unittest
import json
from inti.SCIELO.scielorequest import ScieloRequest
from pymongo import MongoClient


class TestScieloRequest(unittest.TestCase):
    """Testing class."""

    def setUp(self):
        self.scielorequest = self.ScieloRequest(db='scielo', host=None)

    def test__scielorequest_initialization(self):
        self.assertEqual(self.scielorequest.db, 'scielo')
        self.assertEqual(self.scielorequest.host, None)

    def test__get_collections(self):
        """Test get_collections method."""

        collections = ''
        f = open('tests/collections.json')
        collections = json.load(f)
        self.assertNotEqual(collections, '')
        s_cols = self.scielorequest.get_collections()

        for col, s_col in zip(collections, s_cols):
            for key in col.keys():
                self.assertEqual(col[key], s_col[key])

    def test__get_journals(self):
        """Test get_journals method."""

        journals = ''
        f = open('tests/journals.json')
        journals = json.load(f)
        self.assertNotEqual(journals, '')
        s_jrls = self.scielorequest.get_journals()

        for jrl, s_jrl in zip(journals, s_jrls):
            for key in jrl.keys():
                self.assertEqual(jrl[key], s_jrl[key])

    # def dl_limiter(n_articles=5):
    #     """Limits the downloaded articles to test.""""

    # def test__get_articles(self):
    #     """Test get_articles method.""""

    #     stage = ''
    #     f = open('tests/stage.json')
    #     self.assertListEqual()

if __name__ == '__main__':
    unittest.main()
