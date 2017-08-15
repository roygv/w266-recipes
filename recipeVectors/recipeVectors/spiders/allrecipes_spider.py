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
            'http://allrecipes.com/recipes/15039/world-cuisine/african/north-african/egyptian/',
            'http://allrecipes.com/recipes/1827/world-cuisine/african/north-african/moroccan',
            'http://allrecipes.com/recipes/17845/world-cuisine/african/east-african/',
            'http://allrecipes.com/recipes/15035/world-cuisine/african/south-african/',
            'http://allrecipes.com/recipes/233/world-cuisine/asian/indian/',
            'http://allrecipes.com/recipes/695/world-cuisine/asian/chinese/',
            'http://allrecipes.com/recipes/702/world-cuisine/asian/thai/',
            'http://allrecipes.com/recipes/699/world-cuisine/asian/japanese/',
            'http://allrecipes.com/recipes/696/world-cuisine/asian/filipino/',
            'http://allrecipes.com/recipes/700/world-cuisine/asian/korean/',
            'http://allrecipes.com/recipes/16100/world-cuisine/asian/bangladeshi/',
            'http://allrecipes.com/recipes/15974/world-cuisine/asian/pakistani/',
            'http://allrecipes.com/recipes/698/world-cuisine/asian/indonesian/',
            'http://allrecipes.com/recipes/701/world-cuisine/asian/malaysian/',
            'http://allrecipes.com/recipes/703/world-cuisine/asian/vietnamese/',
            'http://allrecipes.com/recipes/15937/world-cuisine/middle-eastern/persian/',
            'http://allrecipes.com/recipes/1824/world-cuisine/middle-eastern/lebanese/',
            'http://allrecipes.com/recipes/1825/world-cuisine/middle-eastern/turkish/',
            'http://allrecipes.com/recipes/1826/world-cuisine/middle-eastern/israeli/',
            'http://allrecipes.com/recipes/228/world-cuisine/australian-and-new-zealander/',
            'http://allrecipes.com/recipes/236/us-recipes/',
            'http://allrecipes.com/recipes/733/world-cuisine/canadian/',
            'http://allrecipes.com/recipes/728/world-cuisine/latin-american/mexican/',
            'http://allrecipes.com/recipes/709/world-cuisine/latin-american/caribbean/cuban/',
            'http://allrecipes.com/recipes/710/world-cuisine/latin-american/caribbean/jamaican/',
            'http://allrecipes.com/recipes/711/world-cuisine/latin-american/caribbean/puerto-rican/',
            'http://allrecipes.com/recipes/2432/world-cuisine/latin-american/south-american/argentinian/',
            'http://allrecipes.com/recipes/1278/world-cuisine/latin-american/south-american/brazilian/',
            'http://allrecipes.com/recipes/1277/world-cuisine/latin-american/south-american/chilean/',
            'http://allrecipes.com/recipes/14759/world-cuisine/latin-american/south-american/colombian/',
            'http://allrecipes.com/recipes/2433/world-cuisine/latin-american/south-american/peruvian/',
            'http://allrecipes.com/recipes/718/world-cuisine/european/austrian/',
            'http://allrecipes.com/recipes/719/world-cuisine/european/belgian/',
            'http://allrecipes.com/recipes/720/world-cuisine/european/dutch/',
            'http://allrecipes.com/recipes/721/world-cuisine/european/french/',
            'http://allrecipes.com/recipes/722/world-cuisine/european/german/',
            'http://allrecipes.com/recipes/731/world-cuisine/european/greek/',
            'http://allrecipes.com/recipes/723/world-cuisine/european/italian/',
            'http://allrecipes.com/recipes/724/world-cuisine/european/portuguese/',
            'http://allrecipes.com/recipes/726/world-cuisine/european/spanish/',
            'http://allrecipes.com/recipes/727/world-cuisine/european/swiss/',
            'http://allrecipes.com/recipes/705/world-cuisine/european/uk-and-ireland/english/',
            'http://allrecipes.com/recipes/706/world-cuisine/european/uk-and-ireland/irish/',
            'http://allrecipes.com/recipes/707/world-cuisine/european/uk-and-ireland/scottish/',
            'http://allrecipes.com/recipes/708/world-cuisine/european/uk-and-ireland/welsh/',
            'http://allrecipes.com/recipes/1892/world-cuisine/european/scandinavian/danish/',
            'http://allrecipes.com/recipes/1893/world-cuisine/european/scandinavian/finnish/',
            'http://allrecipes.com/recipes/1891/world-cuisine/european/scandinavian/norwegian/',
            'http://allrecipes.com/recipes/1890/world-cuisine/european/scandinavian/swedish/',
            'http://allrecipes.com/recipes/713/world-cuisine/european/eastern-european/czech/',
            'http://allrecipes.com/recipes/714/world-cuisine/european/eastern-european/hungarian/',
            'http://allrecipes.com/recipes/715/world-cuisine/european/eastern-european/polish/',
            'http://allrecipes.com/recipes/716/world-cuisine/european/eastern-european/russian/',
                      # 'http://allrecipes.com/recipes/76/appetizers-and-snacks/',
                      #'http://allrecipes.com/recipes/88/bbq-grilling/',
                      #'http://allrecipes.com/recipes/156/bread/',
                      #'http://allrecipes.com/recipes/78/breakfast-and-brunch/',
                      #'http://allrecipes.com/recipes/79/desserts/',
                      #'http://allrecipes.com/recipes/17562/dinner/',
                      #'http://allrecipes.com/recipes/77/drinks/',
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
            u = urlparse.urlsplit(url)
            ethnic_category = u.path.strip('/').split('/')[-1]
            # example: 'english'
            full_category_tree = '/'.join([part for part in u.path.strip('/').split('/') if part != 'recipes' and part != 'world-cuisine' and not part.isdigit()])
            # example: 'european/uk-and-ireland/english'
            yield scrapy.Request(url=url, callback=self.parse, meta={'category_idx': idx, 'ethnic_category': ethnic_category, 'full_category_tree': full_category_tree})

    def create_ajax_request(self, category_url, category_idx, page_number, ethnic_category, full_category_tree):
        # https://stackoverflow.com/a/23721458/2491761
        """
        Helper function to create ajax request for next page.
        """

        u = urlparse.urlsplit(category_url)
        category_url_without_query = u.scheme + "://" + u.netloc + u.path
        ajax_template = '{url}?page={pagenum}'
        url = ajax_template.format(url=category_url_without_query, pagenum=page_number)
        # advance to next page in the category
        return scrapy.Request(url, callback=self.parse, meta={'category_idx': category_idx, 'ethnic_category': ethnic_category, 'full_category_tree': full_category_tree})

    def parse(self, response):
        """
        Parse a category page, then increment pagenum to advance to next page in that category
        """

        category_idx = response.meta.get('category_idx')
        ethnic_category = response.meta.get('ethnic_category')
        full_category_tree = response.meta.get('full_category_tree')

        if 'Please try again' in response.body:
            print('Reached end of category page')
            self.next_page = 1 # will start a new category, so reset page index to 1
            #raise CloseSpider(reason="no more pages to parse")
        else:
            print('='*15,'Extracting From Category ',response.url, ' Ethnic Category ', ethnic_category, ' Full Cat ', full_category_tree, '='*15)
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
                    yield scrapy.Request(recipe_url, callback=self.parse_item, meta={'ethnic_category': ethnic_category, 'full_category_tree': full_category_tree})
            if not found_recipe_links:
                print('***** WARNING: Could not extract recipe links from ', response.url)

            # generate request for next page within the category
            self.next_page_indices[category_idx] += 1
            yield self.create_ajax_request(response.url, category_idx, self.next_page_indices[category_idx], ethnic_category, full_category_tree)


    def parse_item(self, response):
        """
        Parse an individual recipe
        """
        ethnic_category = response.meta.get('ethnic_category')
        full_category_tree = response.meta.get('full_category_tree')

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
        l.add_value('ethnicCategory', ethnic_category)
        l.add_value('fullCategoryTree', full_category_tree)
        item = l.load_item()
        #print(item) # TODO: comment this out eventually
        yield item
