# -*- coding: utf-8 -*-
import scrapy


class ImagesSpider(scrapy.Spider):
    name = 'images'
    allowed_domains = ['instagram.com']
    start_urls = ['http://instagram.com/']

    def parse(self, response):
        pass
