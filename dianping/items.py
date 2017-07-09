# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item,Field


class shopItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = Field()
    stars = Field()
    review_num = Field()
    mean_price = Field()
    comment_list = Field()
    tag = Field()
    address = Field()
    area = Field()
    img = Field()
