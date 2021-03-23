# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class SicEduZcwjItem(scrapy.Item):
    source_web = scrapy.Field()
    classification = scrapy.Field()
    file_url = scrapy.Field()
    title = scrapy.Field()
    release_time = scrapy.Field()
    source = scrapy.Field()
    content = scrapy.Field()

    """
        一级网站(overview):
            source_web	    这条数据（通知）的来源网站，如：四川省教育厅
            classification	这条数据（通知）的类别，如：政策文件
            file_url		这条数据（通知）的二级页面的地址（URL）
        二级网站(detail):
            title			这条数据（通知）的标题
            release_time	这条数据（通知）的发布时间
            source			这条数据（通知）的来源，如：教育部、四川省教育厅
            content		    这条数据（通知）的正文源代码
    """
