# -*- coding: utf-8 -*-
"""
refs:
- http://www.wandaplaza.cn/

dep:
- get all the store info
"""

import redis
import scrapy
from bs4 import BeautifulSoup

from scrapy_redis.spiders import RedisSpider
from scrapy_redis.utils import bytes_to_str

from shop_locations.items import PlazaStoreItem2


redis_client = redis.Redis(host="127.0.0.1", port=6379, db=0)


class WandaPlaza(scrapy.Spider):

    name = "wanda_plaza_store"
    # allowed_domains = ["wandaplaza.cn"]

    home_page = "http://www.wandaplaza.cn/"

    custom_settings = {
        "DOWNLOAD_DELAY": 0.1,
        "CONCURRENT_REQUESTS": 128,
        # "REDIS_START_URLS_KEY": "%(name)s:url",  # key for redis queue
        "RETRY_TIMES": 1,
    }

    # setting for scrapy-redis
    # custom_settings.update(
    #     dict(
    #         SCHEDULER="scrapy_redis.scheduler.Scheduler",
    #         DUPEFILTER_CLASS="scrapy_redis.dupefilter.RFPDupeFilter",
    #         REDIS_HOST="localhost",
    #         REDIS_PORT=6379
    #     )
    # )

    # proxy and agents
    custom_settings.update(
        dict(
            DOWNLOADER_MIDDLEWARES={
                # 'shop_locations.middlewares.CustomProxyMiddleware': 350,
                # 'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 400,
                "shop_locations.middlewares.CustomUserAgentMiddleware": 350,
                "scrapy.downloadermiddlewares.retry.RetryMiddleware": 500,
                "scrapy.downloadermiddlewares.httpcache.HttpCacheMiddleware": 900,
            }
        )
    )

    def start_requests(self):
        urls = redis_client.lrange("wanda_plaza_store:url", 0, -1)
        for url in urls:
            url = bytes_to_str(url)
            yield scrapy.Request(url=url, callback=(self.parse_store_page))

    # def make_request_from_data(self, data):
    #     data = bytes_to_str(data, self.redis_encoding)
    #     return scrapy.Request(url=data, callback=self.parse_store_page)

    def parse_store_page(self, response):

        soup = BeautifulSoup(response.text, "lxml")
        item = PlazaStoreItem2()

        for h1 in soup.find_all("h1"):
            if "bb1s" in h1.attrs["class"]:
                item["store_name"] = h1.text

        for img in soup.find_all("img"):
            if img.attrs.get("alt") == item["store_name"]:
                item["image_urls"] = [img.attrs["src"]]
                item["_id"] = response.url
        yield item
