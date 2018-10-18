# -*- coding: utf-8 -*-
"""
refs:
- http://www.wandaplaza.cn/

dep:
- get all the store info
"""

import scrapy
import redis

from bs4 import BeautifulSoup

from scrapy_redis.utils import bytes_to_str

from shop_locations.items import WebItem, PlazaMapItem, PlazaStoreItem, PlazaStoreItem2


redis_client = redis.Redis(host="127.0.0.1", port=6379, db=0)


class WandaPlaza(scrapy.Spider):

    name = "wanda_plaza_shanghu"

    custom_settings = {"DOWNLOAD_DELAY": 0.5, "CONCURRENT_REQUESTS": 32}

    def start_requests(self):
        items = redis_client.lrange("wanda_plaza:url", 0, -1)
        for item in items:
            item = bytes_to_str(item)
            home_page, plaza_name = item.split("|")
            business_url = home_page + "/shanghu"
            yield scrapy.Request(
                url=business_url,
                callback=(self.parse_detail_page),
                meta={"name": plaza_name, "detail_page": home_page},
            )

    def parse_detail_page(self, response):
        soup = BeautifulSoup(response.text, "lxml")
        map_item = PlazaMapItem()
        plaza_name = response.meta["name"]
        map_item["plaza_name"] = plaza_name
        detail_page = response.meta["detail_page"]
        map_urls = []

        for p in soup.find_all("p"):
            if p.has_attr("class") and p.attrs["class"][0] == "b1s":
                for img in p.find_all("img"):
                    map_urls.append(img.attrs["src"])

        map_item["image_urls"] = map_urls
        map_item["_id"] = plaza_name
        yield map_item

        for ul in soup.find_all("ul"):
            if ul.has_attr("class") and ul.attrs["class"][0] == "cf":
                for a in ul.find_all("a"):
                    store_item = PlazaStoreItem()
                    img = a.find_all("img")[0]

                    store_item["store_url"] = detail_page.rstrip("/") + a.attrs["href"]
                    store_item["image_urls"] = [img.attrs["src"]]
                    store_item["_id"] = store_item["store_url"]
                    store_item["plaza_name"] = plaza_name

                    yield store_item
