# -*- coding: utf-8 -*-
import scrapy
import logging

from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError, TCPTimedOutError

class JinduSpider(scrapy.Spider):
    name = 'test'

    def start_requests(self):

        urls = "http://www.nncc626.com/2017-03/09/c_12950512dd4.htm"
        yield scrapy.Request(urls,callback=self.parse,errback=self.error_handler)

    def parse(self, response):
        yield {
            'url':response.url
        }
    def error_handler(self, failure):
        logger = logging.getLogger('test')
        hdlr = logging.FileHandler('test.log')
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        hdlr.setFormatter(formatter)
        logger.addHandler(hdlr)
        logger.setLevel(logging.WARNING)


        # logger.error(repr(failure))

        # in case you want to do something special for some errors,
        # you may need the failure's type:

        if failure.check(HttpError):
            # these exceptions come from HttpError spider middleware
            # you can get the non-200 response
            response = failure.value.response
            self.logger.error('HttpError on %s,status:%d'% (response.url,response.status))

        elif failure.check(DNSLookupError):
            # this is the original request
            request = failure.request
            self.logger.error('DNSLookupError on %s', request.url)

        elif failure.check(TimeoutError, TCPTimedOutError):
            request = failure.request
            self.logger.error('TimeoutError on %s', request.url)
