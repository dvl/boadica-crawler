# coding: utf-8

from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import Selector

from boadica.items import Produto


class BoadicaSpider(CrawlSpider):
    name = 'boadica'
    allowed_domains = ['boadica.com.br']

    start_urls = [
        'http://www.boadica.com.br/pesquisa/mem_cpu/precos?ClasseProdutoX=3&CodCategoriaX=14&XT=9&XK=9&XF=624',   # Memoria Kingstom
        'http://www.boadica.com.br/pesquisa/mem_cpu/precos?ClasseProdutoX=3&CodCategoriaX=14&XT=9&XK=9&XF=370',   # Memoria Corsair
        'http://www.boadica.com.br/pesquisa/mem_cpu/precos?ClasseProdutoX=3&CodCategoriaX=14&XT=9&XK=9&XF=1818',  # Memoria G-Skill
        'http://www.boadica.com.br/pesquisa/cpu_proc/precos?ClasseProdutoX=5&CodCategoriaX=3&XG=14',  # i5 1150
        'http://www.boadica.com.br/pesquisa/cpu_proc/precos?ClasseProdutoX=5&CodCategoriaX=4&XG=14',  # i7 1150
        'http://www.boadica.com.br/pesquisa/multi_placavideo/precos?ClasseProdutoX=2&CodCategoriaX=7&XG=3&XJ=2&XF=1425',  # GTX EVGA
        'http://www.boadica.com.br/pesquisa/multi_placavideo/precos?ClasseProdutoX=2&CodCategoriaX=7&XG=3&XJ=2&XF=1911',  # GTX Zogis
        'http://www.boadica.com.br/pesquisa/multi_placavideo/precos?ClasseProdutoX=2&CodCategoriaX=7&XG=3&XJ=2&XF=2144',  # GTX Zotac
        'http://www.boadica.com.br/pesquisa/multi_placavideo/precos?ClasseProdutoX=2&CodCategoriaX=7&XG=4&XJ=8&XT=2',     # R7
        'http://www.boadica.com.br/pesquisa/arm_hd/precos?ClasseProdutoX=15&CodCategoriaX=6',  # SSD
        'http://www.boadica.com.br/pesquisa/cpu_plmae/precos?ClasseProdutoX=5&CodCategoriaX=26&XG=14&XF=8',     # MOBO Asus 1150
        'http://www.boadica.com.br/pesquisa/cpu_plmae/precos?ClasseProdutoX=5&CodCategoriaX=26&XG=14&XF=5328',  # MOBO GigaBite 1150
        'http://www.boadica.com.br/pesquisa/out_gabi/precos?ClasseProdutoX=8&CodCategoriaX=45&XF=1162',  # Gabinete Thermaltake
        'http://www.boadica.com.br/pesquisa/out_gabi/precos?ClasseProdutoX=8&CodCategoriaX=45&XF=1171',  # Gabinete Coolermaster
    ]

    rules = [
        Rule(SgmlLinkExtractor(allow=['\&curpage\=\d+']), follow=True, callback='parse_produto'),
    ]

    def parse_produto(self, response):
        produtos = []

        sel = Selector(response)

        cat = sel.xpath('(//div[@class="breadcumb"]/a[2])[1]/text()').extract()

        for tr in sel.xpath('//tr[starts-with(@id, "trProd")]'):
            produto = Produto()

            produto['fabricante'] = tr.xpath('td[2]/a/text()').extract()
            produto['modelo'] = tr.xpath('td[3]/text()').extract()
            produto['especificacoes'] = tr.xpath('td[4]/text()').extract()
            produto['preco'] = tr.xpath('td[5]/text()').extract()
            produto['vendedor'] = tr.xpath('td[6]/a/text()').extract()
            produto['vendedor_link'] = '%s%s' % ('http://www.boadica.com.br', tr.xpath('td[6]/a/@href').re(r'openWindow\(\'(.*)\'\)')[0])
            produto['local'] = tr.xpath('td[7]/text()').extract()
            produto['categoria'] = cat

            produtos.append(produto)

        return produtos
