# Scrapy-Exercise

Scrapy 爬虫练习

# Srapy 框架基本步骤

 `xxx` 表示的是需要更改的

## 1、创建工程

`projectName` 表示工程名，可根据自己的需求进行更改。创建好后，工程的文件名就是工程名。

	scrapy startproject projectName
	
## 2、创建爬虫程序

创建蜘蛛模板，example是蜘蛛名，example.com是start_urls

	cd projectName
	scrapy genspider example example.com
	
注意：**example 不能和项目名（projectName)相同**
	
## 3、定义存储数据的数据结构

编辑 items.py

## 4、编写爬虫

编辑 example.py

## 5、设置配置文件

编辑 settings.py

## 6、编写数据处理脚本

编辑 pipelines.py

## 7、执行爬虫

命令行内输入下列命令：

	scrapy crawl example --nolog
	
注意：

* **这里一定要注意，一定要进入 projectName 这个目录，也就是我们创建的蜘蛛项目目录！**
* ** crawl 后面跟的是类里面定义的蜘蛛名，并不是项目名、也不是类名！**

# 一、爬取 HTML 页面，不做任何处理，直接保存到文件（dictum 项目）

参考文章：[编写第一个scrapy蜘蛛](http://www.scrapyd.cn/doc/140.html)

创建工程：

	scrapy startproject dictum

创建爬虫程序：

	cd .\dictum\
	scrapy genspider dictum_spider lab.scrapyd.cn
	
更改 dictum_spider.py 文件，代码见项目。

# 二、美剧天堂前100最新

参考文章：[Scrapy简单入门及实例讲解](https://www.cnblogs.com/kongzhagen/p/6549053.html)

创建工程：

	scrapy startproject meiju_new100

创建爬虫程序：

	cd .\meiju_new100\
	scrapy genspider meiju meijutt.com
	
定义数据结构：

	class MeijuItem(scrapy.Item):
		rank = scrapy.Field()
		name = scrapy.Field()

编写爬虫，编辑 meiju.py ：

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

设置配置文件，编辑 settings.py ，添加：

	ITEM_PIPELINES = {
		'meiju_new100.pipelines.MeijuNew100Pipeline':100
	}

编写数据处理脚本，编辑 pipelines.py ，将数据写入文件：

	class MeijuNew100Pipeline(object):
		def process_item(self, item, spider):
			with open("meiju.txt",'a') as fp:
				fp.write(item['rank'] + '\t' + item['name'] + '\n')
				
执行爬虫：

	scrapy crawl meiju
	

	