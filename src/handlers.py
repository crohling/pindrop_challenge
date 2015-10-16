import tornado.web
import json

class PhoneHandler(tornado.web.RequestHandler):
    """A tornado RequestHandler which supports the following REST API calls

    GET /area_code/
    GET /area_code/111
    GET /phone_number/
    GET /phone_number/111222333
    """

    def initialize(self, number_database, is_redis=False):
        """Initialize the PhoneHandler 
        
        Keyword arguments:
        number_database -- Either a list of results, or a redis database to query
        is_redis -- Whether or not the number_database is redis
        """
        self.database = number_database
        self.is_redis = is_redis

    def get(self, field_and_value, *args):
        """The HTTP GET method which returns the queried data from the database"""
        field, value = field_and_value.split("/")
        if value:
            value_document = None
            if self.is_redis:
                value_document = json.loads(self.database.get("%s|%s" % (field, value)))
            else:
                value_document = [doc for doc in self.database if doc.get(field) == value]
            if value_document:
                data = value_document
            else:
                raise tornado.web.HTTPError(404)
        else:
            if self.is_redis:
                data = []
                keys = self.database.keys('*')
                for key in keys:
                    data.append(json.loads(self.database.get(key)))
            else:
                data = self.database
        self.set_header('Content-Type', 'application/json')
        self.write(json.dumps(data))
        return

