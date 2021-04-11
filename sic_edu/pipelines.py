# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import pymongo
import pymysql
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
import uuid


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
        return cls(settings['MYSQL_CONFIGURATION'])

    def open_spider(self, spider):
        self.db = pymysql.connect(**self.config)
        self.cursor = self.db.cursor()

    def close_spider(self, spider):
        self.db.close()

    def process_item(self, item, spider):
        sql = """
        insert into 
        `job_info_db`
        set 
        id = {id},
        major = {major},
        position_name = {postion_name},
        salary = {salary},
        enterprise_name = {enterprise_name},
        position_description = {position_description},
        welfare = {welfare},
        position_detail_description = {position_detail_description},
        contact_info = {contact_info},
        company_info = {company_info},
        createtime = {createtime},
        modifiedtime = {modifiedtime},
        """
        item_adapter = ItemAdapter(item)
        mysql_item = MySQLItem(**item_adapter.asdict())
        mysql_item_adapter = ItemAdapter(mysql_item)
        sql.format(mysql_item)
        self.cursor.execute(sql)
        return item


class MongoPipeline(BasePipeline):
    db_name = 'SicEdu'
    collection_name = 'scrapy_items'

    def __init__(self, config):
        self.config = config

    @classmethod
    def from_settings(cls, settings):
        return cls(settings['MONGODB_CONFIGURATION'])

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(**self.config)
        self.db = self.client[self.db_name]

    def close_spider(self, spider):
        self.client.close()

    def process_spider(self, item, spider):
        self.db[self.collection_name].insert_one(dict(item))
        return item


class MySQLItem(dict):
    def __init__(self, **kwargs):
        super().__init__()
        self['id'] = uuid.uuid1()
        self['createtime'] = 11111
        self['modifiedtime'] = 12312
        for (k, v) in kwargs.items():
            self[k] = v
