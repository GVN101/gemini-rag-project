#menu-item-3305
import scrapy
import json

def clear_file():
    with open('college_json_data/cek.json','w') as f:
        f.write('[]')

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

class CEK_board_members(scrapy.Spider):
    name = 'board_members'
    start_urls = ['']

    total_board_members_data = {}

    def parse(self, response):
        member_data = response.css('div.elementor-shortcode ')
        print(member_data)

class CEK_management(scrapy.Spider):
    name = 'board_members'
    # allowed_domains = ['cea.ac.in']
    start_urls = ['https://www.ceknpy.ac.in/management']

    total_management_data = {}

    def parse(self, response):
        member_data = response.css('div.sec-title div p span::text').getall()
        print(member_data)
        management_data = ' '.join(member_data)
        self.total_management_data["Data about Management of CEK"] = management_data

    def closed(self, response):
        with open('college_json_data/cek.json', 'r') as f:
            data = json.load(f)
            data.append(self.total_management_data)
        with open('college_json_data/cek.json', 'w') as f:
            json.dump(data,f,indent=4)

class CEK_admin_staff(scrapy.Spider):
    name = 'admin_staff'
    # allowed_domains = ['cea.ac.in']
    start_urls = ['https://www.ceknpy.ac.in/adminstaff']

    total_admin_staff = {}

    def parse(self, response):
        final_admin_staff_data = []
        admin_staff_data = response.css('div.sec-title div table tr p::text').getall()
        cleaned_admin_staff_data = []
        for i in admin_staff_data:
            if i not in ['\xa0','\r\n']:
                cleaned_admin_staff_data.append(i)

        print(cleaned_admin_staff_data)
        i = 0
        while(i<len(cleaned_admin_staff_data)):
            data = {}
            data["Name"] = cleaned_admin_staff_data[i]
            data["Designation"] = cleaned_admin_staff_data[i+1]
            data["E-mail"] = cleaned_admin_staff_data[i+2]
            data["Phone Number"] = cleaned_admin_staff_data[i+3]
            i+=4
            final_admin_staff_data.append(data)
        self.total_admin_staff["Admnistration staff Data"] = final_admin_staff_data
        
    def closed(self, response):
        with open('college_json_data/cek.json', 'r') as f:
            data = json.load(f)
            data.append(self.total_admin_staff)
        with open('college_json_data/cek.json', 'w') as f:
            json.dump(data,f,indent=4)

class CEK_overview(scrapy.Spider):
    name = 'overview'
    # allowed_domains = ['cea.ac.in']
    start_urls = ['https://www.ceknpy.ac.in/overview']

    total_overview_data = ''

    def parse(self, response):
        data = {}
        overview_data = response.css('div.sec-title div.desc p::text, div.sec-title div::text').getall()
        print(overview_data)
        data["Overview of the college (CEK)"] = overview_data[1] + ' ' + overview_data[2]
        data["Vision of CEK"] = overview_data[3]
        data["Mission"] = overview_data[4]

        data["Programmes Offered"] = {
            "Btech": [overview_data[5], overview_data[6], overview_data[7], overview_data[8]],
            "Mtech": overview_data[10]
        }
        data["Memorandum of Understanding"] = overview_data[11]
        data["Student Professional Bodies"] = overview_data[12]
        data["Data about College Library"] = overview_data[13]
        data["Training and Placement Cell of CEK"] = overview_data[14]
        data["Alumni details about CEK"] = overview_data[15]
        data["Parent-Teacher Association (PTA) of CEK"] = overview_data[16]
        data["College Hostel"] = overview_data[17]
        data["Canteen"] = overview_data[18]
        data["ATM Counter"] =  overview_data[19]
        data["Sports and Cultural Festivals"] = overview_data[20]
        self.total_overview_data = data

    def closed(self, response):
        with open('college_json_data/cek.json', 'r') as f:
            data = json.load(f)
            data.append(self.total_overview_data)
        with open('college_json_data/cek.json', 'w') as f:
            json.dump(data,f,indent=4)