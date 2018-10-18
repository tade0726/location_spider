import scrapy
import json
import re

from shop_locations.items import WebItem


class XiaoTianCai(scrapy.Spider):

    name = "xiaotiancai"
    allowed_domains = ["okii.com"]

    get_area_url = "https://www.okii.com/portals-server/server/getNetInfoByArea/1"
    get_index_url = "https://www.okii.com/portals-server/server/getNetInfoIndex/1"

    custom_settings = {"DOWNLOAD_DELAY": 0, "CONCURRENT_REQUESTS": 16}

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Cache-Control": "no-cache",
    }

    re_json = re.compile("null\((.*)\)")

    def start_requests(self):
        payload = "dataType=json&pageNo=999&pageSize=1&brand=okii&type=sale"
        yield scrapy.Request(
            self.get_index_url,
            method="post",
            body=payload,
            headers=self.headers,
            callback=self.parse,
        )

    def parse(self, response):
        payload = "type=sale&province={}&pageSize=999&brand=okii"
        json_format = self.re_json.findall(response.text)[0]
        json_data = json.loads(json_format)
        data = json_data.get("data")

        if data:
            province_list = data.get("provinceList")
            if province_list:
                for province in province_list:
                    yield scrapy.Request(
                        self.get_area_url,
                        method="post",
                        body=payload.format(province),
                        headers=self.headers,
                        callback=self.parse_detail,
                    )

            else:
                raise ValueError("Json don't contain province lists")

        else:
            raise ValueError("Json don't contain data")

    def parse_detail(self, response):
        json_format = self.re_json.findall(response.text)[0]
        json_data = json.loads(json_format)
        data = json_data.get("data")

        if data:
            results = data.get("netInfo")
            if results:
                for result in results:
                    item = WebItem()
                    item["item"] = result
                    yield item
            else:
                raise ValueError("Json don't contain netInfo")
        else:
            raise ValueError("Json don't contain data")
