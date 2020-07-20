# -*- coding: utf-8 -*-
import scrapy
from copy import deepcopy


class ShougongSpider(scrapy.Spider):
    name = 'shougong'
    allowed_domains = ['kiinii.com']
    start_urls = ['https://www.kiinii.com/course/tutorials']

    def parse(self, response):
        lis = response.xpath('//ul[@class="single-wishlist-items"]/li')
        for li in lis:
            item = {}
            item['n'] = 1
            item['title'] =li.xpath('./div/div[1]/a/@title').extract_first()
            href = li.xpath('./div/div[1]/a/@href').extract_first()
            if href:
                item['href'] = "https://www.kiinii.com" + href
                yield scrapy.Request(
                    item['href'],
                    callback=self.detail_page,
                    meta={"item": deepcopy(item)}
                )
        next_page = response.xpath('//*[@id="main_all"]/div[4]/span/following-sibling::a[1]/@href').extract_first()
        if next_page:
            next_page = "https://www.kiinii.com" + next_page
            yield scrapy.Request(
                next_page,
                callback=self.parse,
                dont_filter=True
            )

    def detail_page(self, response):
        item = response.meta['item']
        item['n'] += 1
        labels = response.xpath('//*[@id="main_all"]/div/div[2]/div[1]/div[2]/div[1]/p/text()').extract()
        if not labels:
            labels = response.xpath("//div[@class='blog-content sogoke-text-area mb40']/p/text()").extract()
        item['labels'] = ''.join(labels)
        yield item
