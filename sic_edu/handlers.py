class ItemHandler:
    def changeFieldProperty(self, **kwargs):
        """
        description:
            转换scrapy.Filed() -> peewee.Filed()
        args:
            kwargs 中存储一堆scrapy.Filed()
        return:
            Iterable 的peewee.Filed()
        """
        pass

    def defineChangeRule(self):
        """
        description:
            制定规则
        """
        pass


class FiveOneJobInfoItemHandler(ItemHandler):
    def changeFieldProperty(self, **kwargs):
        pass

    def defineChangeRule(self):
        self.rules = {}
