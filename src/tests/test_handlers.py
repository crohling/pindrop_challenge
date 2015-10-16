import unittest
import mock
import json
from handlers import PhoneHandler
from tornado.testing import AsyncHTTPTestCase
from tornado.web import Application

class PhoneHandlerTest(AsyncHTTPTestCase):
    def get_app(self):
        self.db = [{
                        "area_code": "111",
                        "phone_number": "1112223333",
                        "body": "testing body",
                        "comment_count": "1"
                    }]
        self.app = Application([('/(phone_number/([0-9]{10})?|area_code/([0-9]{3})?)', PhoneHandler,
                    dict(number_database=self.db))])
        return self.app

    def test_good_area_code(self):
        response = self.fetch("/area_code/111", method='GET')
        self.assertEqual(response.body, json.dumps(self.db))
        self.assertEqual(response.code, 200)

    def test_good_area_code_all(self):
        response = self.fetch("/area_code/", method='GET')
        self.assertEqual(response.body, json.dumps(self.db))
        self.assertEqual(response.code, 200)

    def test_good_phone_number(self):
        response = self.fetch("/phone_number/1112223333", method='GET')
        self.assertEqual(response.body, json.dumps(self.db))
        self.assertEqual(response.code, 200)

    def test_good_phone_number_all(self):
        response = self.fetch("/phone_number/", method='GET')
        self.assertEqual(response.body, json.dumps(self.db))
        self.assertEqual(response.code, 200)

    def test_bad_area_code(self):
        response = self.fetch("/area_code/1112", method='GET')
        self.assertEqual(response.code, 404)

    def test_bad_phone_number(self):
        response = self.fetch("/phone_number/1112", method='GET')
        self.assertEqual(response.code, 404)

    def test_bad_everything(self):
        response = self.fetch("/adsf134", method='GET')
        self.assertEqual(response.code, 404)
