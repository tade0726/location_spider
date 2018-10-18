# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Item

class FailUrlItem(Item):
    # define the fields for your item here like:
    item = scrapy.Field()


class WebItem(Item):
    item = scrapy.Field()


class ApiItem(Item):
    item = scrapy.Field()


## wanda
class BaseItem(Item):
    _id = scrapy.Field()
    crawled_timestamp = scrapy.Field()
    plaza_name = scrapy.Field()


class PlazaMapItem(BaseItem):
    image_urls = scrapy.Field()
    images = scrapy.Field()


class PlazaStoreItem(BaseItem):
    image_urls = scrapy.Field()
    store_url = scrapy.Field()
    images = scrapy.Field()


class PlazaStoreItem2(BaseItem):
    image_urls = scrapy.Field()
    store_name = scrapy.Field()
