#!/usr/bin/env python
# encoding: utf-8
"""
AllRecipesComScraper.py

Created by Timothy Hopper on 2013-03-16.
Copyright (c) 2013 __MyCompanyName__. All rights reserved.
"""

from AbstractScraper import RecipeScraper


class AllRecipes(RecipeScraper):

    def title(self):
        return self.soup.title.string.encode("ascii", 'ignore').strip().split(" - ")[0]

    def url(self):
        return self.url

    def num_servings(self):
        # return self.soup.find("div", {"class": "servings"}).find("span", {"id": "lblYield"}).string.split(" ")[0]
        return self.soup.find("meta",{"id": "metaRecipeServings"}).attrs.get('content')

    def prep_time(self):
        # return self.get_time("prepHoursSpan") + self.get_time("prepMinsSpan")
        return self.soup.find("time",{"itemprop": "prepTime"}).attrs.get('datetime')

    def cook_time(self):
        # return self.get_time("cookHoursSpan") + self.get_time("cookMinsSpan")
        return self.soup.find("time", {"itemprop": "cookTime"}).attrs.get('datetime')

    def total_time(self):
        # return self.get_time("totalHoursSpan") + self.get_time("totalMinsSpan")
        return self.soup.find("time", {"itemprop": "totalTime"}).attrs.get('datetime')

    def ingredients(self):
        # for s in self.soup.findAll("p", {"itemprop": "ingredients"}):
        for s in self.soup.findAll("span", {"itemprop": "ingredients"}):
            yield s.get_text().encode("ascii", "ignore").strip().replace("\n", " ")

    def directions(self):
        # for s in self.soup.findAll("span", {"class": "plaincharacterwrap"}):
        for s in self.soup.find("ol",{"itemprop": "recipeInstructions"}).findAll("span", {"class": "recipe-directions__list--item"}):
                yield s.get_text().encode("ascii", "ignore").strip().replace("\n", " ")

    def note(self):
        return self.soup.find("meta",{"itemprop": "description"}).attrs.get('content')

    def get_time(self, spanName):
        find = self.soup.find("div", {"id": "divRecipeTimesContainer"}).find("span", {"id": spanName})
        if find.__class__.__name__ != "NoneType":
            return " " + find.get_text().encode("ascii")
        return ""
