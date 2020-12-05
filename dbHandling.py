import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="password",
  database="newsCrawler"
)

cursor = mydb.cursor()
"""
sql = "INSERT INTO news (url, title, article) VALUES (%s, %s, %s)"
val = ("John", "Highway 21", "eris")
cursor.execute(sql, val)

mydb.commit()
"""
mycursor = mydb.cursor()

mycursor.execute("SELECT title FROM news ")

myresult = mycursor.fetchall()

#for x in myresult:
 # print(x)

print(len(myresult),'articles in database')

mycursor.execute("SELECT article FROM news")
myresult = mycursor.fetchall()
print(myresult[2])

