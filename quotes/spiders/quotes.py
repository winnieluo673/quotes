import scrapy
from quotes.items import QuotesItem

class Quotes(scrapy.Spider):
    name="quotes"
    allowed_domains=["quotes.toscrape.com"]
    start_urls=[
        'http://quotes.toscrape.com/page/1/',
    ]

    def parse(self,response):
        for quote in response.xpath("//div[@class='quote']"):
            item = QuotesItem()
            item['quote'] = quote.xpath("span[@class='text']/text()").extract_first()
            item['author'] = quote.xpath("span/small[@class='author']/text()").extract_first()
            item['tags'] = quote.xpath("div[@class='tags']/a[@class='tag']/text()").extract()
            yield item

        next_page = response.xpath("//ul[@class='pager']/li[@class='next']/a/@href").extract_first()
        next_page = "http://quotes.toscrape.com" + next_page
        yield scrapy.http.Request(next_page, callback=self.parse)