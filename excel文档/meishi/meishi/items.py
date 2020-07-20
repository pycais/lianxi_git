# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class MeishiItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    big_title = scrapy.Field()
    little_title = scrapy.Field()
    title = scrapy.Field()
    comment = scrapy.Field()
    level1_href = scrapy.Field()
    href = scrapy.Field()
