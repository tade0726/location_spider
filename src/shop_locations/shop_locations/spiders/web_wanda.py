# -*- coding: utf-8 -*-
"""
refs:
- http://www.wandaplaza.cn/

dep:
- get all the store info
"""

import scrapy
from bs4 import BeautifulSoup

from shop_locations.items import WebItem, PlazaMapItem, PlazaStoreItem, PlazaStoreItem2


class WandaPlaza(scrapy.Spider):

    name = "wanda_plaza"
    allowed_domains = ["wandaplaza.cn"]

    home_page = "http://www.wandaplaza.cn/"

    custom_settings = {"DOWNLOAD_DELAY": 0.5, "CONCURRENT_REQUESTS": 32}

    # proxy
    # custom_settings.update(
    #     dict(
    #         DOWNLOADER_MIDDLEWARES={
    #             'shop_locations.middlewares.CustomProxyMiddleware': 350,
    #             'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 400
    #         }
    #     )
    # )

    def start_requests(self):
        yield scrapy.Request(url=self.home_page, callback=self.parse_home_page)

    def parse_home_page(self, response):
        soup = BeautifulSoup(response.text, "lxml")
        item_lists = []

        for a in soup.find_all("a"):
            if a.has_attr("target") and a.has_attr("href") and a.has_attr("title"):
                web_item = WebItem()
                item = {}
                detail_page = a.attrs["href"]
                detail_page = detail_page.rstrip("/")
                item["url"] = detail_page
                item["name"] = a.attrs["title"]
                item["_id"] = item["name"]
                web_item["item"] = item

                item_lists.append(web_item)

                yield scrapy.Request(
                    url=detail_page + "/business",
                    callback=self.parse_detail_page,
                    meta={"name": item["name"], "detail_page": detail_page},
                )

        for item in item_lists:
            yield item

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

                    # yield scrapy.Request(url=store_item["store_url"],
                    #                      callback=self.parse_store_page,
                    #                      meta={
                    #                          "plaza_name": plaza_name,
                    #                          "url": store_item["store_url"]
                    #                      })

                    yield store_item

    # def parse_store_page(self, response):
    #
    #     soup = BeautifulSoup(response.text, "lxml")
    #     item = PlazaStoreItem2()
    #
    #     item["plaza_name"] = response.meta["plaza_name"]
    #
    #     for h1 in soup.find_all("h1"):
    #         if "bb1s" in h1.attrs["class"]:
    #             item["store_name"] = h1.text
    #
    #     for img in soup.find_all("img"):
    #         if img.attrs.get("alt") == item["name"]:
    #             item["image_urls"] = [img.attrs["src"]]
    #             item["_id"] = response.url
    #     yield item
