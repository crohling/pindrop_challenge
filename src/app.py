#!/usr/bin/env python
import time
import tornado.ioloop
import tornado.web
import json
import itertools
# I would normally use the requests library instead of urllib2
import urllib2
import argparse
import redis
from handlers import PhoneHandler
from parsing import parse_page

def get_data(args):
    """Load data, either from command line entered file, or 800notes.com"""
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

def load_redis(database, results):
    """Load the phone number data results into redis, if applicable"""
    for item in results:
        if not item.get("area_code"):
            raise ValueError("The following record was missing an area_code %s" % item)
        if not item.get("phone_number"):
            raise ValueError("The following record was missing a phone_number %s" % item)
        database.set("area_code|%s" % item.get("area_code"), json.dumps(item))
        database.set("phone_number|%s" % item.get("phone_number"), json.dumps(item))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Serve an API to 800notes front page data')
    parser.add_argument('--file', type=argparse.FileType('r'))
    parser.add_argument('-r', action="store_true")
    args = parser.parse_args()
    content = get_data(args)
    results = parse_page(content)
    if args.r:
        print "Serving data out of redis"
        database = redis.StrictRedis(host='redis', port=6379, db=0)
        load_redis(database, results)
    else:
        print "Serving data out of memory"
        database = results
    application = tornado.web.Application([
        (r"/(phone_number/([0-9]{10})?|area_code/([0-9]{3})?)", PhoneHandler, dict(number_database=database, is_redis=args.r)),
    ])
    application.listen(8000)
    tornado.ioloop.IOLoop.current().start()
