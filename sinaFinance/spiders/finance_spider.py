# -*- coding: utf-8 -*-
import scrapy
from items import SinafinanceItem
from scrapy_redis.spiders import RedisSpider

class FinanceSpider(RedisSpider):
# class FinanceSpider(scrapy.Spider):
    name = "sina"
    # start_urls = ['http://vip.stock.finance.sina.com.cn/corp/view/vCB_AllNewsStock.php?symbol=sz000001']
    start_urls = []

    def __init__(self):
        with open('stock_list.csv', 'r') as f:
            for stock in f.readlines():
                stock = stock.strip()
                if stock[-2:] == 'SZ':
                    stock_code = 'sz' + stock[:-3]
                else:
                    stock_code = 'sh' + stock[:-3]
                url = 'http://vip.stock.finance.sina.com.cn/corp/view/vCB_AllNewsStock.php?symbol=' + stock_code
                FinanceSpider.start_urls.append(url)

    def parse(self, response):
        start = response.url.find('symbol=')+len('symbol=')+2
        code = response.url[start: start+6]
        selector = scrapy.Selector(response)
        # 获取新闻列表
        news_list = selector.xpath('//div[@class="datelist"]/ul')
        times = news_list.xpath('text()').extract()
        time_list = []
        for time in times:
            time = time.strip()
            if time != '':
                time_list.append(time)
        titles = news_list.xpath('a/text()').extract()
        title_list = []
        for title in titles:
            title = title.encode('utf-8')
            title_list.append(title)
        urls = news_list.xpath('a/@href').extract()
        url_list = []
        for url in urls:
            url = str(url)
            url_list.append(url)

        for time,title,url in zip(time_list, title_list, url_list):
            date_str, time_str = time[:10], time[-5:]
            year,month,day = date_str.split('-')
            date_str = year+month+day
            hh,mm = time_str.split(':')
            time_str = hh+mm
            # print("time:", time[:10], time[-5:], date_str, time_str)
            # print("title:", title)
            # print("url:", url)
            yield scrapy.Request(url, callback=self.parse_content, meta={'time':date_str+time_str, 'date':date_str, 'code':code, 'link':url, 'title':title})
        # 已经处理完一个页面的所有新闻，进行下一页处理
        next_page = selector.xpath('//div[@style="margin-top:10px;float:right;margin-right:100px;"]/a/@href').extract()
        if next_page:
            next = next_page[-1]
            yield scrapy.Request(next, callback=self.parse)

    def parse_content(self, response):
        selector = scrapy.Selector(response=response)
        content_list = selector.xpath('//div[@id="artibody"]/p//text()').extract()
        content = r""
        for part in content_list:
            part = part.strip().encode('utf-8')
            content += part
        item = SinafinanceItem()
        item['code'] = response.meta['code']
        item['time'] = response.meta['time']
        item['date'] = response.meta['date']
        item['link'] = response.meta['link']
        item['title'] = response.meta['title']
        item['content'] = content
        yield item

