import numpy as np
import pandas as pd
from collections import defaultdict
import time
from tqdm import tqdm as ProgressBar
import six # needed for Google Cloud client
import sys
import pickle
import operator
import nltk
import zlib
import cPickle

import en # NodeBox https://www.nodebox.net/code/index.php/Linguistics#verb_conjugation

from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types

class Ingredients:
    def __init__(self):
        self.IngredientsDict=pd.read_pickle('parsedIngredients.pkl')    
        self.changed = False
    def exists(self, url):
        return url in self.IngredientsDict
    def parse(self, url, ingredients):
        if url not in self.IngredientsDict:
                ingredients = '.'.join(ingredient for ingredient in ingredients)
                if isinstance(ingredients, six.binary_type):
                    ingredients = ingredients.decode('utf-8')
                # Instantiates a plain text document.
                document = types.Document(
                     content=ingredients,
                     type=enums.Document.Type.PLAIN_TEXT)
                tokens = client.annotate_text(document, {'extract_syntax': True,}).tokens
                tokensList=list(tokens)
                self.IngredientsDict[url]=zlib.compress(cPickle.dumps(tokensList))
                self.changed = True
                return tokenList
        return cPickle.loads(zlib.decompress(self.IngredientsDict[url]))
    def close(self):
        if (self.changed == True):
            print "Writing Ingredients to disk..."
            with open('parsedIngredients.pkl', 'wb') as f:
                pickle.dump(IngredientsDict, f) 
            print "Done"
        
    
class Instructions:
    def __init__(self):
        self.InstructionsDict=pd.read_pickle('parsedInstructions.pkl')    
        self.changed = False
    def exists(self, url):
        return url in self.InstructionsDict
    def parse(self, url, ingredients):
        if url not in self.InstructionsDict:
                ingredients = '.'.join(ingredient for ingredient in ingredients)
                if isinstance(ingredients, six.binary_type):
                    ingredients = ingredients.decode('utf-8')
                # Instantiates a plain text document.
                document = types.Document(
                     content=ingredients,
                     type=enums.Document.Type.PLAIN_TEXT)
                tokens = client.annotate_text(document, {'extract_syntax': True,}).tokens
                tokensList=list(tokens)
                self.InstructionsDict[url]=zlib.compress(cPickle.dumps(tokensList))
                self.changed = True
                return tokenList
        return cPickle.loads(zlib.decompress(self.InstructionsDict[url]))
    def close(self):
        if (self.changed == True):
            print "Writing Instructions to disk..."
            with open('parsedInstructions.pkl', 'wb') as f:
                pickle.dump(InstructionsDict, f) 
            print "Done"
        
