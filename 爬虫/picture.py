import os

import requests
from urllib.parse import quote
from lxml import etree
from urllib.parse import urljoin


class PictureBaike(object):
    def __init__(self, tag):
        self.tag = tag
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.113 Safari/537.36'
        }
        self.url = 'https://baike.baidu.com'
        self.start_url = f'https://baike.baidu.com/item/{quote(self.tag)}'

    def parse_page(self, url):
        response = requests.get(url, headers=self.headers).text
        selectors = etree.HTML(response)
        return selectors

    def parse_start_page(self, obj):
        obj.send(None)
        selectors = self.parse_page(self.start_url)
        picture_url = selectors.xpath("//a[@class='more-link']/@href")
        print(picture_url)
        picture_url = picture_url[0]
        picture_selectors = self.parse_page(urljoin(self.url, picture_url))
        divs = picture_selectors.xpath("//div[@id='album-list']/div")
        print(divs)
        for div in divs:
            href = div.xpath("./div[@class='album-pics']/div[@class='pic-list']/a[1]/@href")[0]
            datail_page = self.parse_page(urljoin(self.url, href))
            picture_src = datail_page.xpath("//img[@id='imgPicture']/@src")
            srcs = datail_page.xpath("//div[@class='pic-list']/a/img/@src")
            srcs = [src.replace('h_160', 'h_4096') for src in srcs]
            picture_src.extend(srcs)
            print(picture_src)
            obj.send(picture_src)

    def download_filename(self, title):
        if not os.path.exists(f'{self.tag}'):
            os.mkdir(f'{self.tag}')
        return os.path.join(self.tag, os.path.basename(title + 'jpg'))

    def dowmload_pic(self, url, filename):
        with open(filename, 'wb') as f:
            f.write(requests.get(url, headers=self.headers).content)

    def download(self):
        count = 1
        while True:
            srcs = yield
            for url in srcs:
                filename = self.download_filename(str(count))
                self.dowmload_pic(url, filename)
                count += 1
                print(count)

    def main(self):
        parse = self.download()
        self.parse_start_page(parse)


if __name__ == '__main__':
    PictureBaike('李小璐').main()