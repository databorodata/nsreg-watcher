# -*- coding: utf-8 -*-
import scrapy
from nsreg.items import NsregItem

from ..utils import find_price
# работает, нет переноса, только с консультацией

REGEX_PATTERN = r"([0-9]{3,}).*"
EMPTY_PRICE = {
    'price_reg': None,
    'price_prolong': None,
    'price_change': None,
}


class NsregSafeSpider(scrapy.Spider):
    name = 'nsreg_safe'
    allowed_domains = ['www.safereg.ru']
    start_urls = ['https://www.safereg.ru/site/tariffs']

    def parse(self, response):
        price_reg = response.xpath(
            '/html/body/section/div/div/div/div[2]/div[1]/div[2]/span/text()').get()
        price_reg = find_price(REGEX_PATTERN, price_reg)

        price_prolong = response.xpath(
            '/html/body/section/div/div/div/div[2]/div[2]/div[2]/span/text()').get()
        price_prolong = find_price(REGEX_PATTERN, price_prolong)

        price_change = response.xpath(
            '/html/body/section/div/div/div/div[2]/div[3]/div[2]/span/text()').get()
        price_change = find_price(REGEX_PATTERN, price_change)

        item = NsregItem()
        item['name'] = "ООО «Безопасный регистратор»"
        price = item.get('price', EMPTY_PRICE)
        price['price_reg'] = price_reg
        price['price_prolong'] = price_prolong
        price['price_change'] = price_change
        item['price'] = price

        yield item
