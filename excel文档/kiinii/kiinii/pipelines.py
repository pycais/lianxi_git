# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from itemadapter import ItemAdapter
from openpyxl import Workbook

class KiiniiPipeline(object):
    # def process_item(self, item, spider):
    #     return item
    def open_spider(self, spider):
        self.workbook = Workbook()
        self.sheet = self.workbook.active
        self.sheet.title = '手工'
        self.sheet.append(['序号', '标题', '简介'])

    def close_spider(self, spider):
        self.workbook.save(r'C:\Users\cais\Desktop\aa\生活.xlsx')

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        title = adapter.get('title')
        labels = adapter.get('labels')
        n = adapter.get('n')
        if not labels:
            return item
        self.sheet.append([n, title, labels])
        return item