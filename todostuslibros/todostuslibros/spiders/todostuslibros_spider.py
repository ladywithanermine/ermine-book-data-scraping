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
            meta['title'] = book.css("h2.title a::text").get().strip()
            meta['author'] = book.css("h3.author a::text").get()
            data = book.css("p.data::text").get().split('/')
            meta['publisher'] = data[0].strip()
            meta['isbn'] = re.sub(r'\D', '', data[1].strip())

            book_detail_url = settings.TODOSTUSLIBROS_BOOK_DETAIL_URL_TEMPLATE.replace('{isbn}', meta['isbn'])

            yield scrapy.Request(url=book_detail_url, callback=self.parse_book_detail, cb_kwargs={'meta':meta})
        
        yield from response.follow_all(css='nav a.page-link[rel="next"]::attr("href")', callback=self.parse_book_list)
        

    def parse_book_detail(self, response, meta):
        price = response.css('.book-price strong::text').get()
        meta['price'] = float(re.sub(r'(\d+),(\d+)€', '\\1.\\2', price)) if price else None

        binding = self._get_book_table_data(response, 'Encuadernación')
        meta['binding'] = binding if 'No definida' not in binding else None

        meta['publishing_country'] = self._get_book_table_data(response, 'País de publicación')
        meta['publishing_language'] = self._get_book_table_data(response, 'Idioma de publicación')
        meta['original_language'] = self._get_book_table_data(response, 'Idioma original')
        meta['ean'] = self._get_book_table_data(response, 'EAN')
        meta['publication_date'] = self._get_book_table_data(response, 'Fecha publicación')

        num_pages = self._get_book_table_data(response, 'Nº páginas')
        meta['num_pages'] = int(num_pages) if num_pages else None

        img_url = response.css('.book-image img::attr(src)').get()
        meta['img_url'] = img_url if 'img-no-disponible' not in img_url else None
    
        meta['tags'] = response.css('.row.materias a::text').getall()
        meta['bookstores_number'] = int(response.css('.before-title::text').re(r'\d+')[0])

        yield meta

    def _get_book_table_data(self, response, text):
        value = response.xpath(f'//dt[contains(text(),"{text}")]/following-sibling::dd/text()').get() or ''
        return value.strip()

