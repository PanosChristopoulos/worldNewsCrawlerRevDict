from tokenization import *
import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="password",
  database="newsCrawler"
)

cursor = mydb.cursor()

def articleTF(article):
    tfDict = {}
    articleTokenization = tokenization(article)
    wordCount = articleTokenization[2]
    articleLemmaCount = articleTokenization[1]
    for x in articleLemmaCount:
        tfDict[x[0]] = x[1] / float(wordCount)
    return tfDict

cursor.execute("SELECT article FROM news")
myresult = cursor.fetchall()
print(myresult[0][0])


"""
def computeIDF(articles):
    import math
    N = len(articles)
    idfDict = dict.fromkeys(articles[0][0].keys(),0)
    for article in articles:
        for word, val in article.items():
            if val > 0:
                idfDict[word] += 1
    for word, val in idfDict.items():
        idfDict[word] = math.log(N/float(val))
    return idfDict

print(computeIDF(myresult))
"""