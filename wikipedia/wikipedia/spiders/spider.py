from scrapy.spider import Spider
from scrapy.selector import HtmlXPathSelector
import wikipedia.items

class MySpider(Spider):

    name = "wikipediafilms"

    allowed_domains = ["en.wikipedia.org/wiki/Category:2014_films"]

    start_urls = ["https://en.wikipedia.org/wiki/Category:2014_films"]


    def parse(self, response):

        hxs = HtmlXPathSelector(response)

        titles = hxs.select('//div[@class="mw-content-ltr"]//li')

        items =[]

        for title in titles:
            item = wikipedia.items.WikipediaItem()
            item["title"] = title.select("a/@title").extract
            item["url"] = title.select("a/@href").extract
            items.append(item)
        return items


