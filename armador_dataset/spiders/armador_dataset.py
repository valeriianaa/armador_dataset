import scrapy
import json
import os
from pathlib import Path
from namesakes_acm import ArticlesACMSpider
from acm_author_articles import AuthorArticlesACMSpider
from scrapy.crawler import CrawlerProcess

# class ArmadorDatasetSpider(scrapy.Spider):
#     name = "armador_dataset"
settings = {
                'USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
                'CONCURRENT_REQUESTS': 500
            }

# nombres_autores = open("authors_names.json","r")
# array_autores = json.load(nombres_autores)
# for item in array_autores:
# 	process = CrawlerProcess(settings)

# 	process.crawl(ArticlesACMSpider, query=str(item))

archivo = open("namesakes.txt").read()
autores_ids = archivo.split(",")

for item in autores_ids:
	#print("hola soy el item: " + item)
	process = CrawlerProcess(settings)

	process.crawl(AuthorArticlesACMSpider, query=str(item), author_name=["Roy Williams", "Sparsh Mittal", "Audun Josang"])


process.start()
#filepath = os.path.abspath("namesakes.json")
#print(filepath)
# archivo = open("namesakes.txt","r")
# los_arrays = archivo.read().split(",")
# for item in los_arrays:
# 	print(item)