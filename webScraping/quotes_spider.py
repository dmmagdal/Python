import scrapy

class QuotesSpider(scrapy.Spider):
    name = "quotes"                                                 # identify the spider (must be unique within a project)

    def start_requests(self):                                       # must return an iterable of Requests (can return a list of requests or write a generator function) which the spider will begin to crawl from. Subsequent requests will begin to crawl from these initial requests
        urls = [
            'https://quotes.toscrape.com/page/1/',
            'https://quotes.toscrape.com/page/2/',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):                                      # parse the response, extracting the scraped data as dicts and also finding new URLs to follow and create new requests from them
        page = response.url.split("/")[-2]
        filename = 'quotes-%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)
