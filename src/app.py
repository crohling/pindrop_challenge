import time
import tornado.ioloop
import tornado.web
import json
import itertools
# I would normally use the requests library instead of urllib2
import urllib2
import argparse
from handlers import PhoneHandler
from parsing import parse_page

def get_data(args):
    content = None
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
    return content

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Serve an API to 800notes front page data')
    parser.add_argument('--file', type=argparse.FileType('r'))
    args = parser.parse_args()
    content = get_data(args)
    results = parse_page(content)
    application = tornado.web.Application([
        (r"/(phone_number/([0-9]{10})?|area_code/([0-9]{3})?)", PhoneHandler, dict(number_database=results)),
    ])
    application.listen(8000)
    tornado.ioloop.IOLoop.current().start()
