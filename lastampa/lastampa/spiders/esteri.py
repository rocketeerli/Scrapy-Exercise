# -*- coding: utf-8 -*-
import scrapy
import re
from ..items import LastampaItem

class EsteriSpider(scrapy.Spider):
    # 爬虫名称，唯一
    name = 'esteri'
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
            if url.startswith("/esteri"):
                # 将链接拼接全
                url = response.urljoin(url)
                # 检测链接是否访问过，避免 url 重复访问
                if not url in self.url_set:
                    self.url_set.add(url)
                    yield scrapy.Request(url, callback=self.parse_topic)
    # 分析话题链接，并将文章链接交给处理文章的函数
    def parse_topic(self, response):
        # 找到这个页面下的所有文章链接
        all_urls = response.xpath('//div[@class="ls-box-titolo"]/a/@href').extract()
        for url in all_urls:
            # 找到符合这个话题的文章链接
            if re.search(r"/\d{4}/\d{2}/\d{2}/esteri/", url) is not None:
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
            if re.search(r"/\d{4}/\d{2}/\d{2}/esteri-", page_url) is not None:
                # 将链接拼接全
                page_url = response.urljoin(page_url)
                # 检测链接是否访问过，避免 url 重复访问
                if not page_url in self.url_set:
                    self.url_set.add(page_url)
                    yield scrapy.Request(page_url, callback=self.parse_topic)
            if re.search(r"/\d{4}/\d{2}/\d{2}/lastampa-in-english-", page_url) is not None:
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
        # 获取文章 url
        url = response.url
        # 获取文章评论
        review = ""
        # 获取文章内容
        content = ""
        
        # 获取文章发布时间
        times = response.xpath('//meta[@itemprop="datePublished"]/@content').extract()
        if len(times) > 0:
            time = times[0]
        elif response.xpath('//div[@class="ls-articoloData"]/text()') is not None:
            time = response.xpath('//div[@class="ls-articoloData"]/text()').extract()[0]
        # 文章类型
        type = "esteri"
        item['title'] = title
        item['url'] = url
        item['review'] = review
        item['content'] = content
        item['time'] = time
        item['type'] = type
