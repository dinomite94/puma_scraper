# -*- coding: utf-8 -*-
import json
import logging
import re
import scrapy
import sys
from scrapy_splash import SplashRequest

with open('links.json', 'r') as f:
    start_urls = json.load(f)


class JobSpider(scrapy.Spider):
    name = 'job'
    allowed_domains = ['about.puma.com']
    start_urls = start_urls

    custom_settings = {
        # WARNING, INFO, DEBUG
        'LOG_LEVEL': 'INFO',
    }

    def parse(self, response):
        try:
            yield {
                'body': response.body_as_unicode(),
                'table_type': 'puma_com'
            }
        except:
            e = sys.exc_info()
            logging.getLogger().warning('Problems with ' + response.url)
            logging.getLogger().warning(e)

