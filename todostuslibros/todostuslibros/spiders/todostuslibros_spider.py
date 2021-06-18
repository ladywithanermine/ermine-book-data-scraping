import scrapy
import todostuslibros.settings as settings
import re
class TodostuslibrosSpider(scrapy.Spider):
    name = "todostuslibros"

    def start_requests(self):
        for url in settings.TODOSTUSLIBROS_URL_LIST:
            yield scrapy.Request(url=url, callback=self.parse_book_list)

    def parse_book_list(self, response):
        for book in response.css("div.book-details"):
            meta = {}
            meta['title'] = book.css("h2.title a::text").get().strip(),
            meta['author'] = book.css("h3.author a::text").get(),
            data = book.css("p.data::text").get().split('/')
            meta['publisher'] = data[0].strip()
            meta['isbn'] = re.sub(r'\D', '', data[1].strip())

            book_detail_url = settings.TODOSTUSLIBROS_BOOK_DETAIL_URL_TEMPLATE.replace('{isbn}', meta['isbn'])

            yield scrapy.Request(url=book_detail_url, callback=self.parse_book_detail, cb_kwargs={'meta':meta})
        
        yield from response.follow_all(css='nav a.page-link[rel="next"]::attr("href")', callback=self.parse_book_list)

    def parse_book_detail(self, response, meta):
        meta['price'] = response.css('.book-price strong::text').get()
        meta['tags'] = response.css('.row.materias a::text').get()
        meta['bookstores_number'] = int(response.css('.before-title::text').re(r'\d+')[0])

        yield meta