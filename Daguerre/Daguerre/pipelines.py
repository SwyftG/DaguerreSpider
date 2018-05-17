# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
import logging
from Daguerre.items import DaguerrePostItem


class DaguerrePipeline(object):
    def __init__(self):
        clinet = pymongo.MongoClient("localhost", 27017)
        db = clinet["Daguerre"]
        self.table = db["postTable"]

    def process_item(self, item, spider):
        if isinstance(item, DaguerrePostItem):
            try:
                self.table.insert(dict(item))
            except Exception as e:
                logging.error("PIPLINE EXCEPTION: " + str(e))
        return item
