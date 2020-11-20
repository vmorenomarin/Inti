import unittest
from inti.SCIELO.scielorequest import scielorequest 

class TestScieloRequest(unittest.TestCase):
    """
    Testing class.
    """
    
    def setUp(self):
        self.scielorequest=self.ScieloRequest(db='scielo', host=None)

   """  def test_default_greeting_set(self):
        self.assertEqual("Hello world!", 'Hello world!')
        self.assertEqual() """

    def test__scielorequest_initialization(self):
        self.assertEqual(self.scielorequest.db, 'scielo')
        self.assertEqual(self.scielorequest.host, None)

    def test__get_collections(self):
        """Test get_collections method.""""

        collections = ''
        with open('tests/collections.josn' as f:
            collections = f.read()
            f.close()
        self.assertNotEqual(collections, '')
        scl = self.scielorequest.get_collections()

        for col,scol in zip(collections,scl):
            self.assertEqual(col,scol)

if __name__ == '__main__':
    unittest.main()
