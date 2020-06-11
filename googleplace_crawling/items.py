# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class GoogleplaceCrawlingItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field() # 이름
    category = scrapy.Field()  # 카테고리
    address = scrapy.Field()  # 주소
    score = scrapy.Field()  # 평점
    review = scrapy.Field()  # 리뷰
    pass
