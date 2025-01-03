#menu-item-3305
import scrapy
import json

class AECDepartmentSpider(scrapy.Spider):
    name = 'department'
    # allowed_domains = ['cea.ac.in']
    start_urls = ['https://cea.ac.in/']

    total_department_data = []

    def parse(self, response):
        self.logger.info("Parsing the main departments page.")
        department_links = []
        department_links.append(response.css('#menu-item-3305 a::attr(href)').get()) # Mechanical Engineering link
        department_links.append(response.css('#menu-item-4041 a::attr(href)').get()) # Electrical and Electronics Engineering link
        department_links.append(response.css('#menu-item-4390 a::attr(href)').get()) # Electronics and Communication link
        department_links.append(response.css('#menu-item-4806 a::attr(href)').get()) # Computer Science and Engineering link
        department_links.append(response.css('#menu-item-4486 a::attr(href)').get()) # Applied Science Link
        print(department_links)

        if not department_links:
            self.logger.warning("No department links found. Check the CSS selector.")

        for department_link in department_links:
            yield response.follow(department_link, self.parse_department)

    def parse_department(self, response):
        department_title = response.css('h1::text').get()
        print(department_title)
        department_data = {department_title:{}}
        about_content = response.css('div.elementor-container.elementor-column-gap-default p::text, div.elementor-container.elementor-column-gap-default p span::text').get()
        department_data[department_title]["About the department"] = about_content
        self.total_department_data.append(department_data)
    
    def closed(self,response):
        with open('college_json_data/aec.json', 'r') as f:
            data = json.load(f)
            data.append({"About the Department of Adoor Engineering College":self.total_department_data})
        with open('college_json_data/aec.json','w') as f:
            json.dump(data,f,indent=4)

        