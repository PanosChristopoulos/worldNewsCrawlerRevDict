import nltk
import mysql.connector
import json
from collections import Counter

closedClassTags = ['CD', 'CC', 'DT', 'EX', 'IN', 'LS', "''", ',', '.', '``', 'MD', 'PDT', 'POS', 'PRP', 'PRP$', 'RP', 'TO', 'UH', 'WDT', 'WP', 'WP$', 'WRB']

def listToString(test_list):  
    res = str(test_list).strip('[]')
    return res


def tokenizedPreprocessor(NTLKList):
    tempFinalList = []
    wordsList = []
    for x in NTLKList:
        if x[1] in closedClassTags:
            pass
        else:
            tempFinalList.append(x)
    for x in tempFinalList:
        wordsList.append(x[0])
    counts = Counter(wordsList)
    your_list = [list(i) for i in counts.items()]

    return [tempFinalList,your_list]

def tokenization(tempArticle):
    tokens = nltk.word_tokenize(tempArticle)
    tempTokenizedArticleList = nltk.pos_tag(tokens)
    preprocessedFunctionReturn = tokenizedPreprocessor(tempTokenizedArticleList)
    tempTokenizedArticle = preprocessedFunctionReturn[0]
    totalLemmaArticleCount = preprocessedFunctionReturn[1]
    signigicantWordCount = len(tempTokenizedArticleList)
    return tempTokenizedArticle,totalLemmaArticleCount,signigicantWordCount

#necessary nltk packages
""" 
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
"""
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="password",
  database="newsCrawler"
)

cursor = mydb.cursor()

cursor.execute("SELECT * FROM news ")

newArticlesTokenized = 0

myresult = cursor.fetchall()
for x in myresult:
    #tempId = x[0]
    tempurl = x[1]
    tempTitle = x[2]
    tempArticle = x[3]
    sql = "SELECT url FROM tokenizedNews WHERE url = '{}'".format(tempurl,)
    cursor.execute(sql)
    result = cursor.fetchone()
    if result is not None:
      pass
    else:
      preprocessedFunctionReturn = tokenization(tempArticle)
      tempTokenizedArticle = preprocessedFunctionReturn[0]
      totalLemmaArticleCount = preprocessedFunctionReturn[1]
      significantWordCount = preprocessedFunctionReturn[2]
      #tempTokenizedArticle = ' '.join([str(elem) for elem in preprocessedTokenizedArticleList]) 
      #tempLemmaCount = ' '.join([str(elem) for elem in totalLemmaArticleCount]) 
      sql = "INSERT INTO tokenizedNews (url,title,tokenizedArticle,lemmaCount,wordCount) values (%s, %s, %s, %s, %s)"
      val = (tempurl, tempTitle, json.dumps(tempTokenizedArticle), json.dumps(totalLemmaArticleCount),significantWordCount)
      cursor.execute(sql,val)
      mydb.commit()
      newArticlesTokenized = newArticlesTokenized+1

if newArticlesTokenized > 1:
  print(newArticlesTokenized,'articles tokenized')
elif newArticlesTokenized == 1:
  print(newArticlesTokenized,'article tokenized')
else:
  print("No new tokenized articles")


  
#print(tempId)
#print(tempurl)
#print(tempTitle)
#print(tempArticle)