#!/usr/bin/env python
# encoding: utf-8
import json
from AbstractScraper import RecipeScraper


class FoodCom(RecipeScraper):

    def title(self):
        # return self.soup.title.string.encode("ascii", 'ignore').strip().split(" - ")[0]
        js = self.soup.find("div", {"class": "fd-page-feed"}).find("script", {"type": "application/ld+json"}).contents[0]
        l = json.loads(js)
        title = l["name"]
        return title

    def url(self):
        return self.url

    def num_servings(self):
        return self.soup.find("li", {"id": "yield-servings"}).find("span", {"class": "count"}).contents[0]

    def prep_time(self):
        js = self.soup.find("div", {"class": "fd-page-feed"}).find("script", {"type": "application/ld+json"}).contents[0]
        l = json.loads(js)
        duration = l["prepTime"]
        return self.parse_duration(duration)

    def cook_time(self):
        js = self.soup.find("div", {"class": "fd-page-feed"}).find("script", {"type": "application/ld+json"}).contents[0]
        l = json.loads(js)
        duration = l["cookTime"]
        return self.parse_duration(duration)

    def total_time(self):
        js = self.soup.find("div", {"class": "fd-page-feed"}).find("script", {"type": "application/ld+json"}).contents[0]
        l = json.loads(js)
        duration = l["totalTime"]
        return self.parse_duration(duration)

    def ingredients(self):
        js = self.soup.find("div", {"class": "fd-page-feed"}).find("script", {"type": "application/ld+json"}).contents[0]
        l = json.loads(js)
        ingredients = l["recipeIngredient"]
        for ing in ingredients:
            yield ing

    def directions(self):
        js = self.soup.find("div", {"class": "fd-page-feed"}).find("script", {"type": "application/ld+json"}).contents[0]
        l = json.loads(js)
        directions = l["recipeInstructions"].replace('. ','.').split('.')
        for step in directions:
            if len(step)>1:
                yield step

    def note(self):
        js = self.soup.find("div", {"class": "fd-page-feed"}).find("script", {"type": "application/ld+json"}).contents[0]
        l = json.loads(js)
        description = l["description"]
        return description
