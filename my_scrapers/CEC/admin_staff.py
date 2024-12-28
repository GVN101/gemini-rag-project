import scrapy
import json

class AdminStaffSpider(scrapy.Spider):
    name = "admin_staff"
    start_urls = ["https://ceconline.edu/about/administration/administrative-staff/"]

    total_admin_staff_data = []

    def parse(self, response):
        table = response.xpath("//h2[text()='Administrative Staff']/following-sibling::div//table")

        if not table:
            self.logger.error("Table not found. Verify the XPath selector.")
            return

        rows = table.xpath(".//tr")

        staff_data = []
        for row in rows[1:]:  # Skip header row
            name = row.xpath(".//td[1]//text()").get()
            designation = row.xpath(".//td[2]//text()").get()

            if name and designation:
                staff_data.append({
                    "name": name.strip(),
                    "designation": designation.strip()
                })

        if staff_data:
            self.total_admin_staff_data.append({"Details about Administrative Staff of CEC": staff_data})
    
    def closed(self, response):
        with open('output.json', 'r') as f:
            data = json.load(f)
            data.append(self.total_admin_staff_data)
        with open('output.json','w') as f:
            json.dump(data, f, indent=4)
