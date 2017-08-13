# -*- coding: utf-8 -*-

import scrapy
from scrapy import Selector
from recipeVectors.items import RecipevectorsItem
from scrapy.loader import ItemLoader
from scrapy.exceptions import CloseSpider

import urlparse

class AllrecipesSpider(scrapy.Spider):
    name = 'allRecipes'
    allowed_domains = ['allrecipes.com']
    #download_delay = 1

    crawledCategoriesUrls = []
    crawledRecipesUrls = []
    savedRecipes = []
    numCrawled = 0

    next_page = 1

    def start_requests(self):
        start_urls = [
                      # Tony
                       'http://allrecipes.com/recipes/76/appetizers-and-snacks/',
                      'http://allrecipes.com/recipes/88/bbq-grilling/',
                      'http://allrecipes.com/recipes/156/bread/',
                      'http://allrecipes.com/recipes/78/breakfast-and-brunch/',
                      'http://allrecipes.com/recipes/79/desserts/',
                      'http://allrecipes.com/recipes/17562/dinner/',
                      'http://allrecipes.com/recipes/77/drinks/',
                      # Roy
                      #'http://allrecipes.com/recipes/1642/everyday-cooking/',
                      #'http://allrecipes.com/recipes/1116/fruits-and-vegetables/',
                      #'http://allrecipes.com/recipes/84/healthy-recipes/',
                      #'http://allrecipes.com/recipes/85/holidays-and-events/',
                      #'http://allrecipes.com/recipes/17561/lunch/',
                      #'http://allrecipes.com/recipes/80/main-dish/',
                      #'http://allrecipes.com/recipes/92/meat-and-poultry/',
                      #'http://allrecipes.com/recipes/95/pasta-and-noodles/',
                      # Chu
                      #'http://allrecipes.com/recipes/96/salad/',
                      #'http://allrecipes.com/recipes/93/seafood/',
                      #'http://allrecipes.com/recipes/81/side-dish/',
                      #'http://allrecipes.com/recipes/94/soups-stews-and-chili/',
                      #'http://allrecipes.com/recipes/82/trusted-brands-recipes-and-tips/',
                      #'http://allrecipes.com/recipes/236/us-recipes/',
                      #'http://allrecipes.com/recipes/86/world-cuisine/',
        ]

        self.next_page_indices = [ 1 for url in start_urls ]

        for idx, url in enumerate(start_urls):
            yield scrapy.Request(url=url, callback=self.parse, meta={'category_idx': idx})

    def create_ajax_request(self, category_url, category_idx, page_number):
        # https://stackoverflow.com/a/23721458/2491761
        """
        Helper function to create ajax request for next page.
        """

        u = urlparse.urlsplit(category_url)
        category_url_without_query = u.scheme + "://" + u.netloc + u.path
        ajax_template = '{url}?page={pagenum}'
        url = ajax_template.format(url=category_url_without_query, pagenum=page_number)
        # advance to next page in the category
        return scrapy.Request(url, callback=self.parse, meta={'category_idx': category_idx})

    def parse(self, response):
        """
        Parse a category page, then increment pagenum to advance to next page in that category
        """

        category_idx = response.meta.get('category_idx')

        if 'Please try again' in response.body:
            print('Reached end of category page')
            self.next_page = 1 # will start a new category, so reset page index to 1
            #raise CloseSpider(reason="no more pages to parse")
        else:
            print('='*30,'Extracting From Category ',response.url,'='*30)
            print('Starting URL Extraction')
            responseHTML = response.body
            sel = Selector(text=responseHTML, type="html")
            found_recipe_links = False
            for url in sel.xpath('body/div[@class="slider-container"]/div[@class="site-content"]/div[@class="container-content body-content"]/section/div/section[@id="grid"]/article/a/img/../@href').extract():
                if url.find('/recipe/') == 0 and not url in self.crawledRecipesUrls:
                    self.crawledRecipesUrls.append(url)
                    recipe_url = urlparse.urljoin(response.url, url)
                    print('Found recipe URL ', recipe_url)
                    found_recipe_links = True
                    yield scrapy.Request(recipe_url, callback=self.parse_item)
            if not found_recipe_links:
                print('***** WARNING: Could not extract recipe links from ', response.url)

            # generate request for next page within the category
            self.next_page_indices[category_idx] += 1
            yield self.create_ajax_request(response.url, category_idx, self.next_page_indices[category_idx])


    def parse_item(self, response):
        """
        Parse an individual recipe
        """
        l = ItemLoader(item=RecipevectorsItem(), response=response)
        nameXpath = '//h1[re:test(@itemprop, "name")]//text()'
        totalTimeXPath = '//time[re:test(@itemprop, "totalTime")]//@datetime'
        descriptionXPath = '//meta[re:test(@itemprop,"description")]//@content'
        ratingXpath = '//span[re:test(@itemprop,"aggregateRating")]//meta[re:test(@itemprop, "ratingValue")]//@content'
        ratingCountXpath = '//span[re:test(@itemprop,"aggregateRating")]//meta[re:test(@itemprop, "reviewCount")]//@content'
        ingredXpath = '//span[re:test(@class, "recipe-ingred_txt ")]//text()'
        instructionXpath = '//span[re:test(@class, "directions__list--item")]//text()'
        categoriesXPath = '//img[re:test(@data-container, "relatedCategories")]//@title'

        l.add_value('url', response.url)
        l.add_xpath('name', nameXpath)
        l.add_xpath('rating', ratingXpath)
        l.add_xpath('description', descriptionXPath)
        l.add_xpath('cookingTime', totalTimeXPath)
        l.add_xpath('ratingCount', ratingCountXpath)
        l.add_xpath('ingredients', ingredXpath)
        l.add_xpath('instructionSteps', instructionXpath)
        l.add_xpath('categories', categoriesXPath)
        item = l.load_item()
        #print(item) # TODO: comment this out eventually
        yield item
