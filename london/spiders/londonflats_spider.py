import scrapy
from scrapy import Request
from ..items import LondonItem



class LondonrelocationSpider(scrapy.Spider):
    name = 'londonrelocation'
    allowed_domains = ['londonrelocation.com']
    start_urls = ['https://londonrelocation.com/properties-to-rent/']
    page_number = 2
    def parse(self, response):
        for start_url in self.start_urls:
            yield Request(response.urljoin(start_url),
                          callback=self.parse_area)

    def parse_area(self, response):
        area_urls = response.xpath('.//div[contains(@class,"area-box-pdh")]//h4/a/@href').extract()
        for area_url in area_urls:
            yield Request(response.urljoin(area_url),
                          callback=self.parse_area_pages)

    def parse_area_pages(self, response):        
        flat_urls = response.css('.h4-space a').xpath("@href").extract()
        area_url = response.url
        for flat_url in flat_urls:
            yield Request(response.urljoin(flat_url),
                          callback=self.parse_flat)
            

        next_page = f'{area_url}&pageset={str(LondonrelocationSpider.page_number)}'

        if LondonrelocationSpider.page_number < 3 :
            LondonrelocationSpider.page_number += 1
            yield response.follow(next_page, callback = self.parse_area_pages) 

    def parse_flat(self, response):
        item = LondonItem()        

        title = response.css('h1::text').extract_first()
        price = response.css('h3::text').extract_first().split()[0].replace("£","")

        item["title"] = title
        item["price"] = price
        item["url"] = response.url

        yield item

      