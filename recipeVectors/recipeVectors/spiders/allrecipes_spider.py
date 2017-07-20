# -*- coding: utf-8 -*-

import scrapy
from scrapy import Selector
from recipeVectors.items import RecipevectorsItem
from scrapy.loader import ItemLoader

class AllrecipesSpider(scrapy.Spider):
    name = 'allRecipes'
    allowed_domains = ['allrecipes.com']
    #download_delay = 1

    crawledCategoriesUrls = []
    crawledRecipesUrls = []
    savedRecipes = []
    numCrawled = 0

    def start_requests(self):
        start_urls = ['http://allrecipes.com/recipes/88/bbq-grilling/'
            # ,'http://allrecipes.com/recipes/88/bbq-grilling/'
        ]
        # 'http://allrecipes.com/recipes/76/appetizers-and-snacks/',

        for url in start_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):

        if response.url.find('http://allrecipes.com/recipes/') == 0:
            print('='*30,'Extracting From Category ',response.url,'='*30)
            print('Starting URL Extraction')
            responseHTML = response.body
            sel = Selector(text=responseHTML, type="html")
            for url in sel.xpath('//a[contains(@href,"/recipe")]/@href').extract():
                if url.find('/recipes/') == 0 and not url in self.crawledCategoriesUrls:
                    self.crawledCategoriesUrls.append(url)
                if url.find('/recipe/') == 0 and not url in self.crawledRecipesUrls:
                    self.crawledRecipesUrls.append(url)
            print('crawledCategoriesUrls count:', len(self.crawledCategoriesUrls))
            print(self.crawledCategoriesUrls)
            print
            print('crawledRecipesUrls count:', len(self.crawledRecipesUrls))
            print(self.crawledRecipesUrls)

            if len(self.crawledRecipesUrls)>0:
                baseUrl = 'http://allrecipes.com'
                for item in self.crawledRecipesUrls:
                    url = baseUrl + item
                    print('='*30,'Starting to extract from Recipe: ', url ,'='*30)
                    yield scrapy.Request(url=url, callback=self.parse)
            print('='*30,'Finished Extracting From Category ',response.url,'='*30)
        if response.url.find('http://allrecipes.com/recipe/') == 0:
            l = ItemLoader(item=RecipevectorsItem(), response=response)
            nameXpath = '//h1[re:test(@itemprop, "name")]//text()'
            totalTimeXPath = '//time[re:test(@itemprop, "totalTime")]//@datetime'
            ratingXpath = '//span[re:test(@itemprop,"aggregateRating")]//meta[re:test(@itemprop, "ratingValue")]//@content'
            ratingCountXpath = '//span[re:test(@itemprop,"aggregateRating")]//meta[re:test(@itemprop, "reviewCount")]//@content'
            ingredXpath = '//span[re:test(@class, "recipe-ingred_txt ")]//text()'
            instructionXpath = '//span[re:test(@class, "directions__list--item")]//text()'

            l.add_value('url', response.url)
            l.add_xpath('name', nameXpath)
            l.add_xpath('rating', ratingXpath)
            l.add_xpath('cookingTime', totalTimeXPath)
            l.add_xpath('ratingCount', ratingCountXpath)
            l.add_xpath('ingredients', ingredXpath)
            l.add_xpath('instructionSteps', instructionXpath)
            item = l.load_item()
            print(item)
            yield item

        # self.__extractURLs(response.body)
        # page = response.url.split("/")[-2]
        # filename = './recipes/allrecipes-%s.html' % page
        # with open(filename, 'wb') as f:
        #     f.write(response.body)
