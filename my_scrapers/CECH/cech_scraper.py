import scrapy
import scrapy.crawler

class CECH_principal(scrapy.Spider):
    name = 'cech_principal'
    start_urls = ['https://casadoor.ihrd.ac.in/principal']

    total_principal_data = {}

    def parse(self, response):
        principal_data = {}
        data = response.css('p::text').getall()
        print(data)