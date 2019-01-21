# -*- coding: utf-8 -*-
import scrapy
from ..items import MeijuItem

class MeijuSpider(scrapy.Spider):
    name = 'meiju'
    allowed_domains = ['meijutt.com']
    start_urls = ['http://www.meijutt.com/new100.html']

    def parse(self, response):
        movies = response.xpath('//ul[@class="top-list  fn-clear"]/li')
        rank = 1
        for each_movie in movies:
            item = MeijuItem()
            item['rank'] = str(rank)
            item['name'] = each_movie.xpath('./h5/a/@title').extract()[0]
            rank = rank + 1
            yield item
