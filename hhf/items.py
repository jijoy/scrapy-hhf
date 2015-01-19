# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class HhfItem(scrapy.Item):
    # define the fields for your item here like:
    video_title = scrapy.Field()
    image_url = scrapy.Field()
    image_path = scrapy.Field()
    artist = scrapy.Field()
    added_date = scrapy.Field()
    category = scrapy.Field()
    views = scrapy.Field()
    url = scrapy.Field()
    embed_url = scrapy.Field()
