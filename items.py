# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TexhrItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    sfund = scrapy.Field()
    productype = scrapy.Field()
    people = scrapy.Field()
    location = scrapy.Field()
    address = scrapy.Field()
    website = scrapy.Field()
    common = scrapy.Field()
    companyHead = scrapy.Field()

    pass
