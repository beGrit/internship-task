from scrapy import cmdline


def crawl(spider_name: str):
    cmdline.execute(('scrapy crawl %s --nolog' % spider_name).split())


if __name__ == '__main__':
    crawl('n_job')
