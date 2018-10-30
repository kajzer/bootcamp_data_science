# -*- coding: utf-8 -*-
import scrapy


class MiniSpider(scrapy.Spider):
    name = 'mini'
    # allowed_domains = ['https://ww2.mini.pw.edu.pl/','https://www.mini.pw.edu.pl/']
    start_urls = ['https://ww2.mini.pw.edu.pl/wydzial/komisje-senackie/']

    def parse(self, response):
        for text in response.xpath("//div[contains(@class, 'post-content')]//li"):
            if len(text.re(r'(prof|dr|hab|inż|mgr)')) > 0:
                # print(text.css('a')[0].xpath('text()').extract()[0])
                yield {
                    text.xpath('text()')[0].extract(): text.css('a')[0].xpath('text()').extract()[0]
                }
        for a in response.css('ul li a'):
            yield response.follow(a, callback=self.parse)