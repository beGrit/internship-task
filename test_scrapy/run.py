from scrapy import cmdline


def crawl():
    cmdline.execute('scrapy crawl edu_sc_zcwj'.split())


if __name__ == '__main__':
    crawl()
