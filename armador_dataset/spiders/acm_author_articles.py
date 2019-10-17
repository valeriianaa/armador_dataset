import scrapy
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.exceptions import CloseSpider

import json
import os

class AuthorArticlesACMSpider(scrapy.Spider):
    articles_count = 0
    numpag = 2
    data = []
    training_data = {}
    name = "author_articles_acm"
    articles = {}
    
    # getting the query from console

    def start_requests(self):   
        url = getattr(self, 'query', None)
        author_names = getattr(self, 'author_name', None)
        yield scrapy.Request(url, self.parse, meta={'item': author_names}) 

    # parsing
    def parse(self, response):
        author_names = response.meta.get('item')
        #print("author_names " + str(author_names))
        if(os.path.isfile('articulos_raw.json')):
            with open('articulos_raw.json', 'r+') as archivo:
                articles = str(archivo.read())
                self.articles = json.loads(articles)
        else:
            self.file = open('articulos_raw.json', 'x')
        with open('testing.json') as a_file: #TRAINING/TESTING
            training_data = str(a_file.read())
            self.training_data = json.loads(training_data)
        
        #for each result
        for article in response.xpath('//div[@id="results"]/div[@class="details"]'):
            
            anArticle = {}      
            
            # getting article data
            id_articulo = 'ACM_article_' + str(article.xpath('div[@class="title"]/a/attribute::href').extract_first())[16:]

            titulo = str(article.xpath('div[@class="title"]/a/text()').extract_first())

            #anio de publicacion
            if(article.xpath('div[@class="source"]/descendant::*') != []):
                metadata = article.xpath('div[@class="source"]')
                year = 0
                year = int(metadata.xpath('span[@class="publicationDate"]/text()').re_first(r'(?:\d*\.)?\d+'))
            else:
                year = 0

            #authors
            autores = article.xpath('div[@class="authors"]/a/text()').extract()
            autores_url = article.xpath('div[@class="authors"]/a/attribute::href').extract()

            autores_list = []
            for i, autor in enumerate(autores):
                id_autor = 'ACM_author_' + str(autores_url[i])[19:]
                autores_list.append({"name": autor, 
                                    "id": id_autor
                                    })
                for author_name in author_names:
                    if id_autor in self.training_data[author_name]: 
                        id_articulo_posicion = id_articulo + '-' + str(autores.index(autor))
                        if(id_articulo_posicion in self.training_data[author_name][id_autor]) == False:
                            self.training_data[author_name][id_autor].append(id_articulo_posicion)

            #keywords
            if (article.xpath('div[@class="kw"]') != []):
                palabras_clave = article.xpath('div[@class="kw"]/text()')[1].extract()[2:-1].split(', ')
            else:
                palabras_clave = article.xpath('div[@class="kw"]')

            #snippet
            if(article.xpath('div[@class="abstract"]/text()') != []):
                snippet = article.xpath('div[@class="abstract"]/text()').extract_first()[1:-1]
            else:
                snippet = ""

            #pegando todo
            #self.articles[id_articulo] = {}
            anArticle = {"authors": autores_list,
                        "title": titulo,
                        "keywords": palabras_clave,
                        #"venue": lugar_publicacion, 
                        "year": year,
                        "abstract": snippet[:-4]
                        }
            self.articles[id_articulo] = anArticle            

            #yield anArticle


        paginations = response.xpath('//div[@id="results"]/div[@id="pagelogic"]')

        next_page = paginations.xpath('span[a='+ str(self.numpag) +']//@href').extract_first()
        #print('next_page ' + str(next_page))
        
        with open('testing.json', 'w') as a_file: #TRAINING/TESTING
            json.dump(self.training_data, a_file)
        with open('articulos_raw.json', 'w') as f:  # writing JSON object
            json.dump(self.articles,f)
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse, meta={'item': author_names})
            self.numpag += 1
        else:
            raise CloseSpider()

#consola: scrapy crawl author_articles_acm -o acm_articles_per_author.json -a author_id=81100085687