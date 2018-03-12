# 新浪财经个股新闻爬虫

## 部署信息

1. 爬虫框架：scrapy
2. 爬虫拓展模块（实现分布式）：scrapy-redis
3. 数据库：redis, mongodb
4. python 2.7

## 功能介绍

该爬虫可以爬取个股页面所有的新闻信息，例如（http://vip.stock.finance.sina.com.cn/corp/view/vCB_AllNewsStock.php?symbol=sz000001 ）页面的中的新闻。爬取新闻的时间、标题、正文内容、新闻的url，将这些信息存入mongodb数据库。该爬虫实现了分布式，item去重功能。
