# coding: utf-8

from scrapy.item import Item, Field


class Produto(Item):
    fabricante = Field()
    modelo = Field()
    especificacoes = Field()
    preco = Field()
    vendedor = Field()
    vendedor_link = Field()
    local = Field()
    categoria = Field()
