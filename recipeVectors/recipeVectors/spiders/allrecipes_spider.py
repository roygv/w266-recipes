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
        start_urls = ['http://allrecipes.com/recipes/76/appetizers-and-snacks/',
                      'http://allrecipes.com/recipes/88/bbq-grilling/',
                      'http://allrecipes.com/recipes/156/bread/',
                      'http://allrecipes.com/recipes/78/breakfast-and-brunch/',
                      'http://allrecipes.com/recipes/79/desserts/',
                      'http://allrecipes.com/recipes/17562/dinner/',
                      'http://allrecipes.com/recipes/77/drinks/',
                      'http://allrecipes.com/recipes/1642/everyday-cooking/',
                      'http://allrecipes.com/recipes/1116/fruits-and-vegetables/',
                      'http://allrecipes.com/recipes/84/healthy-recipes/',
                      'http://allrecipes.com/recipes/85/holidays-and-events/',
                      'http://allrecipes.com/recipes/17561/lunch/',
                      'http://allrecipes.com/recipes/80/main-dish/',
                      'http://allrecipes.com/recipes/92/meat-and-poultry/',
                      'http://allrecipes.com/recipes/95/pasta-and-noodles/',
                      'http://allrecipes.com/recipes/96/salad/',
                      'http://allrecipes.com/recipes/93/seafood/',
                      'http://allrecipes.com/recipes/81/side-dish/',
                      'http://allrecipes.com/recipes/94/soups-stews-and-chili/',
                      'http://allrecipes.com/recipes/82/trusted-brands-recipes-and-tips/',
                      'http://allrecipes.com/recipes/236/us-recipes/',
                      'http://allrecipes.com/recipes/86/world-cuisine/',
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
