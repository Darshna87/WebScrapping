import scrapy


class BooksSpider(scrapy.Spider):
    name = "Books_Scraper"

    def start_requests(self):

        url = "http://books.toscrape.com/"
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):

        for article in response.css("li article.product_pod"):
            #self.log(article)
            image_url= article.css("div.image_container img::attr('src')").get()
            book_title= article.css("h3 a::attr('title')").get()
            product_price= article.css("div.product_price p::text").get()

            yield{
               "image_url": image_url,
               "book_title": book_title,
               "product_price": product_price
            }

        next_page = response.css("li.next a::attr('href')").get()
        if next_page is not None:
           next_page = response.urljoin(next_page)
           yield scrapy.Request(url=next_page, callback=self.parse)







