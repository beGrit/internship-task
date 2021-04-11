import scrapy
from urllib.parse import urljoin

from itemadapter import ItemAdapter

from sic_edu.items import SicEduZcwjItem


class EduScZcwjSpider(scrapy.Spider):
    name = 'edu_sc_zcwj'
    allowed_domains = ['edu.sc.gov.cn']
    start_urls = ['http://edu.sc.gov.cn/scedu/c100538/xxgk_list.shtml']

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, callback=self.parse, method='GET')

    def parse(self, response, **kwargs):
        root_selector = response.selector
        li_list = root_selector.xpath('//ul[@class="xwzxList"]/li')
        for li in li_list:
            href = li.xpath('./a/@href').get()
            extract_data = {
                'title': li.xpath('./a/@title').get(),
                'classification': DocumentType.POLICY,
                'file_url': urljoin('http://edu.sc.gov.cn/', href)
            }
            item = SicEduZcwjItem()
            item.collect(**extract_data)

            # issue : meta传值 / key_argument传值的区别
            yield scrapy.Request(extract_data['file_url'], callback=self.parse_content, meta={'item': item})

    def parse_content(self, response):
        item = response.meta['item']
        root_selector = response.selector
        detail_div = root_selector.xpath('//div[@class="detail"]')
        data = {
            'source_web': detail_div.xpath('./div[@class="xgxx"]/span[1]/a/text()').get(),
            'release_time': detail_div.xpath('./div[@class="xgxx"]/span[2]/text()').get(),
            'source': detail_div.xpath('./div[@class="xgxx"]/span[3]/text()').get(),
            'content': root_selector.xpath('//div[@class="detail"]/div[@class="content"]/div[@class="cont"]').get(),
        }
        item.collect(**data)
        print(item['title'])
        yield item


from enum import Enum


class DocumentType(Enum):
    POLICY = 'xxgk'
    RESPONSE = 'xwzx'
