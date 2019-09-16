import scrapy
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.exceptions import CloseSpider

import json

class AuthorArticlesACMSpider(scrapy.Spider):
    articles_count = 0
    numpag = 2
    data = []
    training_data = {}
    name = "author_articles_acm"
    articles = {}

    #rules = {
    # Rule(LinkExtractor(allow =(), restrict_xpaths = ('//h2[contains(@class,"item__title")]/a')), callback = 'parse', follow = False)
		#Rule(LinkExtractor(allow = (), restrict_xpaths = ('//*[(@id = "gs_n")]//a//b')))
    #}
    
    # getting the query from console
    def start_requests(self):   
        url = getattr(self, 'query', None)
        author_names = getattr(self, 'author_name', None)
        yield scrapy.Request(url, self.parse, meta={'item': author_names}) 

    # parsing
    def parse(self, response):
        author_names = response.meta.get('item')
        print("author_names " + str(author_names))
        with open('articulos_raw.json', 'w+') as archivo:
            if archivo.read() != '':    
                self.data = json.load(archivo)
        with open('training.json') as a_file:
            training_data = str(a_file.read())
            print('training_data: ' + str(training_data))
            self.training_data = json.loads(training_data)
        
        #for each result
        for article in response.xpath('//div[@id="results"]/div[@class="details"]'):
            
            anArticle = []      
            
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
                        self.training_data[author_name][id_autor].append(id_articulo_posicion)
                    #print('training_data ahora: ' + str(self.training_data)) 
                    #print('un autor:' + str(self.training_data[autor][id_autor]))
                    #if a_file.read() != '':
                       # print('holo' + training_data)    
                        #training_data = json.load(a_file)
                        #print('todo el json: ' + str(training_data))
                        #print('un autor:' + str(training_data[autor][id_autor]))
                    #else:
                      #  print('se borro el archivo')
                            #self.training_data[autor][id_autor].append(str(autores.index(autor)))
                    #print('soy el autor: ' + str(autor)+' y estoy en la posicion: ' + str(autores.index(autor)))

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
            
            #self.articles.append(anArticle)#aca armar el json
            

            #yield anArticle

            # self.articles_count += 1
            # if self.articles_count >= 20:
            #     print(json.dumps(self.articles))
            #     raise CloseSpider('enough_articles')


        paginations = response.xpath('//div[@id="results"]/div[@id="pagelogic"]')

        next_page = paginations.xpath('span[a='+ str(self.numpag) +']//@href').extract_first()
        
        if next_page is not None:
            with open('training.json', 'w+') as a_file:
                json.dump(self.training_data, a_file)
            yield response.follow(next_page, callback=self.parse, meta={'item': author_names})
            self.numpag += 1
        else:
            #self.data = self.data + self.articles
            with open('training.json', 'w+') as a_file:
                json.dump(self.training_data, a_file)
            with open('articulos_raw.json', 'w+') as f:  # writing JSON object
                json.dump(self.articles,f)
            raise CloseSpider()


# class AuthorOrgACMSpider(scrapy.Spider):
#     def start_requests(self):   
#         url = 'https://dl.acm.org/author_page.cfm?id='
#         author_id = getattr(self, 'author_id', None)
#         #author_id = 'outliers'
#         if author_id is not None:
#             url = url + author_id
#         yield scrapy.Request(url, self.parse)
#consola: scrapy crawl author_articles_acm -o acm_articles_per_author.json -a author_id=81100085687