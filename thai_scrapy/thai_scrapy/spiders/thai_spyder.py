# -*- coding: utf-8 -*-

from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from thai_scrapy.items import ArticleItem

i = 1


class MySpider(CrawlSpider):

    global i

    name = u'thai_spy'
    allowed_domains = [u'dailynews.co.th']
    start_urls = [
        u'http://www.dailynews.co.th',
    ]

    rules = (
        Rule(SgmlLinkExtractor(allow=(), restrict_xpaths=(u'//a',)), callback=u'parse_items', follow=True),
    )

    def parse_items(self, response):

        global i

        hxs = HtmlXPathSelector(response)
        paragraphs = hxs.xpath(u'//div[@class="entry"]/p')
        title = hxs.xpath(u'//h1[@class="entry-title"]/text()').extract()
        content = []
        item = ArticleItem()
        for p in paragraphs:
            content += p.xpath(u'./text()').extract()

        if content:
            item[u'content'] = u' '.join(content)
            item[u'name'] = i
            i += 1
            if title:
                item[u'title'] = title[0]
            item[u'link'] = response.url
            yield item
