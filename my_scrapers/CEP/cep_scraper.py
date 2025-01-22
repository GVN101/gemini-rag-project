import scrapy
import json
import re
import scrapy.crawler

def clean_text(item):
    item = re.sub(r'\\u[0-9a-fA-F]{4}', '', item)
    item = re.sub(r'[\u2013\u2019\u2022\u201a\u201c\u201d\u00b1\xa0]', '-', item)
    item = re.sub(r'\s+', ' ', item).strip()
    item = re.sub(r'<br>','',item)
    item = re.sub(r'-','',item).strip()
    return item

class CEP_facilities(scrapy.Spider):
    name = 'facilities'
    start_urls = [
        'https://cep.ac.in/facilities/computer',
        'https://cep.ac.in/facilities/library',
        'https://cep.ac.in/facilities/seminar',
        'https://cep.ac.in/facilities/transport',
        'https://cep.ac.in/facilities/hostel',
        'https://cep.ac.in/facilities/canteen'
    ]

    facilities_data = {}
    total_fac = {}

    def parse(self, response):
        facility_name = response.url.split('/')[-1]
        if facility_name == 'computer':
            facility_name = 'Central Computer Facility'
        elif facility_name == 'seminar':
            facility_name = 'Seminar Hall'

        desc = response.css('p.px-2.w-full::text').get()
        print(desc)
        self.facilities_data[f"Information about the {facility_name}"] = desc
        self.total_fac["information About the facilties at College of Engineering Poonjar"] = self.facilities_data


    def closed(self, response):
        with open('college_json_data/cep.json', 'r') as f:
            data = json.load(f)
            data.append(self.total_fac)
        with open('college_json_data/cep.json', 'w') as f:
            json.dump(data,f,indent=4)