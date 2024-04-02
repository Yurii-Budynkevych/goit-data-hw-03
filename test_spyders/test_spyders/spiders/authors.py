import scrapy
from test_spyders.items import AuthorsItem

class AuthorsSpider(scrapy.Spider):
    name = "authors"
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["https://quotes.toscrape.com"]

    def parse(self, response, **kwargs):
        for q in response.xpath("/html//div[@class='quote']"):
            author_link = q.xpath('span/a/@href').get()
            yield response.follow(url=self.start_urls[0] + author_link, callback= self.parse_author)
        
        next_link = response.xpath("/html//li[@class='next']/a/@href").get()
        if next_link:
            yield scrapy.Request(url=self.start_urls[0] + next_link, callback=self.parse)


    @classmethod
    def parse_author(cls, response, **kwargs):
        data = response.xpath("/html//div[@class='author-details']")
        fullname = data.xpath("h3/text()").get().strip()
        born_date = data.xpath("p/span[@class='author-born-date']/text()").get().strip()
        born_location = data.xpath("p/span[@class='author-born-location']/text()").get().strip()
        description = data.xpath("div[@class='author-description']/text()").get().strip()

        yield AuthorsItem(
        fullname=fullname,
        born_date=born_date,
        born_location=born_location,
        description=description
        )