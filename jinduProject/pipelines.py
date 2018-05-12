# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import sqlite3

class JinduprojectPipeline(object):
    def process_item(self, item, spider):
        return item
class UrlsPipeline(object):
    def process_item(self, item, spider):
        if spider.name=='jindu_url' or spider.name=='update_jindu':
            self.open_sql()
            self.store_urls(item)
            self.con.commit()
            self.close_sql()
        return item
    def store_urls(self,item):
        self.cur.execute("insert into urls (url,flag,error) values(?,?,?)",(item['url'],item['flag'],item['error']))
        self.con.commit()
    def open_sql(self):
        self.con = sqlite3.connect('/home/zuofeng/jindu.db')
        self.cur = self.con.cursor()
    def close_sql(self):
        self.con.close()
class ContentsPipeline(object):
    def process_item(self, item, spider):
        if spider.name=='jindu_content':
            self.open_sql()
            self.store_urls(item)
            self.con.commit()
            self.close_sql()
        return item
    def store_urls(self,item):
        self.cur.execute("update urls set content=? where url=?",(item['content'],item['url']))
        self.con.commit()
    def open_sql(self):
        self.con = sqlite3.connect('/home/zuofeng/jindu.db')
        self.cur = self.con.cursor()
    def close_sql(self):
        self.con.close()