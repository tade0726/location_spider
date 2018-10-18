# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup
from shop_locations.items import WebItem
import re


class SundanSpider(scrapy.Spider):
    name = "sundan"
    allowed_domains = ["sundan.com"]
    base_url = "https://www.sundan.com/storecenter-selectArea-{}.html"
    re_coor = re.compile("\('(.*?)'\)")

    def start_requests(self):
        for i in range(1, 11):
            URL = self.base_url.format(i)
            yield scrapy.Request(URL, callback=self.parse)

    def parse(self, response):
        soup = BeautifulSoup(response.text, "lxml")

        for item in soup.find_all("div", class_="area_row_message_right"):
            item_store = dict()

            scrapy_item = WebItem()

            title = item.findAll("div", class_="area_row_message_name")[0]
            title = title.text.strip()

            try:
                coordinate = item.findAll("div", class_="check_map")[0]
                coordinate = coordinate.attrs["onclick"]

                lng, lat = self.re_coor.findall(coordinate)[0].split(",")
                item_store["lat"] = lat
                item_store["lng"] = lng
            except Exception as exc:
                pass

            item_store["name"] = title

            for content in item.findAll("div", class_="area_row_message_text"):
                content = content.text.strip()
                field_name, *value = content.split("：")
                value = "：".join(value)
                field_name = field_name.strip()
                item_store[field_name] = value.strip()

            item_store["_id"] = item_store["门店地址"]
            scrapy_item["item"] = item_store

            yield scrapy_item
