# -*- coding: utf-8 -*-
import scrapy
from ..items import XiaohuaPictureItem

class XiaohuaSpider(scrapy.Spider):
    # 爬虫名称，唯一
    name = 'xiaohua'
    # 允许访问的域
    allowed_domains = ['xiaohuar.com']
    # 初始URL
    start_urls = ['http://www.xiaohuar.com/list-1-1.html']
    # 设置一个空集合
    url_set = set()

    def parse(self, response):
    # 设置一个空集合
    url_set = set()

    def parse(self, response):
        if response.url.startswith("http://www.xiaohuar.com/list-"):
            # 获取所有图片的 a 标签
            all_pics = response.xpath('//div[@class="item_t"]')
            for pic in all_pics:
                # 分别处理每个图片，取出名称和地址
                item = XiaohuaPictureItem()
                name = pic.xpath('./div[@class="title"]/span/a/text()').extract()[0]
                addr = pic.xpath('./div[@class="img"]/a/img/@src').extract()[0]
                addr = 'http://www.xiaohuar.com' + addr
                item['name'] = name
                item['addr'] = addr
                yield item
        # 获取所有的地址链接
        urls = response.xpath("//a/@href").extract()
        for url in urls:
            # 如果地址以http://www.xiaohuar.com/list-开头且不在集合中，则获取其信息
            if url.startswith("http://www.xiaohuar.com/list-"):
                if url in XiaohuaSpider.url_set:
                    pass
                else:
                    XiaohuaSpider.url_set.add(url)
                    yield scrapy.Request(url, callback=self.parse)
                    # yield self.make_requests_from_url(url) # 该函数已被弃用
            else:
                pass
