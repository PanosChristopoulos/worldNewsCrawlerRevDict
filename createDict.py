import mysql.connector
import json
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
import openpyxl
import math
import pickle
import os

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="password",
  database="newsCrawler"
)


mycursor = mydb.cursor()

def pklToDict(filename):
    with open(filename,'rb') as handle:
        b = pickle.load(handle)
    return b

cur_path = os.path.dirname(__file__)
#new_path = os.path.relpath('/dictLists',cur_path)
listsToDict = os.listdir('dictLists/')


vastDataList = []
#print(pklToDict('dictLists/2.pkl'))
for x in listsToDict:
    vastDataList.append(pklToDict('dictLists/{}'.format(x)))

totalPandasDictionary=pd.DataFrame(vastDataList)
totalPandasDictionary.to_excel('dictionary.xlsx')