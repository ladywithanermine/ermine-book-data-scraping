import scrapy


class TodostuslibrosSpider(scrapy.Spider):
    name = "todostuslibros"

    def start_requests(self):
        urls = [
            #'https://www.todostuslibros.com/materia/ficcion-moderna-y-contemporanea_FA'
            'https://www.todostuslibros.com/editorial/folio-gallimard' # Tiene pocos resultados
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

        yield from response.follow_all(css='nav a.page-link[rel="next"]::attr("href")', callback=self.parse)