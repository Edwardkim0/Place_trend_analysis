# -*- coding: utf-8 -*-

import scrapy
import time
from googleplace_crawling.items import GoogleplaceCrawlingItem
from scrapy_splash import SplashRequest

class GooglePlaceSpider(scrapy.Spider):
    name = "googlePlaceCrawler"
    allowed_domains = ["https://www.google.com/maps/search/"]
    start_urls = [
        "https://www.google.com/maps/search/%ED%99%8D%EB%8C%80+%EB%94%B8%EA%B8%B0+%ED%83%80%EB%A5%B4%ED%8A%B8/@37.5307577,126.9220613,13.93z"
        , "https://www.google.com/maps/search/%EC%97%AC%EC%9D%98%EB%8F%99+%EB%94%B8%EA%B8%B0+%ED%83%80%EB%A5%B4%ED%8A%B8/@37.5307548,126.9220612,13z/data=!3m1!4b1"
    ]

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(
                url=url, callback=self.parse, endpoint='render.html'
            )

    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = 'quotes-%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)

        item = GoogleplaceCrawlingItem()

        item['address'] = response.xpath('//*[@id="pane"]/div/div[1]/div/div/div[4]/div[1]/div/div[1]/div[1]/div[2]/span[6]').extract()[0]

        print('*' * 100)
        print(item['address'])

        time.sleep(5)

        yield item