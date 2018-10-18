# -*- coding: utf-8 -*-
"""
@Filename: web_target_store
@Date    : 2018/8/8
@Author  : Ted Zhao
@Email   : ted.zhao@dji.com
"""

import scrapy
import json

from urllib.parse import urlencode
from scrapy_redis.utils import bytes_to_str
from scrapy_redis.spiders import RedisSpider

from shop_locations.items import WebItem


class TargetSpider(RedisSpider):
    name = "target"
    allowed_domains = ["target.com"]

    url = "https://redsky.target.com/v2/stores/nearby/{}?"

    custom_settings = {
        "DOWNLOAD_DELAY": 0.5,
        "CONCURRENT_REQUESTS": 16,
        "REDIS_START_URLS_KEY": "%(name)s:address",  # key for redis queue
    }

    # setting for scrapy-redis
    custom_settings.update(
        dict(
            SCHEDULER="scrapy_redis.scheduler.Scheduler",
            DUPEFILTER_CLASS="scrapy_redis.dupefilter.RFPDupeFilter",
            REDIS_HOST="localhost",
            REDIS_PORT=6379,
        )
    )

    querystring = {"locale": "en-US", "limit": "999", "range": "250"}

    headers = {
        'accept': "application/json",
        'Cache-Control': "no-cache"
    }

    def make_request_from_data(self, data):
        data = bytes_to_str(data, self.redis_encoding)
        return scrapy.Request(
            self.get_url(location=data, **self.querystring),
            headers=self.headers,
            callback=self.parse
        )

    def get_url(self, location: str, **kwargs):
        if kwargs:
            return self.url.format(location) + urlencode(kwargs)
        else:
            raise ValueError("kwargs should not be empty.")

    def parse(self, response):
        print(response.url)
        data = json.loads(response.body_as_unicode())
        results = data.get("Locations").get("Location")
        if results:
            for result in results:
                result["_id"] = result["ID"]
                item = WebItem()
                item["item"] = result
                yield item
