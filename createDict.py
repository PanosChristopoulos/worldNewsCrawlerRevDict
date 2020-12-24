import mysql.connector
import json
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
import openpyxl
import math
import pickle
import os
from pathlib import Path

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="password",
  database="newsCrawler"
)


mycursor = mydb.cursor()


def dfToExcel():
    totalPandasDictionary.to_excel('dictionary.xlsx')

def pklToDict(filename):
    with open(filename,'rb') as handle:
        b = pickle.load(handle)
    return b

cur_path = os.path.dirname(__file__)
paths = sorted(Path('dictLists/').iterdir(), key=os.path.getmtime)
print(paths)
pathsNames = []

for x in range(len(paths)):
    pathsNames.append(paths[x].name)

print(pathsNames)

listsToDict = pathsNames
print('liststodict',listsToDict)
"""
with open('listSequence.pkl', 'wb') as f:
    pickle.dump(listsToDict, f)
"""
vastDataList = []
for x in listsToDict:
    vastDataList.append(pklToDict('dictLists/{}'.format(x)))

totalPandasDictionary=pd.DataFrame(vastDataList)


print(totalPandasDictionary)
numOfColumns = len(totalPandasDictionary.columns)
totalPandasDictionary.to_pickle("./dictionary.pkl")


f = open("dictionary.xml", "w")
f.write("<inverted_index>")
f.write("\n")
f.close()
#print(totalPandasDictionary.iloc[:,123].sort_values(ascending=False).name)

for x in range(numOfColumns):
    tempSeries = totalPandasDictionary.iloc[:,x].sort_values(ascending=False)
    tempSeriesName = tempSeries.name
    f = open("dictionary.xml", "a")
    tempSeries.dropna(inplace=True)
    f.write('   <lemma name="{}">'.format(tempSeries.name))
    f.write("\n")
    for x in range(len(tempSeries)):
        #print(tempSeries.index[x]+1,tempSeries.iloc[x])
        f.write('       <document id="{}" TF-IDF weight="{}"/>'.format(tempSeries.index[x]+1,tempSeries.iloc[x]))
        f.write("\n")
    f.write('   </lemma>')
    f.write("\n")
    f.close()
        
f = open("dictionary.xml", "a")
f.write("</inverted_index>")
f.write("\n")
f.close()

