import mysql.connector
import json
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
import openpyxl
import math
import pickle

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="password",
  database="newsCrawler"
)


mycursor = mydb.cursor()


def dictToPickle(name,mydict):
    with open('dictLists/{}.pkl'.format(name),'wb') as f:
        pickle.dump(mydict, f, protocol=pickle.HIGHEST_PROTOCOL)

def dictToJson(dict):
    with open("sample.json", "w") as outfile:  
        json.dump(dict, outfile) 


def totalWordCount():
    wordCount = 0
    mycursor.execute("SELECT wordCount FROM tokenizedNews")
    myresult = mycursor.fetchall()
    for x in myresult:
        wordCount = wordCount + x[0]
    return wordCount

def uniqueLemmas():
    globalLemmaList = []
    mycursor.execute("SELECT * FROM tokenizedNews")
    myresult = mycursor.fetchall()
    #y = json.loads(myresult[100][4])
    #print(type(y))
    for x in range(len(myresult)):
        try:
            lemmaList = json.loads(myresult[x][4])
            for lemma in lemmaList:
                tempLemma = lemma[0]
                if tempLemma not in globalLemmaList:
                    globalLemmaList.append(tempLemma)
        except:
            pass
    #print('There are',len(globalLemmaList),'unique lemmas')
    return globalLemmaList



def computeTF(articleID):
    mycursor.execute("SELECT * FROM tokenizedNews WHERE ID = {}".format(articleID))
    myresult = mycursor.fetchall()
    tfDictionary = {}
    wordsLength = myresult[0][-3]
    bagOfWords = json.loads(myresult[0][4])
    for x in bagOfWords:
        tempNum = x[1] / float(wordsLength)
        tfDictionary[x[0]] = format(tempNum, '.6f')
    return tfDictionary

uniqueWords = uniqueLemmas()
wordsDict = dict.fromkeys(uniqueWords, 0)


def computeIDF():
    idfDict = {}
    mycursor.execute("SELECT article FROM news")
    result = mycursor.fetchall()
    documents = []
    for x in result:
        documents.append(x[0])
    n = len(documents)
    print('Computing IDF for',n,'Documents.')
    for x in documents:
        tempBagofWords=x.split(' ')
        for word in tempBagofWords:
            try:
                wordsDict[word] +=1
            except:
                pass
    erCount = 0
    wordsToRemove = []
    for word, val in wordsDict.items():
        try:
            numToDict = math.log(n/float(val))
            wordsDict[word] = format(numToDict, '.5f')
        except:
            wordsToRemove.append(word)
    for word in wordsToRemove:
        del wordsDict[word]
    print(len(wordsDict),'unique lemmas added')
    return wordsDict



idf = computeIDF()

def computeTFIDF(articleID,idfs):
    tfidf = {}
    tfBagOfWords = computeTF(articleID)
    #print(tfBagOfWords)
    for word,val in tfBagOfWords.items():
        try:
            tempNum = float(val)*float(idfs[word])*10
            tfidf[word] = format(tempNum, '.5f')
        except:
            pass
    #print(word,val)
    #print(idfs[word])
    return tfidf

#print(computeTFIDF(185,idf))
#a = computeTFIDF(185,idf)
#dictToPickle('a',a)
#b = computeTFIDF(12,idf)
#df = pd.DataFrame([a,b])
#print(df)
#df.to_pickle('eris.pkl')

#df = pd.read_pickle('eris.pkl')
#print(df)
"""
print(a)
dictionaryDataframe = pd.DataFrame()
print(dictionaryDataframe)
dictionaryDataframe.append(a, ignore_index = True)
print(dictionaryDataframe)
"""
"""
    print(len(documents))
    print(type(documents[0]))
    article = documents[0][0]
    print(len(article))
    print(type(article))
    #for article in documents:
    wordCollection = article.split(' ')
    print(wordCollection)
    #uniqueWords = set()
    """

mycursor.execute("SELECT id,articleInDict from tokenizedNews")
result = mycursor.fetchall()

articlesToDictCounter = 0
for x in result:
    if x[1] == 0:
       tempList = computeTFIDF(x[0],idf)
       dictToPickle('{}'.format(x[0]),tempList)
       mycursor.execute("UPDATE tokenizedNews SET articleInDict = 1 WHERE id = {};".format(x[0]))
       mydb.commit()
       articlesToDictCounter += 1

print(articlesToDictCounter,'articles added to Dictionary')