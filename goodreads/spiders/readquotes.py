# -*- coding: utf-8 -*-
import scrapy


class ReadquotesSpider(scrapy.Spider):
    name = 'readquotes'
    # allowed_domains = ['https://www.goodreads.com/quotes']
    start_urls = ['http://www.goodreads.com/quotes/']

    def parse(self, response):
        lenxp = '//div[@class="quoteDetails"]'
        lngth = len(response.xpath(lenxp))
        quotxp = '(//div[@class="quoteDetails"])[{}]/div[@class="quoteText"]/text()'
        autxp = '(//div[@class="quoteDetails"])[{}]/div[@class="quoteText"]/span/text()'
        tagxp = '(//div[@class="quoteDetails"])[{}]/div[@class="quoteFooter"]/div[1]/a[not(@class)]/text()'
        for i in range(lngth):
            quotxpath = quotxp.format(i+1)
            authxpath = autxp.format(i+1)
            tagsxpath = tagxp.format(i+1)
            yield {
                'Quotes':(response.xpath(quotxpath).get()).strip(),
                'Author':(response.xpath(authxpath).get()).strip(),
                'Tags':response.xpath(tagsxpath).getall()
            }
        nextpage = response.xpath('//div[@style="text-align: right; width: 100%"]/div/a[@class="next_page"]/@href').get()
        # print(nextpage)
        if nextpage is not None:
            nextpage = response.urljoin(nextpage)
            yield scrapy.Request(nextpage, callback=self.parse)
            # yield response.follow(nextpage, callback=self.parse)

