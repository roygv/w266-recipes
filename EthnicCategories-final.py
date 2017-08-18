
# coding: utf-8

# In[12]:

#get_ipython().magic(u'matplotlib inline')
import matplotlib.pyplot as plt

import string
from os import listdir
import os
import errno
import subprocess
from collections import defaultdict
import operator
import re
import pickle
from collections import OrderedDict
import six # needed for Google Cloud client

import unidecode

import numpy as np
import pandas as pd
import scipy.sparse

from tqdm import tqdm, tqdm_pandas

from scipy.sparse.csr import csr_matrix
from sklearn.decomposition import TruncatedSVD
from sklearn.feature_extraction.text import CountVectorizer,TfidfTransformer
from sklearn.cluster import KMeans, MiniBatchKMeans
from sklearn.pipeline import Pipeline
from sklearn.metrics import confusion_matrix, classification_report, accuracy_score
from sklearn import preprocessing

from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.layers import Dropout
from keras.layers.embeddings import Embedding
from keras.preprocessing import sequence
from keras.preprocessing.text import Tokenizer, text_to_word_sequence
from keras.preprocessing.sequence import pad_sequences
from keras.utils import np_utils
from keras.models import model_from_json

from sklearn.model_selection import train_test_split
from keras.preprocessing import sequence
from sklearn.manifold import TSNE

import nltk


# In[2]:

#get_ipython().magic(u'load_ext autoreload')
#get_ipython().magic(u'autoreload 2')


# In[3]:

try:
    df = pd.read_json('ethnic_categories.json', dtype={})
except ValueError:
    df = pd.read_json(os.path.join('recipes', 'ethnic_categories.json'), dtype={})


# In[4]:

print 'dataset size:', len(df)
df.sample(5)


# In[5]:

df[['url']].values[5883]


# In[6]:

#df[['ethnicCategory']].values.nunique()
df['ethnicCategory'].value_counts()


# In[7]:

cat_mapping_lines = """argentinian  latin_american
australian-and-new-zealander  north_european
austrian  north_european
bangladeshi  south_asian
belgian  north_european
brazilian  latin_american
canadian  north_american
chilean  latin_american
chinese  east_asian
colombian  latin_american
cuban  latin_american
czech  east_european
danish  north_european
dutch  north_european
east-african  african
egyptian  african
english  north_european
filipino  southeast_asian
finnish  north_european
french  north_european
german  north_european
greek  middle_eastern
hungarian  east_european
indian  south_asian
indonesian  southeast_asian
irish  north_european
israeli  middle_eastern
italian  south_european
jamaican  latin_american
japanese  east_asian
korean  east_asian
lebanese  middle_eastern
malaysian  southeast_asian
mexican  latin_american
moroccan  african
norwegian  north_european
pakistani  south_asian
persian  middle_eastern
peruvian  latin_american
polish  east_european
portuguese  south_european
puerto-rican  latin_american
russian  east_european
scottish  north_european
south-african  african
spanish  south_european
swedish  north_european
swiss  north_european
thai  southeast_asian
turkish  middle_eastern
us-recipes  north_american
vietnamese  southeast_asian
welsh  north_european"""

#print cat_mapping_lines
cat_mapping_dict = {}
cat_mapping_list = cat_mapping_lines.split('\n')
#print cat_mapping_list

for mapping in cat_mapping_list:
    #print line
    smaller_category, larger_category = mapping.split()
    cat_mapping_dict[smaller_category] = larger_category
print cat_mapping_dict


# In[8]:

def consolidate_ethnic_categories(cat):
    return cat_mapping_dict[cat]
df['consolidated_category'] = df['ethnicCategory'].apply(consolidate_ethnic_categories)


# In[9]:

df.groupby('consolidated_category').consolidated_category.count()


# In[14]:

from cleaning_util import extract_ingredients, translate_non_alphanumerics

tqdm.pandas()


# In[15]:

df['cleanedIngredients']=df['ingredients'].progress_map(extract_ingredients)


# In[16]:

df[['cleanedIngredients','consolidated_category']].sample(5)


# # EDA: Word to Vec Model 

# Word to vec using gensim: https://radimrehurek.com/gensim/models/word2vec.html  
# Here we are creating the word vectors from the list of clean ingredients. We use the Gensim model to create the similarity matrix(cosine similarity)
# 

# In[17]:

#!pip install gensim

from gensim.models.word2vec import Word2Vec

print('Training a Word2vec model...')
w2v_model = Word2Vec(df['cleanedIngredients'].values, size=100, window=5, min_count=5, workers=4)


# In[18]:

w2v_model.wv.most_similar(positive=['onion'])


# In[19]:

w2v_model.wv.most_similar(positive=['chicken'], negative=['eggs'])


# In[20]:

X = w2v_model[w2v_model.wv.vocab]

tsne = TSNE(n_components=2)
X_tsne = tsne.fit_transform(X)

vocab = list(w2v_model.wv.vocab)
df_tsne = pd.concat([pd.DataFrame(X_tsne),
                pd.Series(vocab)],
               axis=1)
df_tsne.columns = ['x', 'y', 'ingredient']
df_tsne.sample(5)


# In[21]:

def showTSNEGraphForWord(w2v_model, df, pos_words = [], neg_words = []):
    vec = w2v_model.wv.most_similar(positive=pos_words, negative = neg_words)
    ingredients = [w[0] for w in vec]
    vec_df = df[df['ingredient'].isin(ingredients)]
    print vec_df
#    fig = plt.figure()
#    ax = fig.add_subplot(1, 1, 1)
#
#    for i, txt in enumerate(vec_df['ingredient']):
#        ax.annotate(txt, (vec_df['x'].iloc[i], vec_df['y'].iloc[i]))
#
#    ax.scatter(vec_df['x'], vec_df['y'])   


# In[22]:

showTSNEGraphForWord(w2v_model, df_tsne, pos_words=['onion']) 


# In[23]:

showTSNEGraphForWord(w2v_model, df_tsne, pos_words=['chicken', 'rice'], neg_words=['onions']) 


# # POS Tagging

# In[24]:

import re

sentence = "I want 2 blarhg @#$"
re.sub('[^a-zA-Z]', ' ', sentence)


# In[25]:

def extractVerbs(row):
    instructions = row['instructionSteps']
    tokens = []
    for inst in instructions:
        inst = re.sub('[^a-zA-Z]', ' ', inst.lower())
        tokens += inst.split()
    lstTags = nltk.pos_tag(tokens)
    verbs = []
    for item in lstTags:
        if item[1] == 'VB':
            verbs.append(item[0])
    return set(verbs)
df_verbs = df.copy()
df_verbs['verbs'] = df_verbs.progress_apply(extractVerbs, axis=1)


# In[26]:

print df_verbs['verbs'].sample(5)


# In[27]:

def combineIngredientActions(row):
    return row['cleanedIngredients'] + list(row['verbs'])
df_verbs['combined_action_ingredients'] = df_verbs.progress_apply(combineIngredientActions, axis=1)
print('Training a Word2vec model for ingredients + actions...')
action_ingredients_w2v_model = Word2Vec(df_verbs['combined_action_ingredients'].values, size=100, window=5,                                         min_count=5, workers=4)


# In[28]:

action_ingredients_w2v_model.wv.most_similar(positive=['chop'])


# In[29]:

X_2 = action_ingredients_w2v_model[action_ingredients_w2v_model.wv.vocab]

tsne_2 = TSNE(n_components=2)
X_tsne_2 = tsne.fit_transform(X_2)

vocab_2 = list(action_ingredients_w2v_model.wv.vocab)
df_tsne_2 = pd.concat([pd.DataFrame(X_tsne_2),
                pd.Series(vocab_2)],
               axis=1)
df_tsne_2.columns = ['x', 'y', 'ingredient']
df_tsne_2.sample(5)


# In[30]:

showTSNEGraphForWord(action_ingredients_w2v_model, df_tsne_2, pos_words=['chicken', 'rice'], neg_words=['onions']) 


# # Final Dataset

# In[31]:

# define the variables
EMBEDDING_SIZE = 50
MAX_LEN = 50


# In[32]:

from sklearn import preprocessing
le = preprocessing.LabelEncoder()
le.fit(df_verbs['consolidated_category'])
print le.classes_


# In[39]:

df_verbs['features'] = df_verbs['combined_action_ingredients'].progress_map(lambda x : ','.join(x).encode('ascii'))
df_verbs['label'] = le.transform(df_verbs['consolidated_category'])


# In[40]:

features = df_verbs['features'].values
labels = df_verbs['label'].values


# In[41]:

np.random.choice(features)


# In[42]:

final_X = df_verbs['features'].values
final_Y = df_verbs['label'].values

X_train, X_test, y_train, y_test = train_test_split(final_X, final_Y, test_size=0.20)


# In[50]:

cv = CountVectorizer(ngram_range=(1,2), stop_words='english', tokenizer=lambda x: x.split(','))
recipe_vocab_matrix = cv.fit_transform(X_train)
#cv.get_feature_names()
vocab_counts = zip(cv.get_feature_names(), np.asarray(recipe_vocab_matrix.sum(axis=0)).ravel())
df_vocab_counts = pd.DataFrame(vocab_counts, columns=['ingredient', 'count'])
df_vocab_counts.sample(15)


# In[45]:

def print_metrics(true_y, predicted_y, target_names, y_score=None):
    """ Prints classification metrics
    Args:
        true_y: The ground truth target labels
        predicted_y: The predicted labels from the classifier
        y_score: If not None, this is vector of probability scores for positive class (used for roc_curve) (Optional)
    Returns:
        None
    """
    print classification_report(true_y, predicted_y, target_names=target_names)
    cm = confusion_matrix(true_y, predicted_y)
    print "Confusion matrix:"
    print cm
    cm_normalized = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
    print
    print "Confusion matrix(normalized):"
    print cm_normalized
    print
    
    print 'Overall accuracy: {}'.format(accuracy_score(true_y, predicted_y))
    print
    if y_score is not None:
        print "Area Under the ROC Curve: {}".format(roc_auc_score(true_y, y_score))
        print


# # Simple Bigram Model with Random Forest

# In[46]:

from sklearn.ensemble import RandomForestClassifier


# In[47]:

def makePipeline():
    pipeline = Pipeline([
        ('vect', CountVectorizer(ngram_range=(1,2), stop_words='english', tokenizer=lambda x: x.split(','))),
        ('tfidf', TfidfTransformer()),
        ('clf', RandomForestClassifier(class_weight='balanced'))
    ])
    return pipeline
def trainModel(X, y):
    model = makePipeline()
    model.fit(X, y)
    return model

model = trainModel(X_train, y_train)
preds = model.predict(X_test)


# In[48]:

print_metrics(y_test, preds, le.classes_)


# # Embedding Layer

# In[52]:

embedding_length = 200
top_words = 10000 
embedding_vecor_length = 200
tokenizer = Tokenizer(nb_words=top_words, split=',')
tokenizer.fit_on_texts(final_X)
sequences = tokenizer.texts_to_sequences(final_X)

word_index = tokenizer.word_index
print('Found %s unique tokens.' % len(word_index))
final_X_embedded = pad_sequences(sequences, maxlen=embedding_length)
X_train, X_test, y_train, y_test = train_test_split(final_X_embedded, final_Y, test_size=0.20)




# # CNN Model

# In[ ]:

from keras.layers import Dense, Input, Flatten
from keras.layers import Conv1D, MaxPooling1D, Embedding
from keras.models import Model
from keras.utils import to_categorical


def trainKerasModel_conv(X,Y):
    model = Sequential()
    model.add(Embedding(top_words, embedding_vecor_length, input_length=embedding_length))
    model.add(Conv1D(128, 5, activation='relu'))
    model.add(MaxPooling1D(5))
    model.add(Conv1D(128, 5, activation='relu'))
    model.add(MaxPooling1D(5))
    model.add(Flatten())
    model.add(Dense(128, activation='relu'))
    model.add(Dense(len(le.classes_), activation='softmax'))
    model.compile(loss='sparse_categorical_crossentropy',
                optimizer='adam',
                metrics=['acc'])
    print model.summary()
    model.fit(X, Y, epochs=10, batch_size=100)
    # Final evaluation of the model
    return model

conv_model = trainKerasModel_conv(X_train, y_train)


# In[47]:

preds = conv_model.predict(X_test)


# In[48]:

preds = [np.argmax(p) for p in preds]


# In[49]:

print_metrics(y_test, preds, le.classes_)


# In[41]:

def saveKerasModel(modelName, model):
    model_json = model.to_json()
    with open(modelName, "w") as json_file:
        json_file.write(model_json)
def loadKerasModel(modelName):
    json_file = open(modelName, 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    loaded_model = model_from_json(loaded_model_json)
    return loaded_model


# In[50]:

saveKerasModel('conv_model_embed200_epoch5.json', conv_model)


# In[51]:

get_ipython().system(u'aws s3 cp conv_model_embed200_epoch5.json s3://RecipeVectors/')


# In[ ]:



