import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="password"
)



cursor = mydb.cursor()

cursor.execute("CREATE DATABASE IF NOT EXISTS newsCrawler")

cursor.execute("SHOW DATABASES")

#for x in cursor:
#  print(x)

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="password",
  database="newsCrawler"
)

cursor = mydb.cursor()
cursor.execute('DROP TABLE tokenizedNews')
cursor.execute("CREATE TABLE IF NOT EXISTS news (id INT AUTO_INCREMENT PRIMARY KEY, url VARCHAR(255), title TEXT, article TEXT, added TIMESTAMP DEFAULT CURRENT_TIMESTAMP)")


cursor.execute("DESCRIBE news")

print('news Table:')
for x in cursor:
  print(x)

cursor.execute("CREATE TABLE IF NOT EXISTS tokenizedNews (id INT AUTO_INCREMENT PRIMARY KEY, url VARCHAR(255), title TEXT, tokenizedArticle TEXT, lemmaCount TEXT, added TIMESTAMP DEFAULT CURRENT_TIMESTAMP)")


cursor.execute("DESCRIBE tokenizedNews")

print('tokenizedNews Table:')
for x in cursor:
  print(x)