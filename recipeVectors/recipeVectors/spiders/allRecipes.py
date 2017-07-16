# -*- coding: utf-8 -*-
import scrapy


class AllrecipesSpider(scrapy.Spider):
    name = 'allRecipes'
    allowed_domains = ['allrecipes.com']
    start_urls = ['http://allrecipes.com/']

    def parse(self, response):
        print(response.url)
        pass
