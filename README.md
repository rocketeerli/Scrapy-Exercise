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
	
## 3、设置数据存储模板

编辑 items.py

## 4、编写爬虫

编辑 example.py

## 5、设置配置文件

编辑 settings.py

## 6、编写数据处理脚本

编辑 pipelines.py

## 7、执行爬虫

命令行内输入下列命令：

	cd projectName
	scrapy crawl example --nolog
	
注意：

* **这里一定要注意，一定要进入 projectName 这个目录，也就是我们创建的蜘蛛项目目录！**
* ** crawl 后面跟的是类里面定义的蜘蛛名，并不是项目名、也不是类名！**

# 一、爬取 HTML 页面，不做任何处理，直接保存到文件

参考文章：[编写第一个scrapy蜘蛛](http://www.scrapyd.cn/doc/140.html)

创建工程：

	scrapy startproject dictum

创建爬虫程序：

	cd .\dictum\
	scrapy genspider dictum_spider lab.scrapyd.cn
	
更改 dictum_spider.py 文件，代码见项目。

# 二、

