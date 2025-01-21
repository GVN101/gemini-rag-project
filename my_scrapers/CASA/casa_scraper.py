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

class CASA_principal(scrapy.Spider):
    name = 'principal'
    start_urls = ['https://casadoor.ihrd.ac.in/principal']

    total_principal_data = {}

    def parse(self,response):
        principal_data = {}
        data = response.css('div.col-md-8.col-xs-12.aboutus.no-gutters p::text').getall()
        print(data)
        data_split = data[0].split()
        principal_data["Principal Name"] = data_split[0] + ' ' + data_split[1]
        principal_data["About the Principal"] = data[0]
        self.total_principal_data["About the principal"] = principal_data

    def closed(self, reason):
        # This method is called when the spider is closed
        with open('college_json_data/casa.json', 'r') as f:
            existing_data  = json.load(f)
            existing_data.append(self.total_principal_data)
        with open('college_json_data/casa.json','w') as f:
            json.dump(existing_data, f, indent=4)

class CASA_Committee(scrapy.Spider):
    name = 'committees'
    start_urls = ['https://casadoor.ihrd.ac.in/committees']

    total_committee_data = {}

    def parse(self,response):
        committee_data = {}
        data = response.css('ul.programsoffer li::text').getall()
        print(data)
        committee_data["Members of Anti Ragging Commitee"] = [data[i] for i in range(5)]
        committee_data["Members of Grievance Redressal Cell"] = [data[i] for i in range(5,8)]
        committee_data["Other Coordinatores of different forums"] = [data[i] for i in range(8,len(data))]
        self.total_committee_data["Data about the members of different committees"] = committee_data

    def closed(self, reason):
        # This method is called when the spider is closed
        with open('college_json_data/casa.json', 'r') as f:
            existing_data  = json.load(f)
            existing_data.append(self.total_committee_data)
        with open('college_json_data/casa.json','w') as f:
            json.dump(existing_data, f, indent=4)

class CASA_overview(scrapy.Spider):
    name = 'overview'
    start_urls = ['https://casadoor.ihrd.ac.in/overview']

    total_overview_data = {}

    def parse(self,response):
        overview_data = response.css('div.col-md-12.col-xs-12 p::text').getall()
        self.total_overview_data["Overview Information of college of Applied science Adoor"] = overview_data
    def closed(self, reason):
        # This method is called when the spider is closed
        with open('college_json_data/casa.json', 'r') as f:
            existing_data  = json.load(f)
            existing_data.append(self.total_overview_data)
        with open('college_json_data/casa.json','w') as f:
            json.dump(existing_data, f, indent=4)

class CASA_Mission_and_Vision(scrapy.Spider):
    name = 'overview'
    start_urls = ['https://casadoor.ihrd.ac.in/mission-vision']

    total_mission_and_vision_data = {}

    def parse(self,response):
        mission_and_vision_data = {}
        data = response.css('div.col-md-12.col-xs-12 p::text').getall()
        print(data)
        mission_and_vision_data["Vision of the college (CASA)"] = data[0]
        mission_and_vision_data["Mission of the college (CASA)"] = data[1]
        core_values = {
            "Excellence": data[3],
            "Ethics": data[4],
            "Discipline and Diginity": data[5],
            "Student_focus":data[6],
            "Collaboration and Public Engagement": data[7],
            "Gender Equality": data[8]
        }
        mission_and_vision_data["About the Core Values upheld by the institution"] = core_values
        self.total_mission_and_vision_data["About the mission and Vision of CASA"] = mission_and_vision_data
    def closed(self, reason):
        # This method is called when the spider is closed
        with open('college_json_data/casa.json', 'r') as f:
            existing_data  = json.load(f)
            existing_data.append(self.total_mission_and_vision_data)
        with open('college_json_data/casa.json','w') as f:
            json.dump(existing_data, f, indent=4)


class CASA_Anti_rag_cell(scrapy.Spider):
    name = 'anit_rag_cell'
    start_urls = ['https://casadoor.ihrd.ac.in/anti-ragging']

    total_anti_ragging_cell_data = {}

    def parse(self,response):
        arc_data = {}
        data = response.css('div.col-md-12.col-xs-12 p::text').getall()
        arc_data["About the Anti Ragging Cell of CASA"] = data[0] + ' ' + data[1]
        data = response.css('ul.programsoffer li::text').getall()
        arc_data["The Objectives of the Anti Ragging Cell"] = [data[i] for i in range(4)]
        self.total_anti_ragging_cell_data["About the Anti Ragging Cell of CASA"] = arc_data

    def closed(self, reason):
        # This method is called when the spider is closed
        with open('college_json_data/casa.json', 'r') as f:
            existing_data  = json.load(f)
            existing_data.append(self.total_anti_ragging_cell_data)
        with open('college_json_data/casa.json','w') as f:
            json.dump(existing_data, f, indent=4)

class CASA_NSS(scrapy.Spider):
    name = 'nss'
    start_urls = ['https://casadoor.ihrd.ac.in/nss']

    total_nss_data = {}

    def parse(self,response):
        nss_data = {}
        nss = response.css('div.col-md-12.col-xs-12 p::text').getall()
        nss_data["About the NSS forum"] =  nss[0] + ' ' + nss[1]
        obj = response.css('ul.programsoffer li::text').getall()
        nss_data["About objectives the NSS"] = [clean_text(obj[i]) for i in range(4)]
        nss_data["Major Activties in NSS"] = [clean_text(obj[i]) for i in range(4,12)]
        nss_data["Achievements of NSS"] = [clean_text(obj[i]) for i in range(12,15)]
        nss_data["People to be contacted for NSS"] = {
            1:obj[15],
            2:obj[16]
        }
        self.total_nss_data["About the NSS"] = nss_data

    def closed(self, reason):
        with open('college_json_data/casa.json', 'r') as f:
            existing_data  = json.load(f)
            existing_data.append(self.total_nss_data)
        with open('college_json_data/casa.json','w') as f:
            json.dump(existing_data, f, indent=4)

class CASA_cs_department(scrapy.Spider):
    name = 'cs_department'
    start_urls = ['https://casadoor.ihrd.ac.in/departments/computerscience']

    total_cs_dep_data = {}

    def parse(self,response):
        cs_data = {}
        cs_desc = response.css('div.col-md-7.col-xs-12 p::text').get()
        print(cs_desc)
        programmes = response.css(' div.col-md-7.col-xs-12 ul li::text').getall()
        print(programmes)
        pro_data = {
                "PG Programme of CS": clean_text(programmes[0]),
                "UG Programmes of CS": [
                    clean_text(programmes[1]),
                    clean_text(programmes[2])
                ],
                "IHRD Programmes of CS": [
                    clean_text(programmes[3]),
                    clean_text(programmes[4])
                ]
            }
        cs_data["Information (description) about CS Department "] = cs_desc
        cs_data["Information about the various programme offered by Computer Science Department"] = pro_data
        faculty_names_and_positions = response.css('div.Name::text,div.Position::text').getall()
        print(faculty_names_and_positions)
        faculty_info = []
        j = 1
        for i in range(2,len(faculty_names_and_positions),2):
            faculty_info.append({
                j:{
                    "Faculty Name":clean_text(faculty_names_and_positions[i]),
                    "Faculty Designation": clean_text(faculty_names_and_positions[i+1])
                }
            })
            j+=1
        cs_data["Information about the faculty of Computer Science Department"] = faculty_info
        self.total_cs_dep_data = cs_data
        

    def closed(self, reason):
        with open('college_json_data/casa.json', 'r') as f:
            existing_data  = json.load(f)
            existing_data.append(self.total_cs_dep_data)
        with open('college_json_data/casa.json','w') as f:
            json.dump(existing_data, f, indent=4)

class CASA_ec_department(scrapy.Spider):
    name = 'ec_department'
    start_urls = ['https://casadoor.ihrd.ac.in/departments/electronics']

    total_ec_dep_data = {}

    def parse(self,response):
        ec_data = {}
        ec_desc = response.css('div.col-md-7.col-xs-12 p::text').get()
        print(ec_desc)
        programmes = response.css('div.col-md-7.col-xs-12 ul li::text').getall()
        print(programmes)
        pro_data = {
                "PG Programme of EC": clean_text(programmes[0]),
                "UG Programmes of EC": [
                    clean_text(programmes[1])
                ],
            }
        ec_data["Information (description) about Electronics Department "] = ec_desc
        ec_data["Information about the various programme offered by Computer Science Department"] = pro_data
        faculty_names_and_positions = response.css('div.Name::text,div.Position::text').getall()
        print(faculty_names_and_positions)
        faculty_info = []
        j = 1
        for i in range(0,len(faculty_names_and_positions),2):
            if(clean_text(faculty_names_and_positions[i])):
                faculty_info.append({
                j:{
                    "Faculty Name":clean_text(faculty_names_and_positions[i]),
                    "Faculty Designation": clean_text(faculty_names_and_positions[i+1])
                }
            })
                j+=1
        ec_data["Information about the faculty of Electronics Department"] = faculty_info
        self.total_ec_dep_data = ec_data

    def closed(self, reason):
        with open('college_json_data/casa.json', 'r') as f:
            existing_data  = json.load(f)
            existing_data.append(self.total_ec_dep_data)
        with open('college_json_data/casa.json','w') as f:
            json.dump(existing_data, f, indent=4)

class CASA_cm_department(scrapy.Spider):
    name = 'cm_department'
    start_urls = ['https://casadoor.ihrd.ac.in/departments/commerce-management']

    total_cm_dep_data = {}

    def parse(self, response):
        cm_data = {}
        cm_desc = response.css('div.col-md-7.col-xs-12 p::text').get()
        print(cm_desc)
        programmes = response.css('div.col-md-7.col-xs-12 ul li::text').getall()
        print(programmes)
        pro_data = {
                "PG Programme of Commerce and Managment": clean_text(programmes[0]),
                "UG Programmes of Commerce and Managment": [
                    clean_text(programmes[1]),
                    clean_text(programmes[2])
                ],
            }
        cm_data["Information (description) about Commerce and Management Department "] = cm_desc
        cm_data["Information about the various programme offered by Commerce and Management Department"] = pro_data
        faculty_names_and_positions = response.css('div.Name::text,div.Position::text').getall()
        print(faculty_names_and_positions)
        faculty_info = []
        j = 1
        for i in range(0,len(faculty_names_and_positions),2):
            if(clean_text(faculty_names_and_positions[i])):
                faculty_info.append({
                j:{
                    "Faculty Name":clean_text(faculty_names_and_positions[i]),
                    "Faculty Designation": clean_text(faculty_names_and_positions[i+1])
                }
            })
                j+=1
        cm_data["Information about the faculty of Commerce and Management Department"] = faculty_info
        self.total_cm_dep_data = cm_data

    def closed(self, reason):
        with open('college_json_data/casa.json', 'r') as f:
            existing_data  = json.load(f)
            existing_data.append(self.total_cm_dep_data)
        with open('college_json_data/casa.json','w') as f:
            json.dump(existing_data, f, indent=4)

class CASA_math_department(scrapy.Spider):
    name = 'math_department'
    start_urls = ['https://casadoor.ihrd.ac.in/departments/mathematics']

    total_math_dep_data = {}

    def parse(self, response):
        math_data = {}
        math_desc = response.css('div.col-md-7.col-xs-12 p::text').get()
        print(math_desc)
        math_data["Information (description) about Mathematics Department "] = math_desc
        self.total_math_dep_data = math_data

    def closed(self, reason):
        with open('college_json_data/casa.json', 'r') as f:
            existing_data  = json.load(f)
            existing_data.append(self.total_math_dep_data)
        with open('college_json_data/casa.json','w') as f:
            json.dump(existing_data, f, indent=4)

class CASA_english_department(scrapy.Spider):
    name = 'english_department'
    start_urls = ['https://casadoor.ihrd.ac.in/departments/english']

    total_english_dep_data = {}

    def parse(self, response):
        english_data = {}
        english_desc = response.css('div.col-md-7.col-xs-12 p::text').get()
        print(english_desc)
        programmes = response.css('div.col-md-7.col-xs-12 ul li::text').getall()
        print(programmes)
        pro_data = {
                "UG Programme of English": clean_text(programmes[0])
            }
        english_data["Information (description) about English Department "] = english_desc
        english_data["Information about the various programme offered by English Department"] = pro_data
        faculty_names_and_positions = response.css('div.Name::text,div.Position::text').getall()
        print(faculty_names_and_positions)
        faculty_info = []
        j = 1
        for i in range(0,len(faculty_names_and_positions),2):
            if(clean_text(faculty_names_and_positions[i])):
                faculty_info.append({
                j:{
                    "Faculty Name":clean_text(faculty_names_and_positions[i]),
                    "Faculty Designation": clean_text(faculty_names_and_positions[i+1])
                }
            })
                j+=1
        english_data["Information about the faculty of English Department"] = faculty_info
        self.total_english_dep_data = english_data

    def closed(self, reason):
        with open('college_json_data/casa.json', 'r') as f:
            existing_data  = json.load(f)
            existing_data.append(self.total_english_dep_data)
        with open('college_json_data/casa.json','w') as f:
            json.dump(existing_data, f, indent=4)