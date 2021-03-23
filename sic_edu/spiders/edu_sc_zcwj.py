import scrapy
from urllib.parse import urljoin


class EduScZcwjSpider(scrapy.Spider):
    name = 'edu_sc_zcwj'
    allowed_domains = ['edu.sc.gov.cn']
    start_urls = ['http://edu.sc.gov.cn/scedu/c100538/xxgk_list.shtml']

    def parse(self, response):
        root_selector = response.selector
        li_list = root_selector.xpath('//ul[@class="xwzxList"]/li')
        for li in li_list:
            title = li.xpath('./a/@title').get()
            href = li.xpath('./a/@href').get()
            title_src = urljoin('http://edu.sc.gov.cn/', href)
            yield scrapy.Request(title_src, callback=self.parse_content)

    def parse_content(self, response):
        root_selector = response.selector
        div_detail = root_selector.xpath('//div[@class="detail"]')
        title = div_detail.xpath('./h1/text()').get()
        release_time = div_detail.xpath('./div[@class="xgxx"]/span[2]/text()').get()
        print(title, release_time)
        pass

    def test(self, response):
        # 第一段程序,测试Scrapy的运行可否
        if response.status == 200:
            print(response)
            print('爬虫执行完成')
        pass

    def handler_element_test(self, response):
        root_selector = response.selector
        li_list = root_selector.xpath('//ul[@class="xwzxList"]/li')
        for li in li_list:
            title = li.xpath('./a/@title').get()
            href = li.xpath('./a/@href').get()
            title_src = urljoin('http://edu.sc.gov.cn/', href)
            print(title, title_src)
        pass

    def test_redirect(self, response):
        pass
