import time
import tornado.ioloop
import tornado.web
import json
import itertools
# I would normally use the requests library here
import urllib2
import argparse
from BeautifulSoup import BeautifulSoup

ROOT_LIST_ITEM_TAG_CLASS = "oos_listItem oos_20plus"
PHONE_NUMBER_TAG_CLASS = "oos_previewTitle"
COMMENT_COUNT_TAG_CLASS = "oos_previewSide"
BODY_TAG_CLASS = "oos_previewBody"

def parse_comment_count(tag):
    for comment_count in tag.findAll("div", {"class": COMMENT_COUNT_TAG_CLASS}):
        comment_count = comment_count.string
        return comment_count    

def parse_phone_number(tag):
    for phone_number in tag.findAll("a", {"class": PHONE_NUMBER_TAG_CLASS}):
        full_number = phone_number.string
        number_parts = full_number.split("-")
        area_code = number_parts[0]
        just_number = ''.join(number_parts[1:])
        return (full_number.replace("-", ""), area_code)

def parse_body_tag(tag):
    for body_tag in tag.findAll("div", {"class": BODY_TAG_CLASS}):
        body = body_tag.contents[0]
        return body
    

def parse_page(content):
    results = []
    soup = BeautifulSoup(content)
    for tag in soup.findAll(lambda tag: tag.name=="li" and ("class", ROOT_LIST_ITEM_TAG_CLASS) in tag.attrs):
        result = {}
        result['phone_number'], result['area_code'] = parse_phone_number(tag)
        result['comment_count'] = parse_comment_count(tag)
        result['body'] = parse_body_tag(tag)
        results.append(result)
    return results

class PhoneHandler(tornado.web.RequestHandler):
    def initialize(self, number_database):
        self.database = number_database

    def get(self, area_code):
        if area_code:
            area_code_document = [doc for doc in self.database if doc.get('area_code') == area_code]
            print area_code_document
            if area_code_document:
                self.write(json.dumps(area_code_document))
                return
            else:
                raise tornado.web.HTTPError(404)
        self.write(json.dumps(self.database))
        return

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Serve an API to 800notes front page data')
    parser.add_argument('--file', type=argparse.FileType('r'))
    args = parser.parse_args()
    content = None
    print args.file
    if args.file:
        print "File passed, reading file from disk"
        content = args.file.read()
    else:
        print "Reading 800notes.com"
        opener = urllib2.build_opener()
        opener.addheaders = [('User-agent', 'Mozilla/5.0')]
        main_page = opener.open('http://800notes.com/')
        content = main_page.read()
    if not content or len(content) < 1:
        raise Exception("Content of page unable to be read")
    results = parse_page(content)
    application = tornado.web.Application([
        (r"/phone_number/([0-9]{3})?", PhoneHandler, dict(number_database=results)),
    ])
    application.listen(8000)
    tornado.ioloop.IOLoop.current().start()
