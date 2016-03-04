# -*- coding: utf-8 -*-

import scrapy


class ArticleItem(scrapy.Item):
    content = scrapy.Field()
    name = scrapy.Field()
    title = scrapy.Field()
    link = scrapy.Field()
