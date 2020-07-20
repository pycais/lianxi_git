# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from itemadapter import ItemAdapter
import pymysql


class MeishiPipeline(object):
    # def process_item(self, item, spider):
    #     return item

    def open_spider(self, spider):
        self.connect = pymysql.connect(host='150.158.123.234', user='qiaofeng', password="1025", database='test',
                                       port=3306, charset='utf8')
        self.cursor = self.connect.cursor()

    def close_spider(self, spider):
        self.connect.commit()
        self.cursor.close()
        self.connect.close()

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        big_title = adapter.get('big_title')
        little_title = adapter.get('little_title')
        title = adapter.get('title')
        comment = adapter.get('comment')
        sql = f"insert into shiwu (`big_title`, `little_title`, `title`, `comment`) values('{big_title}', '{little_title}', '{title}', '{comment}')"
        print(sql)
        try:
            self.cursor.execute(sql)
        except Exception as e:
            with open('./er.txt', 'a+', encoding='utf-8') as f:
                f.writelines(e)
            self.connect.rollback()
        return item
