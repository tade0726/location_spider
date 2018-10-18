# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
from datetime import datetime
from shop_locations.items import (
    FailUrlItem,
    WebItem,
    # api service
    ApiItem,
    PlazaStoreItem2,
    PlazaMapItem,
    PlazaStoreItem
)


class MongoPipeline:

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get("MONGO_URI"),
            mongo_db=crawler.settings.get("MONGO_DATABASE", "items"),
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        raise NotImplementedError


class ItemPipeline(MongoPipeline):

    def process_item(self, item, spider):
        if isinstance(item, ApiItem):
            item["item"]["crawled_timestamp"] = datetime.now()
            collection_name = "_".join(["api", spider.name])
            self.db[collection_name].insert_one(dict(item["item"]))
        if isinstance(item, WebItem):
            item["item"]["crawled_timestamp"] = datetime.now()
            collection_name = "_".join(["web", spider.name])
            self.db[collection_name].insert_one(dict(item["item"]))
        return item


class WandaStorePipeline(MongoPipeline):

    def process_item(self, item, spider):
        if isinstance(item, PlazaStoreItem2):
            item["crawled_timestamp"] = datetime.now()
            collection_name = "_".join(["web", spider.name, "store"])
            self.db[collection_name].insert_one(dict(item))
        if isinstance(item, PlazaMapItem):
            item["crawled_timestamp"] = datetime.now()
            collection_name = "_".join(["web", spider.name, "map"])
            self.db[collection_name].insert_one(dict(item))
        if isinstance(item, PlazaStoreItem):
            item["crawled_timestamp"] = datetime.now()
            collection_name = "_".join(["web", spider.name, "store_urls"])
            self.db[collection_name].insert_one(dict(item))
        return item