# -*- coding: utf-8 -*-
import scrapy
import re
from ..items import LastampaItem
import html
from ..contentDeal import deal_content

class EconomiaSpider(scrapy.Spider):
    # 爬虫名称，唯一
    name = 'economia'
    # 允许访问的域  
    allowed_domains = ['lastampa.it']
    # 初始URL
    start_urls = ['http://lastampa.it/']
    # 设置一个空集合
    url_set = set()
    # 获取主题链接
    def parse(self, response):
        all_urls = response.xpath('//div[@class="menu_item_normal"]//a/@href').extract()
        for url in all_urls:
            if url.startswith("/economia"):
                # 将链接拼接全
                url = response.urljoin(url)
                # 检测链接是否访问过，避免 url 重复访问
                if not url in self.url_set:
                    self.url_set.add(url)
                    yield scrapy.Request(url, callback=self.parse_topic)
    # 分析话题链接，并将文章链接交给处理文章的函数
    def parse_topic(self, response):
        # 找到这个页面下的所有文章链接
        all_urls = response.xpath('//div[@class="ls-box-titolo"]//a/@href').extract()
        for url in all_urls:
            # 找到符合这个话题的文章链接
            if re.search(r"/\d{4}/\d{2}/\d{2}/economia/", url) is not None:
                # 将链接拼接全
                url = response.urljoin(url)
                # 检测链接是否访问过，避免 url 重复访问
                if not url in self.url_set:
                    self.url_set.add(url)
                    yield scrapy.Request(url, callback=self.get_Content)
        # 查找下一页
        # 第一种分页情况
        page_urls = response.xpath('//a[@class="btn_cerchio-freccia"]/@href').extract()
        for page_url in page_urls:
            # 将链接拼接全
            page_url = response.urljoin(page_url)
            # 检测链接是否访问过，避免 url 重复访问
            if not page_url in self.url_set:
                self.url_set.add(page_url)
                yield scrapy.Request(page_url, callback=self.parse_topic)
        # 第二种分页情况
        page_urls = response.xpath('//div[@class="ls-intestazioneBlu"]//a/@href').extract()
        for page_url in page_urls:
            if re.search(r"\?page=", page_url) is not None:
                # 将链接拼接全
                page_url = response.urljoin(page_url)
                # 检测链接是否访问过，避免 url 重复访问
                if not page_url in self.url_set:
                    self.url_set.add(page_url)
                    yield scrapy.Request(page_url, callback=self.parse_topic)
            
    # 从文章中获取内容
    def get_Content(self, response):
        item = LastampaItem()
        # 获取文章标题
        title = response.xpath('//div[@class="ls-articoloTitolo"]/h3/text()').extract()[0]
        title = re.sub(r"\s+"," ", title)
        # 获取文章 url
        url = response.url
        # 获取文章评论
        review = ""
        # 获取文章内容
        content = ""
        # 第一种文章内容标签
        content_text = response.xpath('//div[@class="ls-articoloTesto"]|//div[@class=ls-articoloTesto]').extract()
        # if len(content_text) == 0:
        #     # 第二种文章内容标签
        #     content_text = response.xpath('').extract()
        content = content_text[0]
        # for text in content_text:
        #     content = content + html.unescape(text)
        # content = re.search(r"<div.*?>(.*)</div>", content, re.S).group(1)
        content = deal_content(content)
        # 获取文章发布时间
        times = response.xpath('//meta[@itemprop="datePublished"]/@content').extract()
        if len(times) > 0:
            time = times[0]
        elif len(response.xpath('//div[@class="ls-articoloData"]/text()').extract()) > 0:
            time = response.xpath('//div[@class="ls-articoloData"]/text()').extract()[0]
        elif len(response.xpath('//meta[@name="EdDateTime"]/@content').extract()) > 0:
            time = response.xpath('//meta[@name="EdDateTime"]/@content').extract()[0]
        # 文章类型
        type = self.name
        item['title'] = title
        item['url'] = url
        item['review'] = review
        item['content'] = content
        item['time'] = time
        item['type'] = type
        yield item

