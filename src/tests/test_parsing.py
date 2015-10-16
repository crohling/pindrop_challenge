import unittest
import mock
import os
from parsing import parse_page

class BasicTestCase(unittest.TestCase):
    def setUp(self):
        dirname = os.path.dirname(os.path.realpath(__file__))
        print dirname
        with open(os.path.join(dirname, "sample_page.html"), 'r') as file:
            self.contents = file.read()
        
    def test_parse_page(self):
        self.assertTrue(len(parse_page(self.contents)) == 40)

    def test_bad_parse_page(self):
        self.assertTrue(len(parse_page("JIBBERISH")) == 0)
