# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.pipelines.images import ImagesPipeline
from scrapy import Request


class MyImagesPipeline(ImagesPipeline):

    def get_media_requests(self, item, info):
        for image_url in item['image_urls']:
            yield Request(
                image_url,
                meta={'item': item,
                      'index': item['image_urls'].index(image_url) + 1}
            )

    def file_path(self, request, response=None, info=None):
        item = request.meta['item']
        page_count = item['page'] - 1
        index = request.meta['index']
        name = item['title'].strip() + '/' + \
            str(page_count * 12 + index) + '.jpg'
        return name
