import sqlite3
conn = sqlite3.connect('newsCrawler')

c = conn.cursor()
c.execute('DROP TABLE urls')