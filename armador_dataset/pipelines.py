# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json, os

class ArmadorDatasetPipeline(object):    
    # articles = {}

    # def open_spider(self, spider):
    #     if(os.path.isfile('items.json')):
    #         self.file = open('items.json', 'r+')
    #         training_data = str(self.file.read())
    #         self.articles = json.loads(training_data)
    #     else:
    #         self.file = open('items.json', 'x')
        

    # def close_spider(self, spider):
    #     #self.file.truncate(0)
    #     self.file = open('items.json', 'w')
    #     self.file.write(json.dumps(self.articles))
    #     self.file.close()

    def process_item(self, item, spider):
        #id_articulo = list(item)[0]
        #self.articles[id_articulo] = item[id_articulo]
        #line = json.dumps(item0)
        #self.file.write(line)
        print('el pipeline de aguera')
        return item
    # def process_item(self, item, spider):
    #     return item
