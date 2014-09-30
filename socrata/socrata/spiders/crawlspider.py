from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy import Selector

from socrata.items import SocrataItem



class MySpider(CrawlSpider):

    name = "socrata2"
    allowed_domains = ["opendata.socrata.com"]
    start_urls = [
    'https://opendata.socrata.com'
    ]


    rules = (Rule
    (SgmlLinkExtractor(allow=("browse\?utf8=%E2%9C%93&page=\d*",
        )), callback="parse_items", follow=True),)

    def parse_items(self,response):

        hxps = Selector(response)
        
        titles = hxps.xpath('//tr[@itemscope="itemscope"]')
        
        items = []

        for t in titles:
            item = SocrataItem()
            item["title"] = t.xpath('td[2]/div/a[@class="name"]/text()').extract()
            item["url"] = t.xpath('td[2]/div/a/@href').extract()
            item["views"] = t.xpath('td[@class="popularity"]/span[@class="visits"]/text()').extract()
            items.append(item)
       


        return (items)

