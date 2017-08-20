# -*- coding: utf-8 -*-
import scrapy
from scrapy import Selector
from recipeVectors.items import RecipevectorsItem
from scrapy.loader import ItemLoader
from scrapy.exceptions import CloseSpider

import urlparse

class EpicuriousSpider(scrapy.Spider):
    name = 'epicurious'
    allowed_domains = ['epicurious.com']

    crawledCategoriesUrls = []
    crawledRecipesUrls = []
    savedRecipes = []
    numCrawled = 0

    next_page = 1

    def start_requests(self):
        labels = [
            'African',
            'American',
            'Asian',
            'British',
            'Cajun-Creole',
            'Californian',
            'Caribbean',
            'Central-South-American',
            'Chinese',
            'Cuban',
            'Eastern-European',
            'English',
            'European',
            'French',
            'German',
            'Greek',
            'Indian',
            'Irish',
            'Italian',
            'Italian-American',
            'Japanese',
            'Jewish',
            'Korean',
            'Latin-American',
            'Mediterranean',
            'Mexican',
            'Middle-Eastern',
            'Moroccan',
            #'Nuevo-Latino', # "fusion" category that will be too hard to categorize
            'Scandinavian',
            'South-American',
            'South-Asian',
            'Southeast Asian',
            'Southern',
            'Southwestern',
            'Spanish-Portuguese',
            'Tex-Mex',
            'Thai',
            'Turkish',
            'Vietnamese',        
        ]
        start_urls = ['http://www.epicurious.com/search?cuisine='+label.lower() for label in labels]
        self.next_page_indices = [ 1 for url in start_urls ]
        
        for idx, (ethnic_category, url) in enumerate(zip(labels, start_urls)):
            u = urlparse.urlsplit(url)
            yield scrapy.Request(url=url, callback=self.parse, meta={'category_idx': idx, 'ethnic_category': ethnic_category})
        
    def create_ajax_request(self, category_url, category_idx, page_number, ethnic_category):
        # https://stackoverflow.com/a/23721458/2491761
        """
        Helper function to create ajax request for next page.
        """

        u = urlparse.urlsplit(category_url)
        category_url_without_query = u.scheme + "://" + u.netloc + u.path
        ajax_template = '{url}?cuisine={ethniccategory}&page={pagenum}'
        url = ajax_template.format(url=category_url_without_query, ethniccategory=ethnic_category, pagenum=page_number)
        # advance to next page in the category
        return scrapy.Request(url, callback=self.parse, meta={'category_idx': category_idx, 'ethnic_category': ethnic_category})

    def parse(self, response):
        """
        Parse a category page, then increment pagenum to advance to next page in that category
        """
        
        # if does not include 'recipe-panel', hit empty page

        category_idx = response.meta.get('category_idx')
        ethnic_category = response.meta.get('ethnic_category')

        if 'recipe-panel' not in response.body:
            print('Reached end of category page')
            self.next_page = 1 # will start a new category, so reset page index to 1
            #raise CloseSpider(reason="no more pages to parse")
        else:
            print('='*15,'Extracting From Category ',response.url, ' Ethnic Category ',ethnic_category, '='*15)
            print('Starting URL Extraction')
            responseHTML = response.body
            sel = Selector(text=responseHTML, type="html")
            found_recipe_links = False
            for url in sel.xpath('//*[@id="react-app"]/span/section/div/article/div[@class="recipe-panel "]/a/@href').extract():
                if not url in self.crawledRecipesUrls:
                    self.crawledRecipesUrls.append(url)
                    recipe_url = urlparse.urljoin(response.url, url)
                    print('Found recipe URL ', recipe_url)
                    found_recipe_links = True
                    yield scrapy.Request(recipe_url, callback=self.parse_item, meta={'ethnic_category': ethnic_category})
            if not found_recipe_links:
                print('***** WARNING: Could not extract recipe links from ', response.url)

            # generate request for next page within the category
            self.next_page_indices[category_idx] += 1
            yield self.create_ajax_request(response.url, category_idx, self.next_page_indices[category_idx], ethnic_category)
            

    def parse_item(self, response):
        """
        Parse an individual recipe
        """
        ethnic_category = response.meta.get('ethnic_category')

        l = ItemLoader(item=RecipevectorsItem(), response=response)
        nameXpath = '//*[@class="title-source"]/h1[@itemprop="name"]//text()'
        #totalTimeXPath = '//time[re:test(@itemprop, "totalTime")]//@datetime'
        #descriptionXPath = '//meta[re:test(@itemprop,"description")]//@content'
        #ratingXpath = '//span[re:test(@itemprop,"aggregateRating")]//meta[re:test(@itemprop, "ratingValue")]//@content'
        #ratingCountXpath = '//span[re:test(@itemprop,"aggregateRating")]//meta[re:test(@itemprop, "reviewCount")]//@content'
        ingredXpath = '//li[@class="ingredient"]//text()'
        instructionXpath = '//li[re:test(@class, "preparation-step")]//text()'
        #categoriesXPath = '//img[re:test(@data-container, "relatedCategories")]//@title'
        recipeCollectionsXpath = '//*[@id="additional-info-panels"]/div/div/dl/a/@href'
        #relatedCategoriesXpath = '//a[re:test(@class, "recipe__relatedCategoryLink")]//text()'

        l.add_value('url', response.url)
        l.add_xpath('name', nameXpath)
        #l.add_xpath('rating', ratingXpath)
        #l.add_xpath('description', descriptionXPath)
        #l.add_xpath('cookingTime', totalTimeXPath)
        #l.add_xpath('ratingCount', ratingCountXpath)
        l.add_xpath('ingredients', ingredXpath)
        l.add_xpath('instructionSteps', instructionXpath)
        #l.add_xpath('categories', categoriesXPath)
        l.add_value('ethnicCategory', ethnic_category)
        l.add_xpath('recipeCollections', recipeCollectionsXpath)
        #l.add_xpath('relatedCategories', relatedCategoriesXpath)
        
        item = l.load_item()
        #print(item) # TODO: comment this out eventually
        yield item

