import unittest

class MyTestCase(unittest.TestCase):
    def test_default_greeting_set(self):
        self.assertEqual("Hello world!", 'Hello world!')

if __name__ == '__main__':
    unittest.main()