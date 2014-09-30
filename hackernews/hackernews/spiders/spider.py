from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from hackernews.items import HackernewsItem

class MySpider(BaseSpider):

    name = "hackernews"

    allowed_domains = ["news.ycombinator.com/"]

    start_urls = ["https://news.ycombinator.com/"]

    def parse(self,response):

        hxs = HtmlXPathSelector(response)
        titles = hxs.select('//td[@class="title"]')
        items = []

        for title in titles:
            item = HackernewsItem()
            item["title"] = title.select("a/text()").extract
            item["url"] = title.select("a/@href").extract
            items.append(item)
        return items




