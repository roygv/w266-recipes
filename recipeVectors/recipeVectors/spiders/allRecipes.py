# -*- coding: utf-8 -*-
import scrapy


class AllrecipesSpider(scrapy.Spider):
    name = 'allRecipes'
    allowed_domains = ['allrecipes.com']
    #download_delay = 1
    start_urls = ['http://allrecipes.com/recipes/76/appetizers-and-snacks/',
                  'http://allrecipes.com/recipes/88/bbq-grilling/']

    def parse(self, response):
        print(response.url)
        pass
