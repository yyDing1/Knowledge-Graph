import scrapy
from Weapon.items import WeaponItem
import urllib.parse


def clean_str(x):
    ret = ""
    for ch in x:
        if u'\u4e00' <= ch <= u'\u9fff':
            ret += ch
    return ret


def clean_des(x):
    ret = ""
    for ch in x:
        if ch != '\r' and ch != '\t' and ch != '\n':
            ret += ch
    return ret


class WuqibaikeSpider(scrapy.Spider):
    name = 'wuqibaike'
    headers = {
        "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/'
                      '90.0.4430.212 Safari/537.36'
    }
    x = 0
    mp = {}

    def start_requests(self):
        yield scrapy.Request("http://www.wuqibaike.com/index.php?doc-view-13001", headers=self.headers)

    def parse(self, response):
        item = WeaponItem()
        item["名称"] = response.xpath("//article/div[2]//a/text()").extract()[0]
        data = response.xpath("//article/div[4]/div/li")
        cnt = 0
        for line in data:
            try:
                elem = clean_str(line.xpath(".//span[1]/text()").extract()[0][:-1])
                val = line.xpath(".//span[2]/text()").extract()[0]
            except IndexError:
                continue

            if elem == "名称" or elem == "介绍":
                continue

            try:
                item[elem] = val
                cnt += 1
            except KeyError:
                continue

        item["介绍"] = clean_des(response.xpath("//article/div[3]/div[1]/text()").extract()[0])
        try:
            name = response.xpath("//article//strong/text()").extract()[1:]
            link = response.xpath("//article//img/@src").extract()
            item["图片"] = [[name[i], link[i], ""] for i in range(len(name))]
        except IndexError:
            print(-1)

        WuqibaikeSpider.x += 1
        if cnt >= 3:
            yield item
        print(WuqibaikeSpider.x)
        # max: 22171
        if WuqibaikeSpider.x == 1:
            for now_num in range(13002, 22172):
                next_url = "http://www.wuqibaike.com/index.php?doc-view-" + str(now_num)
                yield scrapy.Request(next_url, headers=self.headers)


'''
scrapy crawl wuqibaike -o record.json
scrapy crawl wuqibaike -o record.json
scrapy crawl wuqibaike -o record.json
scrapy crawl wuqibaike -o record.json
scrapy crawl wuqibaike -o record.json
scrapy crawl wuqibaike -o record.json
scrapy crawl wuqibaike -o record.json
'''
# /html/body/section/div/article/div[2]/h1/a
# /html/body/section/div/article/div[3]/div/text()
# /html/body/div[3]/div[3]/div[5]/div[1]/table[2]/tbody/tr[4]/td/a
