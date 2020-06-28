# -*- coding: utf-8 -*-
import scrapy
from lxml import etree
from maoyan.items import MaoyanItem


class MoviesSpider(scrapy.Spider):
    name = 'maoyan'
    allowed_domains = ['maoyan.com']
    start_urls = ['https://maoyan.com/films?showType=3']

    def parse(self, response):
        tree = etree.HTML(response.text)
        #解析主页面
        link = tree.xpath('//*[@class="channel-detail movie-item-title"]/a')
        for i in range(0, 10):  # 取前10个电影信息
            # 获取详情页地址
            page_url = "https://maoyan.com" + link[i].attrib['href']
            yield scrapy.Request(url=link, callback=self.parse2)

    def parse2(self, response):
        tree = etree.HTML(response.text)
        # 获取详情页内容
        page_tree = tree.xpath('//*[@class="movie-brief-container"]')

        # 名称
        name_page = page_tree[0].xpath('h1')[0].text

        # 类型
        type_tree = page_tree[0].xpath('ul/li[1]/a')

        # 遍历 a 标签内容
        type_page = ''

        for i in type_tree:
            tpye_page = i.text

        # 时间
        time_page = page_tree[0].xpath('ul/li[3]')[0].text

        item = MaoyanItem()
        item['name_page'] = name_page
        item['type_page'] = type_tree
        item['time_page'] = type_tree

        yield item
