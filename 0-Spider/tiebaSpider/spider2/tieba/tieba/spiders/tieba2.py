# coding: utf-8

import scrapy
import time
from scrapy.http.request import Request
from scrapy.http import HtmlResponse

class TiebaSpider2(scrapy.Spider):

    name = 'tieba2'

    def __init__(self):
        self.urls = []

        # 加载贴吧名
        fr = open("data/%s_all_href.txt" % time.strftime('%Y%m%d'), "r")

        for one in fr.readlines():
            self.urls.append(one.strip())
        fr.close()

    def start_requests(self):
        urls = self.urls

        for one in urls:
            yield scrapy.Request(url=one, callback=self.parse)
    
    def parse_uname(self, response):
        # response = HtmlResponse(url=page_url.url)
        sel = scrapy.Selector(response)
        name_list = sel.xpath('//li[re:test(@class, "d_name")]//a/text()').extract()
        # print respons        
        fw = open("data/%s_all_name.txt" % time.strftime('%Y%m%d'), "a")
        for name in list(set(name_list)):
            fw.write(name.encode("utf-8"))
            fw.write("\n")
        fw.close()
    
    def parse(self, response):
        sel = scrapy.Selector(response)

        # 可能有些帖子被删除
        try:
            # 得到每个帖子有多少页
            num = int(sel.xpath('//span[re:test(@class,"red")]//text()').extract()[1])   
            # 遍历每页获得用户名
            for page_num in range(1, num + 1):
                one_url = response.url + "?pn=" + str(page_num)

                yield Request(url=one_url, callback=self.parse_uname) 
        except Exception as e:
            pass
        
        

    
