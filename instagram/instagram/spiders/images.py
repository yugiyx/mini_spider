# -*- coding: utf-8 -*-
import json
import scrapy
from ..items import ImageItem


class ImagesSpider(scrapy.Spider):
    name = 'images'
    allowed_domains = ['instagram.com']
    start_urls = ['https://www.instagram.com/kuleko/']

    def parse(self, response):
        images = ImageItem()
        json_data = json.loads(response.css('script')[3].extract()[52:-10])
        json_data = json_data["entry_data"]["ProfilePage"][0]["graphql"]["user"]["edge_owner_to_timeline_media"]
        items = json_data["page_info"]
        end_cursor = items['end_cursor']
        has_next_page = items['has_next_page']
        items = json_data["edges"]
        # images['id'] = items[0]['node']['owner']['id']
        images['title'] = items[0]['node']['owner']['username']
        images['image_urls'] = [item['node']['display_url'] for item in items]
        return images

        if has_next_page:
            next_url = 
query_hash = '5b0222df65d7f6659c9b82246780caa7'
variables = {"id": "1413437914", "first": 50, "after": "QVFDVzFIbWc5dkRhcmtNcEl2VEt2bnZOZS14bmgzYnk1MkR1RElZUm85MlBvTFJ5Qkp1RG5CbjFEZHBsb1ZwQV9jSEo3ZTkxamVHREVlcmEtcGx2ODFWag=="}