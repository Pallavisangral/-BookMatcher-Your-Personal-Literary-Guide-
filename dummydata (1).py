# -*- coding: utf-8 -*-
"""dummydata.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1zft9t5mHe2ON7azJpQK80REOeNdr0tR0
"""

import numpy as np
import pandas as pd
#import nltk
import json
import re
import csv
from tqdm import tqdm
pd.set_option('display.max_colwidth', 300)

data = []

with open("booksummaries.txt", 'r') as f:
    reader = csv.reader(f, dialect='excel-tab')
    for row in tqdm(reader):
        data.append(row)

book_index = []
book_id = []
book_author = []
book_name = []
summary = []
genre = []
a = 1
for i in tqdm(data):
    book_index.append(a)
    a = a+1
    book_id.append(i[0])
    book_name.append(i[2])
    book_author.append(i[3])
    genre.append(i[5])
    summary.append(i[6])
df = pd.DataFrame({'Index': book_index, 'ID': book_id, 'BookTitle': book_name, 'Author': book_author,
                       'Genre': genre, 'Summary': summary})
df.head()

df.isna().sum()

df = df.drop(df[df['Genre'] == ''].index)
df = df.drop(df[df['Summary'] == ''].index)


genres_cleaned = []
for i in df['Genre']:
    genres_cleaned.append(list(json.loads(i).values()))
df['Genres'] = genres_cleaned

def clean_summary(text):
    text = re.sub("\'", "", text)
    text = re.sub("[^a-zA-Z]"," ",text)
    text = ' '.join(text.split())
    text = text.lower()
    return text

df['clean_summary'] = df['Summary'].apply(lambda x: clean_summary(x))
df.head(2)

df.drop(columns=["Genre", "Summary"], inplace=True)

df.head(3)

json = df.to_json(r'json file', orient='table')