import scrapy
import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="password",
  database="newsCrawler"
)

c = mydb.cursor()
newsCounter = 0

class buzzFeedWorldSpider(scrapy.Spider):
    name = 'buzzfeed'
    

    def start_requests(self):
        url = "https://www.buzzfeednews.com/section/world"
        yield scrapy.Request(url=url,callback=self.parse)

    def parse(self,response):
        global newsCounter
        tempXpath = "//a[contains(@class, 'newsblock-story-card__link xs-flex')]/@href"
        currentNewList = response.xpath(tempXpath).extract()
        tempList = []
        for x in currentNewList:
            if ('buzzfeed.com') in x:
                pass
            else:
                tempList.append(x)
        for x in tempList:
            sql = "Select url FROM news WHERE url = '{}'".format(x,)
            c.execute(sql)
            result = c.fetchone()
            if result is not None:
                pass
            else:
                yield scrapy.Request(url = x,callback= self.parseArticle)

    def parseArticle(self,response):
        global newsCounter
        url = response.url
        tempXpath = "//h1[contains(@class, 'news-article-header__title')]/text()"
        currentTitle = response.xpath(tempXpath).extract()[0]
        tempParText = response.xpath("//div[@class='js-article-wrapper']//p/text()").extract()
        articleBodyText = ' '.join([str(elem) for elem in tempParText])
        if len(articleBodyText) > 400 and len(articleBodyText) < 15000:
            #print(len(articleBodyText))
            sql = "insert into news (url,title,article) values (%s, %s, %s)"
            val = (url, currentTitle, articleBodyText)
            c.execute(sql, val)
            mydb.commit()
            newsCounter = newsCounter+1

    def closed(self,reason):
        if newsCounter > 1:
          print(newsCounter,'new articles scraped from https://www.buzzfeednews.com/section/world')
        elif newsCounter == 1:
          print(newsCounter,'new article scraped from https://www.buzzfeednews.com/section/world')
        else:
          print('No new articles scraped from https://www.buzzfeednews.com/section/world')
#class="subbuzz subbuzz-text"