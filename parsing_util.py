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
import cleaning_util
 
import en # NodeBox https://www.nodebox.net/code/index.php/Linguistics#verb_conjugation

from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types

common_misspellings={'chily':'chili', 'lemongras':'lemon grass', 'gras':'grass', 'egg plant':'eggplant'}
measuring_units = [
        'teaspoon', 'teaspoons',
        't',
        'tsp', 'tsps',
        'tablespoon','tablespoons',
        'tbl',
        'tbs',
        'tbsp', 'tbsps',
        'fl', 'fluid',
        'oz', 'ozs',
        'ounce', 'ounces',
        'cup', 'cups',
        'c',
        'pint', 'pints',
        'p',
        'pt',
        'quart', 'quarts',
        'qt', 'qts',
        'q', 'qs',
        'gallon', 'gallons',
        'gal', 'gals',
        'jiggers', 'jigger',
        'ml',
        'milliliter', 'milliliters',
        'millilitre', 'millilitres',
        'cc',
        'l',
        'liter', 'liters',
        'litre', 'litres',
        'pinch', 'pinches',
        'pound', 'pounds',
        'lb', 'lbs',
        'mg', 'mgs',
        'milligram', 'milligrams',
        'milligramme', 'milligrammes',
        'g', 'gs',
        'gram', 'grams',
        'gramme', 'grammes',
        'kg', 'kgs',
        'kilogram', 'kilograms',
        'kilogramme', 'kilogrammes',
        'mm', 'mms',
        'millimeter', 'millimeters',
        'millimetre', 'millimetres',
        'cm', 'cms',
        'centimeter', 'centimeters',
        'centimetre', 'centimetres',
        'm', 'ms',
        'meter', 'meters',
        'metre', 'metres',
        'inch', 'inches',
        'in', 'ins',
        'loaf', 'loaves',
        'pouch', 'pouches',
        'wedge', 'wedges',
        'drop', 'drops',
        'amount', 'amounts',
        'bulk', 'bulks',
        'coating', 'coatings',
        'carton', 'cartons',
        'count',
        'dusting', 'dustings',
        'roll', 'rolls',
        'hint', 'hints',
        'round', 'rounds',
        'cube', 'cubes',
        'husk', 'husks',
        'envelope', 'envelopes',
        'container', 'containers',
        'dash', 'dashes',
        'bitesize', 'bitesized',
        'bite', 'sized',
        'size',
        'each',
        'taste', 'desired',
        'can', 'cans',
        'unit', 'units',
        'box', 'boxes',
        'tub', 'tubs',
        'slab', 'slabs',
        'sprig', 'sprigs',
        'stalk', 'stalks',
        'matchstick', 'matchsticks',
        'balls',
        'clove', 'cloves',
        'slice', 'slices',
        'head', 'heads',
        'spear', 'spears',
        'chunk', 'chunks',
        'piece', 'pieces',
        'jar', 'jars',
        'package', 'packages',
        'pack', 'packs',
        'packet', 'packets',
        'bunch', 'bunches',
        'tube', 'tubes',
        'jug', 'jugs',
        'bottle', 'bottles',
        'stick', 'sticks',
        'strip', 'strips',
        'bag', 'bags',
        'dash', 'dashes',
        'container', 'containers',
        'envelope', 'envelopes',
        'sleeve', 'sleeves',
        'rounds',
        'sheet', 'sheets',
        'squares',
        'semicircles', 'semicircle',
        'circles', 'circle',
        'moons', 'halfmoons',
        'strands', 'strands',
        'ribbons', 'ribbon',
        'whole',
        'extra', 'extras',
        'dozen', 'dozens',
        'half', 'halves',
        'third', 'thirds',
        'fourth', 'fourths',
        'quarter', 'quarters',
        'fifth', 'fifths',
        'eighth', 'eighths']

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
        del self.IngredientsDict
        
    
class Instructions:
    def __init__(self):
        self.InstructionsDict=pd.read_pickle('parsedInstructions.pkl')    
        self.changed = False
    def exists(self, url):
        return url in self.InstructionsDict
    def parse(self, url, instructions):
        if url not in self.InstructionsDict:
                instructions = '.'.join(instruction for instruction in instructions)
                if isinstance(instructions, six.binary_type):
                    instructions = instructions.decode('utf-8')
                # Instantiates a plain text document.
                document = types.Document(
                     content=instructions,
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
        del self.InstructionsDict
        
def get_ingredients(parsedInstructions, Ingredients, ingredientsDict, debug=0):
    """Create a more generic list of ingredients using the way they are referenced in the instructions."""
    UnreferencesIngredients = list(Ingredients)
    # Remove junk strings in the end (Should move to harvester).
    while 'Add all ingredients to list' in UnreferencesIngredients:
        UnreferencesIngredients.remove('Add all ingredients to list')
    
    # Convert ingredients to singular, lower case, replace commas with spaces
    UnreferencesIngredients = [en.noun.singular(ingredient.replace(',',' ').lower()) for ingredient in UnreferencesIngredients] 
    
    joined_ingredients = ' '.join(UnreferencesIngredients)
    
    # Tokenize ingredient list (will be used as a last resort)
    tokenized_ingredients = nltk.word_tokenize(joined_ingredients)
    tokenized_ingredients = [common_misspellings.get(word, word) for word in tokenized_ingredients]
    # Detects syntax in the document. You can also analyze HTML with:
    #   document.type == enums.Document.Type.HTML
    tokens = parsedInstructions

    # part-of-speech tags from enums.PartOfSpeech.Tag
    pos_tag = ('UNKNOWN', 'ADJ', 'ADP', 'ADV', 'CONJ', 'DET', 'NOUN', 'NUM',
               'PRON', 'PRT', 'PUNCT', 'VERB', 'X', 'AFFIX')

    short_ingredients=list()
    idx = 0
    content = list()
 
    for token in tokens:
        word = en.noun.singular(token.text.content).lower()
        # Ignore units and other stopwords, correct common mistakes
        word = common_misspellings.get(word, word)
        if word in measuring_units: 
            idx += 1
            continue #stopword
        # Parser fails many times to identify an impertive verb in the beginning of a sentence
        # So if it can be a verb and is capitalized then it is a verb.
        tag = pos_tag[token.part_of_speech.tag]
        if token.text.content.lower() != token.text.content and en.is_verb(token.text.content.lower()):
            tag = 'VERB'
        # If this was identified and a noun and can be a verb and there is a noun following
        elif (content==[] # first
             and tag == 'NOUN' # parser thinks it is a NOUN but can also be a verb
             and len(tokens) > idx+1
             and en.is_verb(token.text.content.lower()) and pos_tag[tokens[idx+1].part_of_speech.tag] in ['ADV','NOUN']):
            if (pos_tag[tokens[idx-1].part_of_speech.tag] == 'PUNCT') and token.text.content+' '+tokens[idx+1].text.content not in ingredientsDict:
                tag = 'VERB'
        else:
            tag = pos_tag[token.part_of_speech.tag]

        # There is another noun coming, collect the whole phrase.
        # PRT example: confectioners' sugar
        # CONJ example: salt and pepper
        # if (tag in ['NOUN','NUM','ADJ','PRT']) and len(tokens) > idx+1 \
        if (tag in ['NOUN','ADJ','PRT']) and len(tokens) > idx+1 \
                        and pos_tag[tokens[idx+1].part_of_speech.tag] in ['NOUN','PRT']:
            content.append(word)
            idx += 1
            continue
        else:
            content.append(token.text.content)
            # Combine the words to a phrase. Since apostrophe is a POS (PRT) I need to eliminate the extra space.
            term = ' '.join(content).replace(' \'','\'')
            if tag == 'NOUN' and term in UnreferencesIngredients: # term === Ingredient
                #print "type 1"
                tag = 'INGREDIENT'
                UnreferencesIngredients.remove(term) 
                # print(u'{}: {}'.format(tag, term))
            elif (tag == 'NOUN' and (term in tokenized_ingredients or en.noun.plural(term) in tokenized_ingredients)):
                #print "type 2"
                tag = 'INGREDIENT'
                UnreferencesIngredients.remove(
                            [ingredient for ingredient in UnreferencesIngredients 
                             if term in ingredient or term in ingredient or en.noun.plural(term) in ingredient][0]) 
            elif (' ' in term and tag == 'NOUN' and term in joined_ingredients):
                tag = 'INGREDIENT'
                ingSet = [ingredient for ingredient in UnreferencesIngredients if term in ingredient]
                if ingSet<>[]:
                    UnreferencesIngredients.remove(ingSet[0]) 
            else:
                if (' ' in term and tag == 'NOUN'):
                    if len(set([i for i in UnreferencesIngredients if len(set(term.split()) - set(i.split())) == 0])) > 0:
                        for i in set([i for i in UnreferencesIngredients if len(set(term.split()) - set(i.split())) > 0]):
                            UnreferencesIngredients.remove(i) 
                        #print "type 4"
                        tag = 'INGREDIENT'
                    if term == ' '.join([word for i in UnreferencesIngredients for word in term.split() if word in i]):
                        for i in set([i for i in UnreferencesIngredients for word in term.split() if word in i]):
                            UnreferencesIngredients.remove(i) 
                        #print "type 5"
                        tag = 'INGREDIENT'
                else:
                    # Find single nouns that apear in the remaining ingredients (tokenized)
                    if (tag == 'NOUN' and term in tokenized_ingredients):
                        for i in set([i for i in UnreferencesIngredients if term in i]):
                            UnreferencesIngredients.remove(i) 
                        #print "type 6"
                        tag = 'INGREDIENT'
                    # print(u'{}: {}'.format(tag, term))
                    pass
            content = list()
            idx += 1
        if tag == 'INGREDIENT':
            short_ingredients.append(en.noun.singular(term))
            joined_ingredients = ' '.join(UnreferencesIngredients)
            tokenized_ingredients = nltk.word_tokenize(joined_ingredients)
        if debug > 5:
            print(u'{}: {}'.format(tag, term))
    #time.sleep(.03)   # avoid Google API quota
    
    # Some ingredients were left unreferences, clean them up using brute force
    if UnreferencesIngredients <> []:
        UnreferencesIngredients = cleaning_util.extract_ingredients(UnreferencesIngredients)
    if debug > 1:
        print UnreferencesIngredients
    return(set(short_ingredients +  UnreferencesIngredients))
