# -*- coding: utf-8 -*-
import json
import hashlib
import scrapy
from ..items import ImageItem


class ImagesSpider(scrapy.Spider):
    name = 'images'
    allowed_domains = ['instagram.com']
    start_urls = ['https://www.instagram.com/kuleko/']

    def parse(self, response):
        images = ImageItem()
        json_data = json.loads(response.css('script')[3].extract()[52:-10])
        json_data = json_data["entry_data"]["ProfilePage"][0][
            "graphql"]["user"]["edge_owner_to_timeline_media"]
        page_info = json_data["page_info"]
        end_cursor = page_info['end_cursor']
        has_next_page = page_info['has_next_page']
        edges = json_data["edges"]
        # images['id'] = items[0]['node']['owner']['id']
        images['title'] = edges[0]['node']['owner']['username']
        images['image_urls'] = [item['node']['display_url'] for item in edges]
        yield images

        if has_next_page:
            print('还有后文')
            print(end_cursor)
            yield scrapy.Request(next_url, headers=headers)

    def hash_str(self, strInfo):
        h = hashlib.md5()
        h.update(strInfo.encode("utf-8"))
        return h.hexdigest()
