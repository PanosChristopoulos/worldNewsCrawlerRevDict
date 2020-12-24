import mysql.connector
import json
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
import openpyxl
import math
import pickle
import os
import random
import time


mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="password",
  database="newsCrawler"
)


cursor = mydb.cursor()


dictionary = pd.read_pickle("./dictionary.pkl")
with open('listSequence.pkl', 'rb') as f:
    listSequence = pickle.load(f)


def dictionaryQuery(words):
    try:
        print("Query:",words)
        wordsList = list(words.split(" "))
        tempDictDf = dictionary[wordsList].copy().fillna(0)
        for col in tempDictDf.columns:
            tempDictDf[col] = pd.to_numeric(tempDictDf[col],errors='coerce')
        tempDictDf['mean'] = tempDictDf.mean(axis=1)
        fits = tempDictDf.sort_values(by='mean', ascending=False).head()
        idxList = list(fits.index)
        for x in idxList:
            cursor.execute("SELECT title,url FROM tokenizedNews WHERE id={}".format(x+2))
            for x in cursor:
                print(x)
    except:
        print("Query",words,"not successfull")

lemmaList = []
sampling = [0,1,2,3,4]
start = time.time()

for col in dictionary.columns: 
    lemmaList.append(col)

print("Total number of lemmas in dictionary: ",len(lemmaList))
sampling[1] = random.choices(lemmaList,k=20)
print("20 random single word queries:")

for x in sampling[1]:
    dictionaryQuery(x)

print("20 random double word queries:")

sampling[1] = random.choices(lemmaList,k=20)
sampling[2] = random.choices(lemmaList,k=20)
for x in range(20):
    dictionaryQuery(sampling[1][x]+' '+sampling[2][x])

print("30 random triple word queries:")

sampling[1] = random.choices(lemmaList,k=30)
sampling[2] = random.choices(lemmaList,k=30)
sampling[3] = random.choices(lemmaList,k=30)

for x in range(30):
    dictionaryQuery(sampling[1][x]+' '+sampling[2][x]+' '+sampling[3][x])

print("30 random quadruple word queries:")

sampling[1] = random.choices(lemmaList,k=30)
sampling[2] = random.choices(lemmaList,k=30)
sampling[3] = random.choices(lemmaList,k=30)
sampling[4] = random.choices(lemmaList,k=30)

for x in range(30):
    dictionaryQuery(sampling[1][x]+' '+sampling[2][x]+' '+sampling[3][x]+' '+sampling[4][x])

end = time.time()
totalTime = format(end-start, '.5f')
print('Total time elapsed for all searches:',totalTime)
print('Average time elapsed for each query group:',float(totalTime)/4)

itterationBool = True

while(itterationBool == True):
    stringIn = input('Please type search query: \n (To exit type exit) \n')
    if stringIn == 'exit':
        break
    else:
        dictionaryQuery(stringIn)