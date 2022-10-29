# A web spider collect shop location within mainland China

## datasource

| Brand        |         Branch         | Link                                                         | Remarks                           | 目前已经入库的 | Dimension  Source |
| :------------ | :-------------------- | :----------------------------------------------------------- | :-------------------------------- | -------------- | ----------------- |
| shuandian         |         offical web          | https://www.sundan.com/storecenter.html                      | can be crawled                  | 1              | 1                 |
| guomei         |          offical web          | https://help.gome.com.cn/question/37.html?intcmp=sy-1000043114-0 | can be crawled                        |                |                   |
|              |          api          | https://help.gome.com.cn/help/findmarkers.do                 | form-data  find store by city id  |                | 1                 |
|              |          api          | https://help.gome.com.cn/help/findCity.do?provinceId=15000000&_=1524641769587 | find city id                      |                | 1                 |
|              |          api          | https://help.gome.com.cn/question/37.html                    | Province id                       |                | 1                 |
| Suning         |          offical web          | https://vbuy.suning.com/vbuyCity.html                        |                           | 1              | 1                 |
|              |        baidu map api        | http://api.map.baidu.com/place/v2/search?query=%E8%8B%8F%E5%AE%81%E7%94%B5%E5%99%A8&region=%E6%9D%AD%E5%B7%9E&page_size=20%E7%9A%84&output=json&page_num=0&ak=qXINrzrUL7ks5fBxA7xk95eFpUPp3TmP | using baidu map api                  |                |                   |
|              |        api from front-end       | https://mois.suning.com/pc/getCityStoreVServants/010-1-cityDataCb.html?callback=cityDataCb&_=1524643166243 |                                   |                |                   |
| Apple Store        |     Official store     | https://www.aggdata.com/aggdata/complete-list-apple-retail-store-locations |               | 1              | 1                 |
|              | 合作经销商（只含北美） | https://www.aggdata.com/aggdata/complete-list-apple-specialists-distributor-locations |                | 1              |                   |
| BestBuy      |        US only         | https://www.aggdata.com/aggdata/complete-list-best-buy-locations |               | 1              |                   |
|              |      DJI internal     | excel                                                        |                                   |                | 1                 |
| DJI          |          Official web          | https://www.dji.com/zh-tw/where-to-buy                       |                  | 1              |                   |
|              |          api         | https://www.dji.com/zh-tw/api/dealers/stores/cn              |                                   |                | 1                 |
| SONY         |         us offical web         | https://www.sony.com/retailers                               | only retail partner                |                |                   |
|              |       china offical web     | https://www.sonystyle.com.cn/dealerweb/index.html            | offical store and retail partner   ） |                |                   |
| NIKON        |       china offical web         | http://www.nikon.com.cn/sc_CN/where_to_buy/image_shop.page?lang= |                                   |                |                   |
|              |         us offical web         | https://cdn-6.nikon-cdn.com/where-to-buy/nikon_img_auth_dealers.pdf |              |                |                   |
| baidu map api |          api          | http://lbsyun.baidu.com/index.php?title=webapi/guide/webservice-placeapi |                                   |                |                   |
| xiaomi       |          offical web         | https://www.mi.com/c/xiaomizhijia/                           | using google map api parsing text address      |                | 1                 |
| GoPro        |         China          | http://www.goprochina.cn/stores                              |  using google map api parsing text address      |                | 1                 |
|              |          Gobal          | https://gopro.com/store-locator                              | Coordinates                    |                | 1                 |


## Data collecting process

### libs

- using scrapy https://scrapy.org/
  - support parsing and asynchronous
  - paring HTML/JS
  - deduplicateubg links
- using MongoDB as store with json, a no sql apporach suitable for web data collection

### procedure

- for the entry point for each brand
- collect coordinates/text address then parse them using map api of all kind to deal with address only situation, then store the coordinates of the store location.
- parsing again to get the detail information of the city / province meta for each address
