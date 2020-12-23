import mysql.connector
import json
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
import openpyxl
import math
import pickle
import os
import random


dictionary = pd.read_pickle("./dictionary.pkl")


def dictionaryQuery(words):
    wordsList = list(words.split(" "))
    print(wordsList)
    print(len(wordsList))
    tempDictDf = dictionary[wordsList].copy().fillna(0)
    for col in tempDictDf.columns:
        tempDictDf[col] = pd.to_numeric(tempDictDf[col],errors='coerce')
    tempDictDf['mean'] = tempDictDf.mean(axis=1)
    fits = tempDictDf.sort_values(by='mean', ascending=False).head()
    print(fits)
    idxList = list(fits.index)
    print(idxList)

lemmaList = []
sampling = [0,1,2,3,4]

for col in dictionary.columns: 
    lemmaList.append(col)

print("Total number of lemmas in dictionary: ",len(lemmaList))
sampling[1] = random.choices(lemmaList,k=20)
print("20 random single word queries:",sampling[1])
sampling[1] = random.choices(lemmaList,k=20)
sampling[2] = random.choices(lemmaList,k=20)

dictionaryQuery("Lillard Jane elite movie")