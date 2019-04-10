# -*- coding: utf-8 -*-
import json
import logging
import re
import scrapy
import sys
from scrapy_splash import SplashRequest


class IndexSpider(scrapy.Spider):
    name = 'index'
    allowed_domains = ['about.puma.com']
    start_urls = ['https://about.puma.com/en/careers/job-openings#jobfinder']

    custom_settings = {
        # WARNING, INFO, DEBUG
        'LOG_LEVEL': 'INFO',
    }

    # profile_data_extractor = re.compile(r'var\s+data\s*=\s*(.*);')

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url=url,
                callback=self.parse,
                endpoint='execute',
                args={'lua_source': '''function main(splash, args)
  -- load website
  assert(splash:go(args.url))
  assert(splash:wait(1))

  -- wait until all job teasers are displayed
  local result, error = splash:wait_for_resume([[
    function main(splash) {
        let lastLoadHref = '';

        function loadMore() {
            const loadMoreButton = document.querySelector('.load-more');

            if (loadMoreButton && (loadMoreButton.href != lastLoadHref)) {
                lastLoadHref = loadMoreButton.href;
                loadMoreButton.click();

                setTimeout(loadMore, 1);
            } else if (document.querySelectorAll('.job-teaser a').length == document.querySelector('.job-post-boilerplate .headline .number').innerText) {
                splash.resume();
            } else {
                setTimeout(loadMore, 1)
            }
        }

        loadMore();
  	}
  ]])
  
  -- get hrefs for jobs
  local get_hrefs = splash:jsfunc([[
    function(sel) {
    	var elems = document.querySelectorAll(sel);
    	var hrefs = [];
    	[].forEach.call(elems, e => hrefs.push(e.href));
    	
    	return hrefs;
  	}
  ]])
  
  return get_hrefs('.job-teaser a')
end'''})

    def parse(self, response):
        links = response.data
        logging.getLogger().info('{} Links found'.format(len(links)))

        with open('links.json', 'w') as f:
            f.write(json.dumps(links))

        """
        for link in links:
            yield response.follow(link, callback=self.parse_profile)
        """

    def parse_profile(self, response):
        pass
        """
        try:
            body = response.body_as_unicode()
            item = json.loads(IndexSpider.profile_data_extractor.search(body).group(1))
            item['table_type'] = 'weltklassejungs_de'
            yield item
        except:
            e = sys.exc_info()
            logging.getLogger().warning('Problems with ' + response.url)
            logging.getLogger().warning(e)
        """
