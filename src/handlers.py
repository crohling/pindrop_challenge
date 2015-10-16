import tornado.web
import json

class PhoneHandler(tornado.web.RequestHandler):
    def initialize(self, number_database):
        self.database = number_database

    def get(self, field_and_value, *args):
        field, value = field_and_value.split("/")
        if value:
            value_document = [doc for doc in self.database if doc.get(field) == value]
            if value_document:
                data = json.dumps(value_document)
            else:
                raise tornado.web.HTTPError(404)
        else:
            data = json.dumps(self.database)
        self.write(data)
        return

