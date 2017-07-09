# -*- coding: utf-8 -*-
from scrapy import Spider,Request
from dianping.items import shopItem


class DianpingspiderSpider(Spider):
    name = 'dianpingspider'
    allowed_domains = ['www.dianping.com']
    # start_urls = ['http://www.dianping.com/']

    hg_url = 'http://www.dianping.com/search/category/1/10/g101'

    def start_requests(self):
        yield Request(self.hg_url,self.parse_shop)

    def parse_shop(self, response):
        shop_list = response.xpath('//*[@id="shop-all-list"]/ul/li')
        for li in shop_list:
            item = shopItem()
            item['img'] = li.xpath('.//div[@class="pic"]/a/img/@data-src').extract_first()
            item['name'] = li.xpath('.//div[@class="txt"]/div[@class="tit"]/a/@title').extract_first()
            item['stars'] = li.xpath('.//div[@class="comment"]/span/@title').extract_first()
            item['review_num'] = li.xpath('.//div[@class="comment"]/a[@class="review-num"]/b/text()').extract_first()
            item['mean_price'] = li.xpath('.//div[@class="comment"]/a[@class="mean-price"]/b/text()').extract_first()[1:]
            # item['comment_list'] = li.xpath('.//div[@class="txt"]//div[@class="comment-list"]')
            comment_list = []
            spans = li.xpath('.//div[@class="txt"]/span[@class="comment-list"]/span')
            for span in spans:
                a = span.xpath('.//text()').extract_first()
                b = span.xpath('.//b/text()').extract_first()
                comment = {a:b}
                comment_list.append(comment)
            item['comment_list'] = comment_list
            item['tag'] = li.xpath('.//div[@class="txt"]/div[@class="tag-addr"]/a[1]/span/text()').extract_first()
            item['area'] = li.xpath('.//div[@class="txt"]/div[@class="tag-addr"]/a[2]/span/text()').extract_first()
            item['address'] = li.xpath('.//div[@class="txt"]/div[@class="tag-addr"]/span[@class="addr"]/text()').extract_first()
            yield item

