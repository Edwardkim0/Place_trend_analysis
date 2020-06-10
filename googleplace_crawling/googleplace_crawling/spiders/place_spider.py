# -*- coding: utf-8 -*-

import scrapy
import time
import csv
from googleplace_crawling.googleplace_crawling.items import GoogleplaceCrawlingItem


class GooglePlaceSpider(scrapy.Spider):
    name = "googlePlaceCrawler"
    allowed_domains = ["https://www.google.com/maps/search/"]
    start_urls = [
        "https://www.google.com/maps/search/%ED%99%8D%EB%8C%80+%EB%94%B8%EA%B8%B0+%ED%83%80%EB%A5%B4%ED%8A%B8/@37.5307577,126.9220613,13.93z"
        , "https://www.google.com/maps/search/%EC%97%AC%EC%9D%98%EB%8F%99+%EB%94%B8%EA%B8%B0+%ED%83%80%EB%A5%B4%ED%8A%B8/@37.5307548,126.9220612,13z/data=!3m1!4b1"
    ]
    def parse(self, response):
        item = GoogleplaceCrawlingItem()

        item['name'] = response.xpath('//*[@id="cSub"]/div[1]/em/a/img/@alt').extract()[0]
        item['category'] = '정치'
        item['address'] = response.xpath('//*[@id="cSub"]/div[1]/h3/text()').extract()[0]
        item['score'] = response.xpath('/html/head/meta[contains(@property, "og:regDate")]/@content').extract()[0][:8]
        item['review'] = response.xpath(
            '//*[@id="harmonyContainer"]/section/div[contains(@dmcf-ptype, "general")]/text()').extract() \
                          + response.xpath(
            '//*[@id="harmonyContainer"]/section/p[contains(@dmcf-ptype, "general")]/text()').extract()

        print('*' * 100)
        print(item['title'])
        print(item['date'])

        time.sleep(5)

        yield item