import unittest
import mock
import app
import json

class RedisTestCase(unittest.TestCase):
    def setUp(self):
        self.fake_results = [{
            "area_code": "111",
            "phone_number": "1112223333",
            "body": "testing body",
            "comment_count": "1"
            }]
        self.no_area_code_results = [{
            "phone_number": "1112223333",
            "body": "testing body",
            "comment_count": "1"
            }]
        self.no_phone_number_results = [{
            "area_code": "111",
            "body": "testing body",
            "comment_count": "1"
            }]

    #@mock.patch.object('app.redis.Redis', "set", autospec=True)
    def test_loading_redis(self):
        mock_redis = mock.Mock()
        app.load_redis(mock_redis, self.fake_results)
        mock_redis.set.assert_called_with("phone_number|%s" % self.fake_results[0].get('phone_number'), json.dumps(self.fake_results[0]))
        self.assertTrue(len(mock_redis.method_calls) == 2)

    def test_no_phone_number_redis(self):
        mock_redis = mock.Mock()
        try:
            app.load_redis(mock_redis, self.no_phone_number_results)
        except ValueError:
            self.assertFalse(mock_redis.called)

    def test_no_area_code_redis(self):
        mock_redis = mock.Mock()
        try:
            app.load_redis(mock_redis, self.no_area_code_results)
        except ValueError:
            self.assertFalse(mock_redis.called)

