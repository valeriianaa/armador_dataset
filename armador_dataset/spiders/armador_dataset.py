import scrapy
import json
import os
import twisted
from pathlib import Path
from namesakes_acm import ArticlesACMSpider
from acm_author_articles import AuthorArticlesACMSpider
from scrapy.crawler import CrawlerProcess
from pipelines import ArmadorDatasetPipeline

# class ArmadorDatasetSpider(scrapy.Spider):
#     name = "armador_dataset"
settings_for_namesakes = {
                'USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/74.0.3729.157 Safari/537.36',
                'CONCURRENT_REQUESTS': 500,
                #'CONCURRENT_REQUESTS_PER_DOMAIN': 64
            }

settings_for_articles = {
                'USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/74.0.3729.157 Safari/537.36',
                'CONCURRENT_REQUESTS': 500,
                #'CONCURRENT_REQUESTS_PER_DOMAIN': 64,
    #             'ITEM_PIPELINES': {
                #     'pipelines.ArmadorDatasetPipeline': 300
                # }
            }

def count_in_nested_json(json_file):
    sumatoria = 0
    with open(json_file, 'r') as archivo:
        nested_json = json.loads(archivo.read())
    for k,v in nested_json.items():
        for vk, vv in v.items():
            sumatoria += len(vv)
    return sumatoria


try:
    nombres_autores = open("authors_names.json","r")
    array_autores = json.load(nombres_autores)
    # for item in array_autores:
    #   process = CrawlerProcess(settings_for_namesakes)

    #   process.crawl(ArticlesACMSpider, query=str(item))

    archivo = open("namesakes.txt").read()[:-1]
    autores_ids = archivo.split(",")

    process = CrawlerProcess(settings_for_articles)
    for item in autores_ids:
    #testing
        process.crawl(AuthorArticlesACMSpider, query=str(item), author_name=array_autores)

    #process1.start()
    process.start()
except twisted.internet.error.ConnectionLost():
    print('error de conexion. intentar de vuelta')

with open('articulos_raw.json', 'r') as archivo:
    articulos = json.loads(archivo.read())
    print('cantidad total de articulos: ' + str(len(articulos.keys())))
    print('cantidad training: '+ str(count_in_nested_json('training.json')))
 #   print('cantidad testing: ' + str(count_in_nested_json('testing.json')))

