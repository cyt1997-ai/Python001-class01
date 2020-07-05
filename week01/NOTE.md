## 爬取数据

urllib，requests



## 解析数据

Beautifulsoup、xpath

```
pip  install  bs4

pip  install  lxml
```



## requestments.txt

pip install -r requestments.txt

```
requirements.txt的生成方法有两个：freeze命令和pipreqs，它们的区别是：Freeze 生成 Python环境下的所有类库到requirments.txt,而pipreqs只生成当前项目下中用到的类库。用法为：

pip freeze > requirments.txt    

或

pip install pipreqs (已安装pipreqs的省略这步)

pipreqs  path
# 使用步骤在项目根目录下执行命令
pipreqs ./  # 报错就执行下面这条
pipreqs ./ --encoding=utf-8
```



## 前端基础

**1、http和浏览器之间的关系**

http传输网页源代码，浏览器负责解析获取源代码并HTML源代码解析成平时看到的样子，爬虫就是使用第三方库模拟浏览器获取源代码的这一过程。



**2、http请求与返回头部**

user-Aget



**3、请求方式**

get、post、delete、head、put



**4、状态码**

1xx  信息响应

2xx  成功响应

3xx  重定向

4xx  客户端问题

5xx  服务端问题



**5、html 常用的标签和属性**

文字 span

链接  a

图片  img



## Scrapy框架

![在这里插入图片描述](https://img-blog.csdnimg.cn/20200705215149303.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2N5dDA5MDY=,size_16,color_FFFFFF,t_70)
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200705215156313.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2N5dDA5MDY=,size_16,color_FFFFFF,t_70)
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200705215209613.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2N5dDA5MDY=,size_16,color_FFFFFF,t_70)

**安装**

```
pip  install  scrapy
```



**创建项目** 

```
scrapy  startproject  （项目名）
###############
cd spiders
scrapy  genspider (爬虫的名字)  （爬取的域名）
```

> 此项注意，爬虫的名字后续用于启动爬虫，同时会初始化配置文件，配置文件中会有很多地方引用这个名字。



**settings.py 配置文件**

```
USER_AGENT = 'maoyan (+http://www.yourdomain.com)'  # 模拟浏览器
DOWNLOAD_DELAY = 1      #控制节奏
```



**爬虫文件**

```
name : 爬虫运行时指定的名字
allowed-domains :  限制爬取的域名
start_urls :  第一次向谁发起请求（启动Twised异步框架，获取头部信息）
def parse(self,response): #response 向start_urls发起请求的返回信息
```



movies.py

```python
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

```

> 爬虫运行时首先会向start_urls配置项指定的url发起请求，获取返回信息，然后运行parse解析主网页，并获取详情页的url，最后回调parse2解析详情页。在最后利用item把返回信息解耦，pipelines.py进行输出。

> 默认 parse 从 start_urls 获取response ，可以定义start_requests函数，编写前置逻辑，它会在爬虫启动时运行，也在parse之前。

> #选择器
>
> from scrapy.selector import Selector



items.py

```python
# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class MaoyanItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    #pass
    
	#固定格式
    name_page = scrapy.Field()
    type_page = scrapy.Field()
    time_page = scrapy.Field()

```



pipelines.py

```
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

class MaoyanPipeline:
    def process_item(self, item, spider):
        return item

```

> 在这里可以定义数据的输出方式，比如存入文本，但是结尾必须要有return item



运行爬虫

```
scrapy  crawl  爬虫的名字
```



