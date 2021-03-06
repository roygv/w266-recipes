# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import Join, MapCompose, TakeFirst


class RecipevectorsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    url = scrapy.Field(output_processor=TakeFirst())
    name = scrapy.Field(output_processor=TakeFirst())
    description = scrapy.Field(output_processor=TakeFirst())
    rating = scrapy.Field(output_processor=TakeFirst())
    cookingTime = scrapy.Field(output_processor=TakeFirst())
    ratingCount = scrapy.Field(output_processor=TakeFirst())
    ingredients = scrapy.Field()
    instructionSteps = scrapy.Field()
    categories = scrapy.Field()
    siteCategory = scrapy.Field(output_processor=TakeFirst())
    ethnicCategory = scrapy.Field(output_processor=TakeFirst())
    recipeCollections = scrapy.Field()
    relatedCategories = scrapy.Field()
