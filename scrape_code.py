"""
this scraping code gets the principal name and IHRD director name from the
ceconline.edu website and update the "clean.json" file we can do this method
for important data in the json file.

"""

from scrapy.crawler import CrawlerProcess
from scrapy.http import Request
from my_scrapers.cec_spider import CeconlineSpider
import json

class AdminExtractor(CeconlineSpider):
    def __init__(self):
        self.admin_data = {}
        self.count = 1
        self.data_unique_check_set = set()

    """Extended Spider to fetch admin details specifically."""
    def start_requests(self):
        admin_url = "https://ceconline.edu/administrators"  # Replace with the actual page URL
        yield Request(url=admin_url, callback=self.parse_administrations)

    def parse_administrations(self, response):
        admin_details = response.xpath('//div[contains(@class, "stm-teacher")]')
        for admin in admin_details:
            designation = admin.xpath('.//div[contains(@class, "stm-teacher__position")]/text()').get()
            cleaned_designation = self.clean_text(designation)

            staff_name = admin.xpath('.//div[contains(@class, "stm-teacher__name")]/text()').get()
            cleaned_staff_name = self.clean_text(staff_name)


            if cleaned_designation and cleaned_staff_name and (cleaned_designation, cleaned_staff_name) not in self.data_unique_check_set:
                self.admin_data[self.count] = {}
                self.admin_data[self.count]["position"] = cleaned_designation
                self.admin_data[self.count]["admin_name"] = cleaned_staff_name
                self.data_unique_check_set.add((cleaned_designation, cleaned_staff_name))
                self.count += 1
            
            print(self.admin_data)
            with open('clean.json', 'r') as file:
                data = json.load(file)

            if self.admin_data.get(1,None):
                data['Administration'] = {"IHRD Director": self.admin_data[1]['admin_name']}
            if self.admin_data.get(2,None):
                data['Engineering Colleges']['College of Engineering Chengannur']['Principal_name'] = self.admin_data[2]['admin_name']

            with open('clean.json', 'w') as file:
                json.dump(data, file, indent=4)
            
        

# Run the spider
process = CrawlerProcess(settings={
    "LOG_LEVEL": "ERROR",  # Set log level to reduce verbosity
})
process.crawl(AdminExtractor)
process.start()

