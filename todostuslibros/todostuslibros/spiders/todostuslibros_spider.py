import scrapy
import todostuslibros.settings as settings
import re
from urllib.parse import urlparse
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

        meta['synopsis'] = response.css('#synopsis > div > div.col-md-9.synopsis p::text').get()
    
        meta['tags'] = response.css('.row.materias a::text').getall()
        meta['bookstores_number'] = int(response.css('.before-title::text').re(r'\d+')[0])

        isbn_site_url = settings.ISBN_DATABASE_URL
        formdata = settings.ISBN_QUERY_FORMDATA
        formdata['params.cisbnExt'] = meta['isbn']
        yield scrapy.FormRequest(url=isbn_site_url, callback=self.query_isbn_detail, formdata=formdata, cb_kwargs={'meta':meta})

        yield meta

    def _get_book_table_data(self, response, text):
        value = response.xpath(f'//dt[contains(text(),"{text}")]/following-sibling::dd/text()').get() or ''
        return value.strip()

    def query_isbn_detail(self, response, meta):
        isbn_detail_url_relative = response.css('div.camposCheck a::attr(href)').extract()[0]
        parsed_response_url = urlparse(response.url)

        isbn_detail_url = parsed_response_url.scheme + '://' + parsed_response_url.netloc + isbn_detail_url_relative

        # Invoke URL to retrieve details
        yield scrapy.Request(url=isbn_detail_url, callback=self.parse_isbn_detail, cb_kwargs={'meta':meta})

    def parse_isbn_detail(self, response, meta):
        # Get ISBN data from the page
        
        publication_language = response.xpath('//*[@id="formularios"]/div[2]/table/tr[3]/td/span/text()').get()
        edition_date = response.xpath('//*[@id="formularios"]/div[2]/table/tr[4]/td/text()').get()
        printing_date = response.xpath('//*[@id="formularios"]/div[2]/table/tr[5]/td/text()').get()
        description = response.xpath('//*[@id="formularios"]/div[2]/table/tr[7]/td/text()').get()
        binding = response.xpath('//*[@id="formularios"]/div[2]/table/tr[8]/td/text()').get()
        subject = response.xpath('normalize-space(//*[@id="formularios"]/div[2]/table/tr[10]/td/span/text())').get()
        price = response.xpath('//*[@id="formularios"]/div[2]/table/tr[11]/td/text()').get()
        formatted_price = float(re.sub(r'(\d+),(\d+)\sEuros', '\\1.\\2', price)) if price else None

        # Update the metadata and insert new fields
        meta['publishing_language'] = meta['publishing_language'] if meta['publishing_language'] else publication_language
        meta['publication_date'] = meta['publication_date'] if meta['publication_date'] else edition_date
        meta['printing_date'] = printing_date
        meta['edition_description'] = description
        meta['binding'] = meta['binding'] if meta['binding'] else binding
        meta['isbn_classification'] = subject
        meta['price'] = meta['price'] if meta['price'] else formatted_price

        yield meta