# -*- coding: utf-8 -*-
import scrapy
import re
re_postid = r"id(\d{4,})"

class Mogi1Spider(scrapy.Spider):
    name = 'mogi1'
    allowed_domains = ['mogi.vn']
    start_urls = ['https://mogi.vn/']

    def __init__(self):
        self.stop_flag = False

        self.links = [x for x in range(5)]

    def start_requests(self):
        for i in range(5):
            url = "https://mogi.vn/ho-chi-minh/mua-nha?cp=" + str(i)
            yield scrapy.http.Request(url=url, callback=self.parse_page)

            # links = page_response.css('div[class="prop-info"]').css('a::attr(\'href\')').getall()
            # for link in links:
            #     link = "https://mogi.vn/" + link

            #     link_response = scrapy.http.TextResponse(url=link)
            #     with open("result1.txt", "a+") as file:
            #         file.write(re.findall(pattern=re_postid, string=link_response.url)[0] + "\n")

    def parse_page(self, response):         
        url = response.url
        order = int(re.findall(r"cp=(\d+)", url))

        links = response.css('div[class="prop-info"]').css('a::attr(\'href\')').getall()
        self.links[order] = links

            # yield scrapy.Request(url=link, callback=self.parse_link)
            
    # def parse_link(self, response):
    #     with open("result3.txt", "w+") as file:
    #         file.write(re.findall(pattern=re_postid, string=response.url)[0] + "\n")
    #     file.close()
                