#menu-item-3305
import scrapy
import json

class MECDepartmentSpider(scrapy.Spider):
    name = 'department'
    start_urls = ['https://www.mec.ac.in/departments']

    total_department_data = []

    def parse(self, response):
        department_links = response.css('h1::text').getall()
        self.total_department_data.append(department_links)
        print(department_links)
    def parse_department(self, response):
        ...
    
    def closed(self,response):
        with open('college_json_data/mec.json', 'r') as f:
            data = json.load(f)
            data.append(self.total_department_data)
        with open('college_json_data/mec.json','w') as f:
            json.dump(data,f,indent=4)