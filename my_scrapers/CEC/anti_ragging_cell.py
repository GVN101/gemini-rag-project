import scrapy
import json

class AntiRaggingSpider(scrapy.Spider):
    name = "antiragging_spider"
    start_urls = ["https://ceconline.edu/about/committees/anti_ragging/"]

    total_Anti_Ragging_Cell_data = ''

    def parse(self, response):
        # More robust XPath using contains()
        antiragging_section = response.xpath(
            '//div[contains(@class, "wpb_text_column") and contains(@class, "wpb_content_element") and contains(@class,"vc_custom_")]'
        )

        if antiragging_section:
            details = {}
            functions = []
            for li in antiragging_section.xpath('.//ul/li'):
                function_text = li.xpath('.//text()').get("").strip()
                if function_text:
                    functions.append(function_text)
            if functions:
                details["functions"] = functions
                self.total_Anti_Ragging_Cell_data = {"details_about_anti_ragging_cell": details}
            else:
                print("No functions found within the anti-ragging section.")
        else:
            print("Anti-ragging section not found. Check the XPath.")

    def closed(self, response):
        if(self.total_Anti_Ragging_Cell_data):
            data_dict = {"Board of Governors of CEC Related Data": self.total_Anti_Ragging_Cell_data}
            with open('output.json','r') as f:
                data = json.load(f)
                data.append(data_dict)
            with open('output.json', 'w') as f:
                json.dump(data, f, indent=4)