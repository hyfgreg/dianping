# -*- coding: utf-8 -*-
import json
from dianping.settings import MONGO_URI,MONGO_DATABASE
import re
from scrapy import Spider,Request
from dianping.items import shopItem,categoryItem
import pymongo
import logging

class DianpingspiderSpider(Spider):
    name = 'dianpingspider'
    allowed_domains = ['www.dianping.com']
    # start_urls = ['http://www.dianping.com/']
    client = pymongo.MongoClient(MONGO_URI)
    db = client[MONGO_DATABASE]
    logger = logging.getLogger()

    menu_url = 'http://www.dianping.com/ajax/json/category/menu?cityId={cityId}'

    category_url = 'http://www.dianping.com/search/category/{cityId}/{categoryId}/g{child_categoryId}'

    def start_requests(self):
        yield Request(self.menu_url.format(cityId='1'),self.parse_menu)

    def parse_menu(self,response):
        result = json.loads(response.text)
        cityId = re.search('cityId=(.*?)$',response.url).group(1)
        self.logger.debug('cityId=',cityId)
        try:
            if 'categories' in result.keys() and result.get('categories'):
                categories = result.get('categories')
                for category in categories:
                    item = categoryItem()
                    for field in item.fields:
                        if field in category.keys():
                            item[field] = category.get(field)
                    yield item
                    for child in item.get('children'):
                        yield Request(self.category_url.format(cityId=cityId,categoryId=item['categoryId'],child_categoryId=child.get('categoryId')),callback=self.parse_shop)

        except Exception:
            raise Exception

    def parse_test(self, response):
        url = 'http://www.dianping.com/search/category/1/10/g101'
        a = re.search(r'category\/(.*?)\/(.*?)\/g(.*?)$', url).group(1)
        b = re.search(r'category\/(.*?)\/(.*?)\/g(.*?)$', url).group(2)
        c = re.search(r'category\/(.*?)\/(.*?)\/g(.*?)$', url).group(3)
        print(a,b,c)


    def parse_shop(self, response):
        shop_list = response.xpath('//*[@id="shop-all-list"]/ul/li')
        for li in shop_list:
            try:
                item = shopItem()
                item['img'] = li.xpath('.//div[@class="pic"]/a/img/@data-src').extract_first()
                item['name'] = li.xpath('.//div[@class="txt"]/div[@class="tit"]/a/@title').extract_first()
                item['shopId'] = li.xpath('.//div[@class="txt"]/div[@class="tit"]/a/@href').extract_first()[6:]
                item['stars'] = li.xpath('.//div[@class="comment"]/span/@title').extract_first()
                item['review_num'] = li.xpath('.//div[@class="comment"]/a[@class="review-num"]/b/text()').extract_first()
                item['mean_price'] = li.xpath('.//div[@class="comment"]/a[@class="mean-price"]/b/text()').extract_first()[1:]
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

                item['categoryId'] = re.search(r'category\/(.*?)\/(.*?)\/g(.*?)$', response.url).group(2)
                # item['categoryName'] = self.db['category'].find_one({'categoryId':item['categoryId']}).get('categoryName')

                item['child_categoryId'] = re.search(r'category\/(.*?)\/(.*?)\/g(.*?)$', response.url).group(3)

                item['cityId'] = re.search(r'category\/(.*?)\/(.*?)\/g(.*?)$', response.url).group(1)

                yield item
            except TypeError:
                pass

        next = response.xpath('//div[@class="section Fix"]/div[@class="content-wrap"]/div[@class="shop-wrap"]/div[@class="page"]/a[@class="next"]/@href').extract_first()
        next_url = response.urljoin(next)
        if next_url:
            yield Request(next_url,self.parse_shop)
