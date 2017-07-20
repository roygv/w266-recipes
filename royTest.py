import scrapy
import sys
import rescrape
import pandas as pd

# print(dir(rescrape))
# s = rescrape.site.AllRecipes("http://allrecipes.com/Recipe/Grilled-Salmon-I/Detail.aspx")
# s.write()

#import urllib2
#from bs4 import BeautifulSoup
#url='http://allrecipes.com/Recipe/Grilled-Salmon-I/Detail.aspx'
#html=urllib2.urlopen(url).read()
#soup = BeautifulSoup(html, "html.parser")
#print(soup.find("time",{"itemprop": "prepTime"}).attrs.get('datetime'))
#print(soup.find("time",{"itemprop": "cookTime"}).attrs.get('datetime'))
#print(soup.prettify())

# pd.from_csv('recipeVectors/recipeVectors/allRecipes_recipes.json')
