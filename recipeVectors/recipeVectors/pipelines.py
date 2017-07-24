# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exporters import JsonLinesItemExporter
from scrapy import signals
import json
from scrapy.utils.serialize import ScrapyJSONEncoder
encoder = ScrapyJSONEncoder()

class RecipevectorsPipeline(object):

    def __init__(self):
        self.items = []

    @classmethod
    def from_crawler(cls, crawler):
        pipeline = cls()
        # crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
        crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
        return pipeline

    def spider_closed(self, spider):
        print('ughhh',self.items)
        with open('%s_recipes.json' % spider.name, 'w') as f:
            json.dump(self.items, f)
            f.close()

    def process_item(self, item, spider):
        if item and item['ingredients']:
            # self.exporter.export_item(item)
            self.items.append(dict(item))
        pass
