# -*- coding: utf-8 -*-
from copy import deepcopy

import scrapy


class ShiwuSpider(scrapy.Spider):
    name = 'shiwu'
    allowed_domains = ['meishij.net']
    start_urls = ['https://meishij.net']

    def parse(self, response):
        divs = response.xpath('//*[@id="main_nav"]/li[2]/div/div')
        print(len(divs))
        for div in divs:
            item = {}
            item['big_title'] = div.xpath("./div/dl/dt/a/text()").extract_first()
            dds = div.xpath("./div/dl/dd")
            for dd in dds:
                item['little_title'] = dd.xpath('./a/text()').extract_first()
                item['level1_href'] = dd.xpath('./a/@href').extract_first()
                if item['level1_href'] is not None:
                    yield scrapy.Request(
                        item['level1_href'],
                        callback=self.page_parse,
                        meta={'item': deepcopy(item)}
                    )

    def page_parse(self, response):
        item = deepcopy(response.meta['item'])
        divs = response.xpath("//div[@class='listtyle1_list clearfix']/div")
        for div in divs:
            item['title'] = div.xpath("./a/@title").extract_first()
            item['href'] = div.xpath("./a/@href").extract_first()
            if item['href'] is not None:
                yield scrapy.Request(
                    item['href'],
                    callback=self.detail,
                    meta={'item': deepcopy(item)}
                )
        next_page = response.xpath("//a[@class='next']/@href").extract_first()
        if next_page is not None:
            yield scrapy.Request(
                next_page,
                callback=self.page_parse,
                meta={'item': response.meta['item']}
            )

    def detail(self, response):
        item = response.meta['item']
        divs = response.xpath("//div[@class='editnew edit']/div")
        q = []
        for div in divs:
            level_2 = div.xpath("./div/p/text()").extract()
            q.extend(level_2)
        item['comment'] = ''.join(q)
        yield item