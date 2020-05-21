import random
import time
import redis
import requests
from lxml import etree

redi = redis.StrictRedis(host='localhost', port=6379, db=1)

count = 1
def proxy(url='https://www.kuaidaili.com/free/inha/1/'):
    global count
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.113 Safari/537.36'
    }
    res = requests.get(url, headers=headers).text
    selector = etree.HTML(res)
    trs = selector.xpath('//tbody/tr')
    for tr in trs:
        ip = tr.xpath("./td[@data-title='IP']/text()")[0]
        port = tr.xpath("./td[@data-title='PORT']/text()")[0]
        print(ip, ':', port)
        ips = "http://{}:{}".format(ip, port)
        ip_vriable = verify_ip(ips)
        if ip_vriable is not None:
            if redi.sadd('verify', ips):
                redi.lpush('proxy', ips)
    count += 1
    if count > 20:
        return 'ok'
    new_url = 'https://www.kuaidaili.com/free/inha/{}/'.format(count)
    time.sleep(random.uniform(2, 4))
    print(count, '-'*40)
    proxy(new_url)


def verify_ip(ips):
    url = 'https://www.bilibili.com/'
    if requests.get(url, headers={'proxies': ips}).status_code == 200:
        return ips
    else:
        return None


if __name__ == '__main__':
    proxy()
