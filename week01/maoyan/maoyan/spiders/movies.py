# -*- coding: utf-8 -*-
import scrapy
from lxml import etree
from scrapy.selector import Selector
from maoyan.items import MaoyanItem


class MoviesSpider(scrapy.Spider):
    name = 'maoyan'
    allowed_domains = ['maoyan.com']
    start_urls = ['https://maoyan.com/films?showType=3']

    def parse(self, response):
        # tree = Selector(response=response)
        tree = etree.HTML(response.text)
        #解析主页面
        link = tree.xpath('//*[@class="channel-detail movie-item-title"]/a')
       # items = []
        for i in range(0, 10):  # 取前10个电影信息
            item = MaoyanItem()
            # 获取详情页地址
            page_url = "https://maoyan.com" + link[i].attrib['href']
            # item['page_url'] = page_url
            # items.append(item)
        # return items
            yield scrapy.Request(url=page_url, callback=self.parse2)

    def parse2(self, response):
        # tree = Selector(response=response)
        tree = etree.HTML(response.text)
        # 获取详情页内容
        page_tree = tree.xpath('//*[@class="movie-brief-container"]')

        # 名称
        name_page = page_tree[0].xpath('h1')[0].text

        # 类型
        type_page = page_tree[0].xpath('ul/li[1]/a')[0].text



        # 时间
        time_page = page_tree[0].xpath('ul/li[3]')[0].text

        item = MaoyanItem()
        item['name_page'] = name_page
        item['type_page'] = type_page
        item['time_page'] = time_page

        yield item
