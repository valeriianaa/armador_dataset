import scrapy
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.exceptions import CloseSpider

import json
import os

class ArticlesACMSpider(scrapy.Spider):
    namesakes_count = 0
    numpag = 2
    name = "namesakes_acm"
    namesakes = {}
    author_name = {}
    # getting the query from console
    def start_requests(self):
        url_prefix = 'https://dl.acm.org/results.cfm?query=persons.authors.personName:(%252B'
        url_middle = '%20%252B'
        url_suffix = ')&within=owners.owner=GUIDE&filtered=&dte=&bfr='
        query = getattr(self, 'query', None)
        #query = 'outliers'
        if query is not None:
            self.author_name[query] = ''
            if query.find(' ') != -1:
                fixed_query = ''
                query_words = query.split()
                for word in query_words:
                    if query_words.index(word) < (len(query_words) -1):
                        fixed_query += word + url_middle
                    else:
                        fixed_query += word
                url = url_prefix + fixed_query + url_suffix
            else:
                url = url_prefix + query + url_suffix
        yield scrapy.Request(url, self.parse, meta={'hero_item': query})    

    # parsing
    def parse(self, response):
        query = str(response.meta.get('hero_item'))
        #raise CloseSpider('enough_articles')
        if(os.path.isfile('training.json')):#TRAINING/TESTING
            with open('training.json', 'r') as archivo: #TRAINING/TESTING
                data = str(archivo.read())
                self.namesakes = json.loads(data)
        else:
            self.file = open('training.json', 'x') #TRAINING/TESTING
        author_ids = []
        self.namesakes[query] = {}
        for article in response.xpath('//div[@id="results"]/div[@class="details"]'):
            aNamesake = {}
            
            #authors list of an article

            #autoress = articulo.xpath('div[@class="authors"]/a[contains(@style, 'color: #990033')]/text()').extract()
            autores = article.xpath('div[@class="authors"]/a/text()').extract()

            #author with the name we are looking for
            if query in autores != False:
                autor = autores.index(query)
                autor_url = article.xpath('div[@class="authors"]/a/attribute::href')[autor].extract()
                id_autor = 'https://dl.acm.org/' + str(autor_url)
                cod_autor = 'ACM_author_' + str(autor_url[19:])

                if len(author_ids) > 0:
                    if (str(id_autor) in str(author_ids)) == False:
                        aNamesake = id_autor
                        self.namesakes[query][cod_autor] = []
                        author_ids.append(id_autor)
                        yield aNamesake
                        with open('namesakes.txt', 'a+') as f:  # writing JSON object
                            f.write(aNamesake + ",")
                else:
                    aNamesake = id_autor
                    self.namesakes[query][cod_autor] = []
                    author_ids.append(id_autor)
                    yield aNamesake
                    with open('namesakes.txt', 'a+') as f:  # writing JSON object
                        f.write(aNamesake + ",")


        paginations = response.xpath('//div[@id="results"]/div[@class="pagelogic"]')

        next_page = paginations.xpath('span[a='+ str(self.numpag) +']//@href').extract_first()
        
        if 'None' in self.namesakes:
            self.namesakes.pop('None')
        with open('training.json', 'w+') as f:  #TRAINING/TESTING
            json.dump(self.namesakes,f)

        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)
            self.numpag += 1
        else:
            raise CloseSpider()


#consola: scrapy crawl namesakes_acm -o namesakes.json -a query='Bharat Bhargava'
#real query: https://dl.acm.org/results.cfm?query=persons.authors.personName:(%252BBharat%20%252BBhargava)&within=owners.owner=HOSTED&filtered=&dte=&bfr=