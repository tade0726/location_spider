# 店铺地理信息收集

## 数据源整理

| Brand        |         Branch         | Link                                                         | Remarks                           | 目前已经入库的 | Dimension  Source |
| :------------ | :-------------------- | :----------------------------------------------------------- | :-------------------------------- | -------------- | ----------------- |
| 顺电         |          官网          | https://www.sundan.com/storecenter.html                      | 可以通过爬虫获取                  | 1              | 1                 |
| 国美         |          官网          | https://help.gome.com.cn/question/37.html?intcmp=sy-1000043114-0 | 可以爬出爬取                      |                |                   |
|              |          接口          | https://help.gome.com.cn/help/findmarkers.do                 | form-data  find store by city id  |                | 1                 |
|              |          接口          | https://help.gome.com.cn/help/findCity.do?provinceId=15000000&_=1524641769587 | find city id                      |                | 1                 |
|              |          接口          | https://help.gome.com.cn/question/37.html                    | Province id                       |                | 1                 |
| 苏宁         |          官网          | https://vbuy.suning.com/vbuyCity.html                        | 易购代表                          | 1              | 1                 |
|              |        百度 api        | http://api.map.baidu.com/place/v2/search?query=%E8%8B%8F%E5%AE%81%E7%94%B5%E5%99%A8&region=%E6%9D%AD%E5%B7%9E&page_size=20%E7%9A%84&output=json&page_num=0&ak=qXINrzrUL7ks5fBxA7xk95eFpUPp3TmP | 通过百度api 请求                  |                |                   |
|              |        前端接口        | https://mois.suning.com/pc/getCityStoreVServants/010-1-cityDataCb.html?callback=cityDataCb&_=1524643166243 |                                   |                |                   |
| 苹果         |     直营店（全球）     | https://www.aggdata.com/aggdata/complete-list-apple-retail-store-locations | 购买后可以持续更新                | 1              | 1                 |
|              | 合作经销商（只含北美） | https://www.aggdata.com/aggdata/complete-list-apple-specialists-distributor-locations | 购买后可以持续更新                | 1              |                   |
| BestBuy      |        US only         | https://www.aggdata.com/aggdata/complete-list-best-buy-locations | 购买后可以持续更新                | 1              |                   |
|              |      DJI 销售整理      | excel                                                        |                                   |                | 1                 |
| DJI          |          官网          | https://www.dji.com/zh-tw/where-to-buy                       | 内部获取 or 爬取                  | 1              |                   |
|              |          接口          | https://www.dji.com/zh-tw/api/dealers/stores/cn              |                                   |                | 1                 |
| SONY         |         us官网         | https://www.sony.com/retailers                               | 只有零食商的名字                  |                |                   |
|              |       china官网        | https://www.sonystyle.com.cn/dealerweb/index.html            | 基本都是代理商，小量直营店（5家） |                |                   |
| NIKON        |       china官网        | http://www.nikon.com.cn/sc_CN/where_to_buy/image_shop.page?lang= |                                   |                |                   |
|              |         us官网         | https://cdn-6.nikon-cdn.com/where-to-buy/nikon_img_auth_dealers.pdf | 只有代理商名单的pdf               |                |                   |
| 百度地图 api |          接口          | http://lbsyun.baidu.com/index.php?title=webapi/guide/webservice-placeapi |                                   |                |                   |
| 小米         |          官网          | https://www.mi.com/c/xiaomizhijia/                           | 爬虫 然后谷歌接口解析出GPS        |                | 1                 |
| GoPro        |         China          | http://www.goprochina.cn/stores                              | 爬虫 然后谷歌接口解析出GPS        |                | 1                 |
|              |          全球          | https://gopro.com/store-locator                              | 爬虫，带坐标                      |                | 1                 |


## 数据整理流程

### 工具

- 使用 scrapy https://scrapy.org/
  - 支持异步请求/解析
  - 支持HTML/JS 解析
  - 网址去重
- 数据库使用 MongoDB，方便随时调整 schema（因为根本就没有 schema）

### 流程

- 搜集店铺官网的入口
- 爬取地址后，有些店铺信息因为没有 GPS 需要通过 高德 api 利用 文本地址信息解析出 GPS
- 最后使用 djiservice 的接口解析一遍 GPS，得到标准的国家省份信息

### 顺电

- 通过官网爬虫
- 注意顺电官网给出的是经纬度(lng, lat)，不是标准的(lat, lng) 顺序
- 因为经纬度不完整，最后我用高德的 api 重新 parse 出 lat， lng

###小米

- 也是通过官网爬虫，由于没有给出经纬度信息，还要通过高德 parse 地址到 gps

###GoPro

- 国外官网数据是带 gps 的
- 国内官网没有带 gps， 也是通过高德 api parse 一次

###Apple

- 通过第三方买的

###DJI

- 爬取了DJI 官网，但是GPS数据有问题

###国美

- 官网爬取，有200个左右地址没有 GPS，同时GPS是百度的，在google map 上有偏移

###苏宁 

- 官网爬取，GPS是百度的，在google map 上有偏移