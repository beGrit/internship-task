# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
from dataclasses import dataclass

import scrapy
from itemadapter import ItemAdapter

"""
    一级网站(overview):
        title			这条数据（通知）的标题
        classification	这条数据（通知）的类别，如：政策文件
        file_url		这条数据（通知）的二级页面的地址（URL）
    二级网站(detail):
        source_web	    这条数据（通知）的来源网站，如：四川省教育厅
        release_time	这条数据（通知）的发布时间
        source			这条数据（通知）的来源，如：教育部、四川省教育厅
        content		    这条数据（通知）的正文源代码
"""


class CollectionMixin:
    def collect(self, **kwargs):
        adapter = ItemAdapter(self)
        for (k, v) in kwargs.items():
            adapter[k] = v


class SicEduZcwjItem(scrapy.Item):
    identify = scrapy.Field()
    title = scrapy.Field()
    classification = scrapy.Field()
    file_url = scrapy.Field()
    source_web = scrapy.Field()
    release_time = scrapy.Field()
    source = scrapy.Field()
    content = scrapy.Field()

    def collect(self, **kwargs):
        adaper = ItemAdapter(self)
        try:
            for (key, value) in kwargs.items():
                adaper[key] = value
        except KeyError as e:
            print(e)


class JobInfoItem(scrapy.Item, CollectionMixin):
    """Summary of class here
    Attributes:

    """
    name = scrapy.Field()
    area = scrapy.Field()
    salary = scrapy.Field()
    limit_experience = scrapy.Field()
    limit_education_background = scrapy.Field()
    publish_time = scrapy.Field()
    recruit_num = scrapy.Field()
    job_detail_info = scrapy.Field()


class CompanyInfoItem(scrapy.Item):
    name = scrapy.Field()
    classification = scrapy.Field()


class FiveOneJobInfoItem(scrapy.Item, CollectionMixin):
    id = scrapy.Field()
    major = scrapy.Field()
    position_name = scrapy.Field()
    salary = scrapy.Field()
    company = scrapy.Field()
    description = scrapy.Field()
    education_limit = scrapy.Field()
    num_of_recruit = scrapy.Field()
