# -*- coding: utf-8 -*-
import scrapy
from ..items import ContentItem
import sqlite3
import logging
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError, TCPTimedOutError

class JinduSpider(scrapy.Spider):
    name = 'jindu_content'
    allowed_domains = ['nncc626.com']

    def start_requests(self):
        con = sqlite3.connect('/home/zuofeng/jindu.db')
        cur = con.cursor()
        cur.execute("select * from urls")
        r = cur.fetchall()
        for url in r:
            if url[1] == 0:
                yield scrapy.Request(url=url[0], callback=self.parse,errback=self.error_handler)
        con.close()
        # 将flag=0的url放进start_url

    def parse(self, response):
        self.logger.info("页面的地址" + response.url)
        item = ContentItem()
        item['url'] = response.url
        item['content'] = response.body
        yield item

        con = sqlite3.connect('/home/zuofeng/jindu.db')
        cur = con.cursor()
        url = response.url
        cur.execute("update urls set flag=1 where url=%s" % "'" + url + "'")

        con.commit()
        con.close()
        ##爬取过的url，将flag设为1
    def error_handler(self, failure):  #记录异常
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
            url = response.url
            logger.error('HttpError on %s,status:%d' % (url, response.status))

        elif failure.check(DNSLookupError):
            # this is the original request
            request = failure.request
            url = request.url
            logger.error('DNSLookupError on %s', url)

        elif failure.check(TimeoutError, TCPTimedOutError):
            request = failure.request
            url = request.url
            logger.error('TimeoutError on %s', url)

        con = sqlite3.connect('/home/zuofeng/jindu.db')
        cur = con.cursor()

        result = cur.execute("select error from urls where url=%s" % "'" + url + "'")
        for i in result:
            error_code=i[0]

        cur.execute("update urls set error=? where url=?",(error_code+1,url))

        con.commit()
        con.close()
