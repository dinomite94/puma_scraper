# -*- coding: utf-8 -*-
import base64
import json
import logging
import re
import scrapy
import sys
from scrapy_splash import SplashRequest

with open('out/links.json', 'r') as f:
    start_urls = json.load(f)


class JobSpider(scrapy.Spider):
    name = 'job'
    allowed_domains = ['about.puma.com']
    start_urls = start_urls

    custom_settings = {
        # WARNING, INFO, DEBUG
        'LOG_LEVEL': 'INFO',
    }

    url_id_extractor = re.compile(r'\/jobs\/(.*)\?')
    json_extractor = re.compile(r'<script type="application\/ld\+json">([^<]*?"@type": "JobPosting",.*?)</script>', re.MULTILINE | re.DOTALL)

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url=url,
                callback=self.parse,
                endpoint='execute',
                args={'lua_source': '''function main(splash, args)
  assert(splash:go(args.url))
  splash:set_viewport_full()
  splash:wait(0.5)
  
  splash:select('.accept-cookies-button').mouse_click()
  splash:set_viewport_full()
  splash:wait(0.1)

  return {
    date_location = splash:select('.date-location').node.innerHTML,
    html = splash:html(),
    png = splash:png(),
  }
end'''})

    def parse(self, response):
        try:
            image_data = base64.b64decode(response.data['png'])
            job_id = JobSpider.url_id_extractor.search(response.url).group(1)
            with open('out/jobs/' + job_id + '.png', 'wb') as f:
                f.write(image_data)

            data = json.loads(JobSpider.json_extractor.search(response.data['html']).group(1))
            data['date_location'] = response.data['date_location']

            with open('out/jobs/' + job_id + '.json', 'w') as f:
                json.dump(data, f)
        except:
            e = sys.exc_info()
            logging.getLogger().warning('Problems with ' + response.url)
            logging.getLogger().warning(e)
