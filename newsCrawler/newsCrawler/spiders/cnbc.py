import scrapy
import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="password",
  database="newsCrawler"
)

c = mydb.cursor()


class cnbcWorldSpider(scrapy.Spider):
    name = "cnbc"
    
    def start_requests(self):
        url = "https://www.cnbc.com/world/"
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self,response):
        #filename = "news.txt"
        newsCounter = 0
        #latestNews = response.xpath('//*[@id="HomePageInternational-latestNews-7-7"]/div[2]/div[2]/a/text()').getall()
        for newIndex in range(30):
            currentNew = response.xpath('//*[@id="HomePageInternational-latestNews-7-{}"]/div[2]/div[2]/a'.format(newIndex)).getall()
            tempStr = currentNew
            newUrl = currentNew[0].split('href="')[1].split('" title=""')[0]
            #print("newurl",newUrl)
            sql = "SELECT url FROM news WHERE url='{}'".format(newUrl,)
            c.execute(sql)
            result = c.fetchone()
            #print('Result = ',result)
            if result is not None:
                pass
            else:
                """
                sql = "insert into news (url,title,article) values (%s, %s, %s)"
                val = (url, "Highway 21", "eris")
                c.execute(sql, val)
                mydb.commit()
                #print(newUrl,'added to Database')
                newsCounter = newsCounter+1
                """
                newsCounter = newsCounter+1
                yield scrapy.Request(url = newUrl, callback=self.parseArticle)
        if newsCounter > 1:
            print(newsCounter,'new articles scraped from https://www.cnbc.com/world/')
        elif newsCounter == 1:
            print(newsCounter,'new article scraped from https://www.cnbc.com/world/')
        else:
            print('No new articles scraped from https://www.cnbc.com/world/')
        #print(newsCounter)

    def parseArticle(self,response):
        url = response.url
        textList = []
        tempParText = response.css('.group p::text').getall()
        #print(tempParText)
        #print(tempParText)
        articleBodyText = ' '.join([str(elem) for elem in tempParText]) 
        #print(articleBodyText)
        title = response.xpath('//*[@id="main-article-header"]/div/div[1]/div[1]/h1/text()').getall()
        sql = "insert into news (url,title,article) values (%s, %s, %s)"
        val = (url, title[0], articleBodyText)
        c.execute(sql, val)
        mydb.commit()



