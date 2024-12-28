import scrapy
import json

class BoardOfGovernorsSpider(scrapy.Spider):
    name = "bog"
    start_urls = ['https://ceconline.edu/board-of-governors/']
    
    total_board_of_governors = []

    def parse(self, response):
        table = response.xpath('//div[@class="wpb_wrapper"]//table[contains(., "Board of Governors")]')
        rows = table.xpath('.//tr[td]') 

        for row in rows:
            # sl_no = row.xpath('td[1]/strong/text()').get()
            name_designation = row.xpath('td[2]/strong/text()').get()
            designation = row.xpath('td[3]/strong/text()').get()
            role = row.xpath('td[4]/strong/text()').get()
            if  name_designation and designation:
                self.total_board_of_governors.append({
                    # 'Sl.No': sl_no.strip(),
                    'Name and Designation': name_designation.strip(),
                    'Designation': designation.strip(),
                    'Role': role.strip() if role else '',
                })
    def closed(self, response):
        if(self.total_board_of_governors):
            data_dict = {"Board of Governors of CEC Related Data": self.total_board_of_governors}
            with open('output.json','r') as f:
                data = json.load(f)
                data.append(data_dict)
            with open('output.json', 'w') as f:
                json.dump(data, f, indent=4)