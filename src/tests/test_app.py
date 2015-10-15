import unittest
import mock

class BasicTestCase(unittest.TestCase):
    def setUp(self):
        self.a = 1
        self.b = 2
        self.result = 3

    def test_addition(self):
        self.assertTrue(self.a + self.b == self.result)
