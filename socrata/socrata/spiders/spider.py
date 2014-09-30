from scrapy.spider import Spider
from scrapy import Selector
from socrata.items import SocrataItem

class MySpider(Spider):

    name = "socrata"
    allowed_domains = ["opendata.socrata.com"]
    start_urls = [
    'https://opendata.socrata.com'
    ]


    def parse(self,response):

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

