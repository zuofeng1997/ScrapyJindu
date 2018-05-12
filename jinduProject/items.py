# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class JinduprojectItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass
class UrlItem(scrapy.Item):
    url = scrapy.Field()
    flag = scrapy.Field()
    error = scrapy.Field()

class ContentItem(scrapy.Item):
    url = scrapy.Field()
    content = scrapy.Field()
class UpdatedUrlIten(scrapy.Item):
    url = scrapy.Field()
    flag = scrapy.Field()

