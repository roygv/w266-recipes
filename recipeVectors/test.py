from recipeVectors.items import RecipevectorsItem
from scrapy.loader import ItemLoader
from scrapy import Selector

s = ''
with open('./recipes/allrecipes-marinated-pork-tenderloin.html', 'r') as f:
    for line in f:
        s+= line
# print(s)

sel = Selector(text=s, type="html")
# for scope in sel.xpath('//a[contains(@href,"/recipe/")]/@href').extract():
#     print(scope)
#

# print(recipe)

name=sel.xpath('//h1[re:test(@itemprop, "name")]//text()').extract()[0]
totalTime=sel.xpath('//time[re:test(@itemprop, "totalTime")]//@datetime').extract()[0]
aggregateRating= sel.xpath('//span[re:test(@itemprop,"aggregateRating")]')
description= sel.xpath('//meta[re:test(@itemprop,"description")]//@content').extract()[0]


stars = aggregateRating.xpath('.//meta[re:test(@itemprop, "ratingValue")]//@content').extract()[0]
ratingcounts=aggregateRating.xpath('.//meta[re:test(@itemprop, "reviewCount")]//@content').extract()[0]
print 'description', description

print(name)
print(stars)
print(ratingcounts)
print('='*100)

ingred = []
for idx,item in enumerate(sel.xpath('//span[re:test(@class, "recipe-ingred_txt ")]//text()').extract()):
    print(idx,item)
    ingred.append(item)
print('='*100)

categories = []
for idx,item in enumerate(sel.xpath('//img[re:test(@data-container, "relatedCategories")]//@title').extract()):
    print(idx,item)
    categories.append(item)
print('='*100)

instructions = []
for idx,item in enumerate(sel.xpath('//span[re:test(@class, "directions__list--item")]//text()').extract()):
    print(idx,item)
    instructions.append(item)
rvi = RecipevectorsItem()
rvi['name'] = name
rvi['cookingTime'] = totalTime
rvi['rating'] = stars
rvi['ratingCount'] = ratingcounts
rvi['ingredients'] = ingred
rvi['instructionSteps'] = instructions
print(rvi)

import json
from scrapy.utils.serialize import ScrapyJSONEncoder
obj = {}
obj['blarg'] = 'blarg'
testJson = json.dumps(obj)
print(testJson)
