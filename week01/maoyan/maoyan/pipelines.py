# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

#在这里可以定义数据的输出方式，比如存入文本，但是结尾必须要有return item
class MaoyanPipeline:
    def process_item(self, item, spider):
        return item
