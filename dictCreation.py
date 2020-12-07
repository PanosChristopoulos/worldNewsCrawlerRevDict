import mysql.connector
import json
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
import openpyxl
import math

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="password",
  database="newsCrawler"
)


mycursor = mydb.cursor()


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

"""
uniqueLemmas()
vectorizer = TfidfVectorizer()
mycursor.execute("SELECT id,article FROM news")
myresult = mycursor.fetchall()
articleList = []
articleId = []
for x in myresult:
    articleList.append(x[1])
    articleId.append(x[0])


vectors = vectorizer.fit_transform(articleList)
feature_names = vectorizer.get_feature_names()
dense = vectors.todense()
denselist = dense.tolist()
df = pd.DataFrame(denselist, columns=feature_names)
df.index = articleId
df.to_excel('output.xlsx',sheet_name = 'eris')

"""


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
