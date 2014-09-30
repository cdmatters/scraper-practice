# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


import sqlite3


class SocrataPipeline(object):

    def __init__(self):
        self.conn = sqlite3.connect('project.db')
        self.cur = self.conn.cursor()

            


    def process_item(self, item, spider):
        self.cur.execute("INSERT into data (title, url, views)\
            VALUES(?,?,?)", (item['title'][0], item['url'][0],
            item['views'][0]))
        self.conn.commit()
        return item
