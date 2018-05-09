import scrapy
from scrapy.linkextractor import LinkExtractor
from scrapy.spiders import Rule, CrawlSpider
from elComercio.items import articleItems
import json
from bs4 import BeautifulSoup

class TestSpider(scrapy.Spider):
    name = "test"
    start_urls = [
        'http://elcomercio.pe/archivo',
    ]

    allowed_domains = ["elcomercio.pe"]

    articleList = []

    def parse(self, response):
        newsContainer = response.css('div.column-flows')[0]
        articlesData = newsContainer.css('article')

        # Getting the Link for each article and requesting a new response for each link
        for article in articlesData:
            partialLink = article.css('h2.flow-title')[0].css('a::attr(href)')[0].extract()
            fullLink = response.urljoin(partialLink)
            yield scrapy.Request(url=fullLink, callback=self.parseArticles)

    def parseArticles(self, response):

        # Crawling information related to the article
        articleData = response.css('article.news-detail')[0]
        category = articleData.css('div.sponsorr')[0].css('h3.news-category')[0].css('a::text')[0].extract().encode('utf-8')
        title = articleData.css('div.sf.elemento.generico')[0].css('h1.news-title::text')[0].extract().encode('utf-8')
        summary = articleData.css('div.sf.elemento.generico')[0].css('h2.news-summary::text')[0].extract().encode('utf-8')
        
        # Crawling information related to the article
        bodyData = articleData.css('div.news-column')[0].css('div.news-body.clearfix')[0]
        author = bodyData.css('div.news-author-date')[0].css('span')[0].css('a')[0].css('span::text')[0].extract().encode('utf-8')
        time = bodyData.css('div.news-author-date')[0].css('time::attr(datetime)')[0].extract().encode('utf-8')

        # Recursevly get the parragraphs and the links
        contentData = bodyData.css('div.article-content')[0].css('div.news-text')[0]
        soup = BeautifulSoup(contentData.extract())
        content = " ".join([p.get_text().strip() for p in soup.find_all('p')])

        article = articleItems()
        article["title"] = title
        article["category"] = category
        article["summary"] = summary
        article["author"] = author
        article["time"] = time
        article["content"] = content
        self.articleList.append(article)
    
    def closed(self, reason):
        articleJsonFile = open("articlesData.json","w+")
        articleJsonFile.write(json.dumps([ob.__dict__ for ob in self.articleList]))
        articleJsonFile.close()
        return self.articleList
