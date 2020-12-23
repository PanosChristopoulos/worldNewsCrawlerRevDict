import scrapy
import mysql.connector
import time

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="password",
  database="newsCrawler"
)

c = mydb.cursor()

newsCounter=0

class abcWorldSpider(scrapy.Spider):
    name = "abc"
    newsCounter=0
    
    def start_requests(self):
        url = "https://abcnews.go.com/International"
        yield scrapy.Request(url=url, callback=self.parse)
    def parse(self,response):
        global newsCounter
        tempXpath = '//h2/a/@href'
        currentNewList = response.xpath(tempXpath).extract()
        for x in currentNewList:
          sql = "Select url FROM news WHERE url = '{}'".format(x,)
          c.execute(sql)
          result = c.fetchone()
          if result is not None:
            pass
          else:
            yield scrapy.Request(url = x, callback = self.parseArticle)


    def parseArticle(self,response):
      global newsCounter
      try:
        tempXpath = "//h1[contains(@class, 'Article__Headline__Title')]/text()"
        currentTitle = response.xpath(tempXpath).extract()
        title = currentTitle[0]
        url = response.url
        tempParText = response.xpath("//section[@class='Article__Content story']//p/text()").getall()
        articleBodyText = ' '.join([str(elem) for elem in tempParText])
        #print('len',len(articleBodyText))
        #print(articleBodyText)
        if len(articleBodyText) > 700:
          sql = "insert into news (url,title,article) values (%s, %s, %s)"
          val = (url, title, articleBodyText)
          c.execute(sql, val)
          mydb.commit()
          newsCounter = newsCounter+1
        #print(newsCounter)
      except:
        pass

    def closed(self,reason):
        if newsCounter > 1:
          print(newsCounter,'new articles scraped from https://abcnews.go.com/International')
        elif newsCounter == 1:
          print(newsCounter,'new article scraped from https://abcnews.go.com/International')
        else:
          print('No new articles scraped from https://abcnews.go.com/International')

#//*[@id="fitt-analytics"]/div/main/div[7]/div[1]/section/section[1]/div[2]/h2/a
#//*[@id="fitt-analytics"]/div/main/div[7]/div[1]/section/section[2]/div[2]/h2/a
#/html/body/div[1]/div/div/main/div[7]/div[1]/section/section[1]/div[2]/h2/a
#//div[@class='Article__Content story']//p
#//*[@id="fitt-analytics"]/div/main/div[7]/div[1]/section/section[50]/div[2]/h2/a