import nltk
import mysql.connector
from tokenPreprocessing import *
import json

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
      tokens = nltk.word_tokenize(tempArticle)
      tempTokenizedArticleList = nltk.pos_tag(tokens)
      preprocessedFunctionReturn = tokenizedPreprocessor(tempTokenizedArticleList)
      tempTokenizedArticle = preprocessedFunctionReturn[0]
      totalLemmaArticleCount = preprocessedFunctionReturn[1]
      #tempTokenizedArticle = ' '.join([str(elem) for elem in preprocessedTokenizedArticleList]) 
      #tempLemmaCount = ' '.join([str(elem) for elem in totalLemmaArticleCount]) 
      sql = "INSERT INTO tokenizedNews (url,title,tokenizedArticle,lemmaCount) values (%s, %s, %s, %s)"
      val = (tempurl, tempTitle, json.dumps(tempTokenizedArticle), json.dumps(totalLemmaArticleCount))
      cursor.execute(sql,val)
      mydb.commit()
      newArticlesTokenized = newArticlesTokenized+1
#print(tempTokenizedArticleList)
#print(type(tempTokenizedArticleList))
#print(totalLemmaArticleCount)
#print(type(tempTokenizedArticle))
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