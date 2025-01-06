#menu-item-3305
import scrapy
import json

class CEK_principal(scrapy.Spider):
    name = 'principal'
    # allowed_domains = ['cea.ac.in']
    start_urls = ['https://ceknpy.ac.in/principal']

    total_principal_data = {}

    def parse(self, response):
        principal_data = {}
        principal_name = response.css('table tbody tr td p span strong::text').get()
        principal_other_data = response.css('table tbody tr td p span::text').getall()
        print(principal_name)
        print(principal_other_data[:5])
        principal_data["Principal Name"] = principal_name
        principal_data["Department of the principal"] = principal_other_data[0]
        principal_data["Address of the principal"] = {"college":principal_other_data[1],"place and PIN Code": principal_other_data[2]} 
        principal_data["Phone Number and Fax Number of the Principal"] = principal_other_data[3]
        principal_data["Email ID of the principal"] = principal_other_data[4]
        self.total_principal_data["Data about the Principal of CEK"] = principal_data

    def closed(self, response):
        with open('college_json_data/cek.json', 'r') as f:
            data = json.load(f)
            data.append(self.total_principal_data)
        with open('college_json_data/cek.json', 'w') as f:
            json.dump(data,f,indent=4)

        