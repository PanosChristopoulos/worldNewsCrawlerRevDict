for x in range(1,100):
    tempParText = response.xpath('//*[@id="SpecialReportArticle-ArticleBody-6"]/div[2]/p[{}]/text()'.format(x))
    if  tempParText is not None:
        textList.append(tempParText)
    else:
        break