import scrapy
import todostuslibros.settings as settings

class TodostuslibrosSpider(scrapy.Spider):
    name = "todostuslibros"

    def start_requests(self):
        for url in settings.TODOSTUSLIBROS_URL_LIST:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for book in response.css("div.book-details"):
            yield {
                'title' : book.css("h2.title a::text").get().strip(),
                'author' : book.css("h3.author a::text").get(),
                'data' : book.css("p.data::text").get()
            }

        yield from response.follow_all(css='nav a.page-link[rel="next"]::attr("href")', callback=self.parse)