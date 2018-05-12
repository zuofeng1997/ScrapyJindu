# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractor import LinkExtractor
import re
import json
from ..items import UrlItem
class JinduSpider(scrapy.Spider):
    name = 'jindu_url'
    # allowed_domains = ['nncc626.com']
    def start_requests(self):
        urls = [
            'http://www.nncc626.com/',
            'http://www.nncc626.com/tj.htm'
        ]
        yield scrapy.Request(urls[0],callback=self.parse)
        yield scrapy.Request(urls[1],callback=self.parse_index)

    def parse(self, response):
        link = LinkExtractor(allow=r'http://www.nncc626.com/[a-z]{1,}(.htm)',deny=r'index')
        links = link.extract_links(response)
        for link in links:
            yield scrapy.Request(link.url,callback=self.parse_index)

    def parse_index(self,response):
        link = LinkExtractor(allow=r'2015/ssy/[a-z]{1,}(.htm)')
        links = link.extract_links(response)
        for link in links:
            yield scrapy.Request(link.url, callback=self.parse_category)
    def parse_category(self,response):
        script = response.xpath('//script/text()').extract_first()
        nid = re.search('[0-9]{8}',script).group()
        for i in range(12):
            url = "http://qc.wa.news.cn/nodeart/list?nid="+str(nid)+"&pgnum="+str(i+1)+"&cnt=100&attr=&tp=1&orderby=0"
            yield scrapy.Request(url,callback=self.parse_json)
    def parse_json(self,response):
        data = json.loads(response.body.decode('utf-8').replace('(','').replace(')',''))
        if data['status']=='-1':
            pass
        else:
            list_data = data['data']['list']
            for i in list_data:
                item  = UrlItem()
                for i in list_data:
                    item['url'] = i['LinkUrl'] #记录链接
                    item['flag'] = 0   #记录是否爬取完成
                    item['error'] = 0  #记录链接是否异常
                    yield item

