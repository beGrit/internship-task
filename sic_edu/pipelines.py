# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import pymongo
import pymysql
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem


class BasePipeline:

    def open_spider(self, spider):
        pass

    def close_spider(self, spider):
        pass

    def process_spider(self, item, spider):
        pass


class SicEduPipeline:
    def process_item(self, item, spider):
        return item


# 去重
class DuplicatesPipeline:

    def __init__(self):
        self.ids_seen = set()

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        if adapter['index'] in self.ids_seen:
            raise DropItem(f'Duplicates item found:{item!r}')
        else:
            self.ids_seen.add(adapter['index'])
            return item


class MySQLPipeline:
    def __init__(self, config):
        self.config = config

    @classmethod
    def from_settings(cls, settings):
        return cls(settings['MySQLConfiguration'])

    def open_spider(self, spider):
        self.db = pymysql.connect(**self.config)
        self.cursor = self.db.cursor()

    def close_spider(self, spider):
        self.db.close()

    def process_item(self, item, spider):
        pass


class MongoPipeline(BasePipeline):
    db_name = 'SicEdu'
    collection_name = 'scrapy_items'

    def __init__(self, config):
        self.config = config

    @classmethod
    def from_settings(cls, settings):
        return cls(settings['MongoDBConfiguration'])

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(**self.config)
        self.db = self.client[self.db_name]

    def close_spider(self, spider):
        self.client.close()

    def process_spider(self, item, spider):
        self.db[self.collection_name].insert_one(dict(item))
        return item
