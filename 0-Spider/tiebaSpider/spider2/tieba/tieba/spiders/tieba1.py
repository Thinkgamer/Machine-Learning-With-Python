# coding: utf-8

import scrapy
import urllib
import time


class TiebaSpider(scrapy.Spider):

    name = 'tieba'

    def __init__(self):
        self.urls = []

        # 加载贴吧名
        fr = open("name.txt", "r")

        for one in fr.readlines():
            for i in range(0, 3):
                self.urls.append('https://tieba.baidu.com/f?kw=' +
                                 urllib.quote(one.strip()) + '&ie=utf-8&pn=' + str(i * 50))
        fr.close()

    def start_requests(self):
        urls = self.urls

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        sel = scrapy.Selector(response)
        ahref_list = sel.xpath(
            '//a[re:test(@class, "j_th_tit ")]//@href').extract()

        fw = open("data/%s_all_href.txt" % time.strftime('%Y%m%d'), "a")
        for ahref in ahref_list:
            href = "https://tieba.baidu.com" + ahref
            fw.write(href + "\n")
        fw.close()
