# -*- coding: utf-8 -*-

# Scrapy settings for shop_locations project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html
import os
from shop_locations.utils import AESCipher


BOT_NAME = "shop_locations"

SPIDER_MODULES = ["shop_locations.spiders"]
NEWSPIDER_MODULE = "shop_locations.spiders"

# Obey robots.txt rules
ROBOTSTXT_OBEY = False
DOWNLOAD_DELAY = 0.5

# setting for mongodb
MONGO_DATABASE = "shops_geo"
MONGO_URI = "mongodb://localhost:27017/"

ITEM_PIPELINES = {
    "shop_locations.pipelines.ItemPipeline": 700,
    "shop_locations.pipelines.WandaStorePipeline": 700
}

# CRYPKEY
CRYPKEY = os.getenv("CRYPKEY")
SAFE_TOOL = AESCipher(CRYPKEY)
