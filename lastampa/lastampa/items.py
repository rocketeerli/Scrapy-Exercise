# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class LastampaItem(scrapy.Item):
    title = scrapy.Field()
    url = scrapy.Field()
    review = scrapy.Field()
    content = scrapy.Field()
    time = scrapy.Field()
    type = scrapy.Field()
