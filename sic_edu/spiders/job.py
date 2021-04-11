from urllib.parse import urljoin

import scrapy

from sic_edu.enums import WebURLFlagEnum
from sic_edu.items import JobInfoItem, FiveOneJobInfoItem

import re


class BossZhiPingSpider(scrapy.Spider):
    name = 'boss_zhi_ping'

    starts_url = [
        'https://www.zhipin.com/c101270100-p100101/?srcReferer=https%3A%2F%2Fwww.zhipin.com%2Fweb%2Fcommon%2Fsecurity-check.html%3Fseed%3DOU4B%2BXIEgKl5KkyB0iv8Tw8S6JUaLyzs%2FWhiontfUng%3D&srcReferer=https%3A%2F%2Fwww.zhipin.com%2Fweb%2Fcommon%2Fsecurity-check.html%3Fseed%3DOU4B%252BXIEgKl5KkyB0iv8Tw8S6JUaLyzs%252FWhiontfUng%253D%26name%3D8bcd4390%26ts%3D1616727275191%26callbackUrl%3D%252Fc101270100-p100101%252F%26srcReferer%3Dhttps%253A%252F%252Fwww.zhipin.com%252Fweb%252Fcommon%252Fsecurity-check.html%253Fseed%253DOU4B%25252BXIEgKl5KkyB0iv8Tx6zmV5gNSHtZDF0WU5fx1w%25253D%2526name%253D8bcd4390%2526ts%253D1616727274927%2526callbackUrl%253D%25252Fc101270100-p100101%25252F%2526srcReferer%253Dhttps%25253A%25252F%25252Fwww.zhipin.com%25252Fweb%25252Fcommon%25252Fsecurity-check.html%25253Fseed%25253DOU4B%2525252BXIEgKl5KkyB0iv8Tx6zmV5gNSHtZDF0WU5fx1w%2525253D%252526name%25253D8bcd4390%252526ts%25253D1616727274398%252526callbackUrl%25253D%2525252Fc101270100-p100101%2525252F%252526srcReferer%25253Dhttps%2525253A%2525252F%2525252Fwww.zhipin.com%2525252Fchengdu%2525252F&name=8bcd4390&ts=1616727275491&callbackUrl=%2Fc101270100-p100101%2F']

    def start_requests(self):
        for url in self.starts_url:
            yield scrapy.Request(url, callback=self.parse)

    def parse(self, response, **kwargs):
        root_selector = response.selector
        li_list = root_selector.xpath('//div[@class="job-list"]/ul/li')
        for li in li_list:
            base_url = 'https://www.zhipin.com/'
            data = {
                'job_name': li.xpath('.//span[@class="job-name"]/a/text()').get(),
                'job_area': li.xpath('.//span[@class="job-area"]/text()').get(),
                'salary': li.xpath('.//div[contains(@class, "job-limit")]/span/text()').get(),
                # 'limit': li.xpath('.//div[contains(@class, "job-limit")]/p/text()').get(),x
            }
            detail_url = urljoin(base_url, li.xpath('.//span[@class="job-name"]/a/@href').get())
            item = JobInfoItem()
            item.collect(**data)
            yield scrapy.Request(detail_url, callback=self.parse_detail,
                                 meta={
                                     'item': item,
                                     'proxy': {
                                         'http_proxy': '127.0.0.1:1081',
                                         'https_proxy': '127.0.0.1:1081',
                                     },
                                 })

    def parse_detail(self, response, **kwargs):
        root_selector = response.selector
        description = root_selector.xpath('.//h3[text()="职位描述"]/following-sibling::div').get()
        item = response.meta['item']
        item.collect(description=description)
        yield item


class FiveOneJobSpider(scrapy.Spider):
    name = 'n_job'

    base_url = 'https://search.51job.com/list/090200,000000,0000,32,9,99,%25E8%25BD%25AF%25E4%25BB%25B6%25E5%25B7%25A5%25E7%25A8%258B%25E5%25B8%2588,2,{page}.html?lang=c&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&ord_field=0&dibiaoid=0&line=&welfare='

    pages = [x for x in range(1, 7)]

    def start_requests(self):
        for page in self.pages:
            url = self.base_url.format(page=page)
            yield scrapy.Request(url.format(page=1), callback=self.parse,
                                 meta={'level': WebURLFlagEnum.FIRST_LEVEL_PAGE})

    def parse(self, response, **kwargs):
        root_selector = response.selector
        job_list = root_selector.xpath('//div[@class="j_joblist"]/div')

        for job in job_list:
            # 一级页面爬取
            data = dict()
            data['position_name'] = job.xpath('.//span[@class="jname at"]/text()').get()
            data['salary'] = job.xpath('.//span[@class="sal"]/text()').get()
            data['company'] = job.xpath('.//a[contains(@class, "cname")]/text()').get()
            # data['description'] = job.xpath('.//p/span[@class="d at"]/text()').get()
            detail_url = job.xpath('.//a[@class="el"]/@href').get()

            item = FiveOneJobInfoItem()
            item.collect(**data)

            yield scrapy.Request(detail_url, callback=self.parse_detail,
                                 meta={
                                     'level': WebURLFlagEnum.SECONDE_LEVEL_PAGE,
                                     'item': item,
                                 })

    def parse_detail(self, response, **kwargs):
        root_selector = response.selector
        main_info = root_selector.xpath('//div[@class="tCompany_main"]')
        data = {
            'detail_info': main_info.xpath('.//div[@class="bmsg job_msg inbox"]').get(),
            'contact_info': main_info.xpath('.//p[@class="fp"]').get(),
            'company_info': main_info.xpath('.//div[@class="tmsg inbox"]').get()
        }
        item = response.meta['item']
        yield item
