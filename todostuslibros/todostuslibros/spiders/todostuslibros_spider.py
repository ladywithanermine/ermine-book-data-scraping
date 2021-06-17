import scrapy


class TodostuslibrosSpider(scrapy.Spider):
    name = "todostuslibros"

    def start_requests(self):
        urls = [
            'https://www.todostuslibros.com/materia/ficcion-moderna-y-contemporanea_FA'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for book in response.css("div.book-details"):
            yield {
                'title' : book.css("h2.title a::text").get().strip(),
                'author' : book.css("h3.author a::text").get(),
                'data' : book.css("p.data::text").get()
            }

        #yield from response.follow_all(css='ul.pager a', callback=self.parse)