# coding: utf-8

from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import Selector

from boadica.items import Produto


class BoadicaSpider(CrawlSpider):
    name = 'boadica'
    allowed_domains = ['boadica.com.br']

    start_urls = [
        'http://www.boadica.com.br/pesquisa/arm_hd/precos?ClasseProdutoX=15&CodCategoriaX=6',
    ]

    rules = [
        Rule(SgmlLinkExtractor(allow=['\&curpage\=\d+']), follow=True, callback='parse_produto'),
    ]

    def parse_produto(self, response):
        produtos = []

        sel = Selector(response)

        for tr in sel.xpath('//tr[starts-with(@id, "trProd")]'):
            produto = Produto()

            produto['fabricante'] = tr.xpath('td[2]/a/text()').extract()
            produto['modelo'] = tr.xpath('td[3]/text()').extract()
            produto['especificacoes'] = tr.xpath('td[4]/text()').extract()
            produto['preco'] = tr.xpath('td[5]/text()').extract()
            produto['vendedor'] = tr.xpath('td[6]/a/text()').extract()
            produto['vendedor_link'] = '%s%s' % ('http://www.boadica.com.br', tr.xpath('td[6]/a/@href').re(r'openWindow\(\'(.*)\'\)')[0])
            produto['local'] = tr.xpath('td[7]/text()').extract()

            produtos.append(produto)

        return produtos
