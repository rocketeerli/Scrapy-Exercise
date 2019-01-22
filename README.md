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
	
定义数据结构，编辑 items.py，添加下面这个类：

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
	
# 三、爬取校花网（http://www.xiaohuar.com/list-1-1.html）

参考文章：[Scrapy简单入门及实例讲解](https://www.cnblogs.com/kongzhagen/p/6549053.html)

创建工程：

	scrapy startproject xiaohua_picture
	
创建爬虫：

	cd .\xiaohua_picture\
	scrapy genspider xiaohua xiaohuar.com

定义数据结构，编辑 items.py，更改类为：

	class XiaohuaPictureItem(scrapy.Item):
		addr = scrapy.Field()
		name = scrapy.Field()
		
编写爬虫：

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
	
		def parse(self, response):
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

设置配置文件，编辑 settings.py ，添加：

	ITEM_PIPELINES = {
		'xiaohua_picture.pipelines.XiaohuaPicturePipeline':100
	}
					
编写数据处理脚本，编辑 pipelines.py ：
	# -*- coding: utf-8 -*-
	import urllib.request
	import os
	
	class XiaohuaPicturePipeline(object):
		def process_item(self, item, spider):
			headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0'}
			req = urllib.request.Request(url=item['addr'],headers=headers)
			res = urllib.request.urlopen(req)
			file_name = os.path.join(r'F:\xiaohua-pictures',item['name']+'.jpg')
			with open(file_name,'wb') as fp:
				fp.write(res.read())

运行爬虫：

	scrapy crawl xiaohua

修改爬虫文件，获取所有的校花图片，修改 xiaohua.py ：

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

运行爬虫：

	scrapy crawl xiaohua
					
