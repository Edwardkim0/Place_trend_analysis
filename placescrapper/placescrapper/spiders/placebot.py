# -*- coding: utf-8 -*-
import scrapy
import time
from scrapy_splash import SplashRequest
from placescrapper.items import PlacescrapperItem
from selenium import webdriver
import urllib.parse


class PlacebotSpider(scrapy.Spider):
    name = 'placebot'
    # allowed_domains = ['https://www.google.com/maps/']
    # start_urls = ['http://https://www.google.com/maps/']
    driver = webdriver.Chrome()
    custom_settings= {
        'DOWNLOADER_MIDDLEWARES': {
            'placescrapper.middlewares.PlacescrapperSpiderMiddleware': 100
        }
    }
    base_url = "https://www.google.com/maps/"
    driver.get(base_url)
    time.sleep(1)
    search_name = '딸기 타르트'
    ## 검색어 입력
    driver.find_element_by_xpath('''//*[@id="searchboxinput"]''').send_keys(search_name)
    ## 검색 버튼 클릭
    driver.find_element_by_xpath('//*[@id="searchbox-searchbutton"]').click()
    time.sleep(4)
    ## 검색 후 현재 url 저장
    search_url = driver.current_url
    start_urls = [search_url]

    ## check box 클릭 (움직임에 따라 지도 업데이트 비활성화)
    try:
        driver.find_element_by_xpath('//*[@id="pane"]/div/div[1]/div/div/div[4]/div[3]/button').click()
    except:
        print('no checkbox')

    try:
        while driver.find_element_by_xpath('//*[@id="n7lv7yjyC35__section-pagination-button-next"]/span').is_enabled():
            driver.find_element_by_xpath('//*[@id="n7lv7yjyC35__section-pagination-button-next"]/span').click()
            time.sleep(1)
            print(driver.current_url)
            start_urls.append(driver.current_url)
    except:
        print('no page')


    # start_urls = [
    #     "https://www.google.com/maps/search/%ED%99%8D%EB%8C%80+%EB%94%B8%EA%B8%B0+%ED%83%80%EB%A5%B4%ED%8A%B8/@37.5307577,126.9220613,13.93z"
    #     , "https://www.google.com/maps/search/%EC%97%AC%EC%9D%98%EB%8F%99+%EB%94%B8%EA%B8%B0+%ED%83%80%EB%A5%B4%ED%8A%B8/@37.5307548,126.9220612,13z/data=!3m1!4b1"
    # ]
    start_urls = list(set(start_urls))
    print('#'*100 + ' all urls ' + '#'*100)
    for url in start_urls:
        print(url)

    # def start_requests(self):
    #     for url in self.start_urls:
    #         yield SplashRequest(
    #             url=url,
    #             callback=self.parse,
    #             args={
    #                 'wait': 0.5,
    #                 'timeout': 120,
    #             },
    #             endpoint='render.html'
    #         )

    def parse(self, response):
        names = response.xpath('//*[@id="pane"]/div/div[1]/div/div/div[4]/div[1]/div/div[1]/div[1]/div[1]/div[1]/div[2]/h3/span').extract()
        addresses = response.xpath('//*[@id="pane"]/div/div[1]/div/div/div[4]/div[1]/div/div[1]/div[1]/div[2]/span[6]').extract()
        kinds = response.xpath('//*[@id="pane"]/div/div[1]/div/div/div[4]/div[1]/div/div[1]/div[1]/div[2]/span[4]').extract()
        scores = response.xpath('//*[@id="pane"]/div/div[1]/div/div/div[4]/div[1]/div/div[1]/div[1]/div[1]/div[1]/div[2]/span[3]/span[1]/span[1]/span').extract()
        # print('*' * 100)
        #
        # for item in zip(names, addresses, kinds, scores):
        #     place_item = {}
        #     place_item['name'] = item[0].strip()
        #     place_item['address'] = item[1].strip()
        #     place_item['kind'] = item[2].strip()
        #     place_item['score'] = item[3].strip()
        #
        #     print('*' * 100)
        #     print(place_item)
        #     time.sleep(1)
        #     yield place_item
        print('#' * 100 + ' url ' + response.url.split("/")[-2] + '#' * 100 + '\n\n')
        time.sleep(1)

        # print('*' * 100)
        for item in zip(names, addresses, kinds, scores):
            place_item = PlacescrapperItem()
            place_item['name'] = item[0].strip()
            place_item['address'] = item[1].strip()
            place_item['kind'] = item[2].strip()
            place_item['score'] = item[3].strip()

            print('*' * 100)
            # print(place_item)
            time.sleep(0.01)
            yield place_item
    #
    # def parse(self):
    #     """
    #     Get URL of all URLs from the alphabet letters (breed_urls)
    #     :return:
    #     """
    #     breed_urls = 'parse the urls'
    #     for url in breed_urls:
    #         yield scrapy.Request(url=url, callback=self.parse_sub_urls)
    #
    # def parse_sub_urls(self, response):
    #     """
    #     Get URL of all SubUrls from the subPage (sub_urls)
    #     :param response:
    #     :return:
    #     """
    #     sub_urls= 'parse the urls'
    #     for url in sub_urls:
    #         yield scrapy.Request(url=url, callback=self.parse_details)
    #
    # def parse_details(self, response):
    #     """
    #     Get the final details from the listing page
    #     :param response:
    #     :return:
    #     """
    #     names = response.xpath('//*[@id="pane"]/div/div[1]/div/div/div[4]/div[1]/div/div[1]/div[1]/div[1]/div[1]/div[2]/h3/span').extract()
    #     addresses = response.xpath('//*[@id="pane"]/div/div[1]/div/div/div[4]/div[1]/div/div[1]/div[1]/div[2]/span[6]').extract()
    #     kinds = response.xpath('//*[@id="pane"]/div/div[1]/div/div/div[4]/div[1]/div/div[1]/div[1]/div[2]/span[4]').extract()
    #     scores = response.xpath('//*[@id="pane"]/div/div[1]/div/div/div[4]/div[1]/div/div[1]/div[1]/div[1]/div[1]/div[2]/span[3]/span[1]/span[1]/span').extract()
    #     for item in zip(names, addresses, kinds, scores):
    #         scrapped_info = {
    #             'name' : item[0].strip(),
    #             'address' : item[1].strip(),
    #             'kind' : item[2].strip(),
    #             'score' : item[3].strip(),
    #         }
    #         print('*' * 100)
    #         print(scrapped_info)
    #         yield scrapped_info
