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
            data["Name"] = clean_text(cleaned_admin_staff_data[i])
            data["Designation"] = clean_text(cleaned_admin_staff_data[i+1])
            data["E-mail"] = clean_text(cleaned_admin_staff_data[i+2])
            data["Phone Number"] = clean_text(cleaned_admin_staff_data[i+3])
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
        for i in overview_data:
            i.replace('\r\n','')
        data["Overview of the college (CEK)"] = clean_text(overview_data[1] + ' ' + overview_data[2])
        data["Vision of CEK"] = clean_text(overview_data[3])
        data["Mission"] = clean_text(overview_data[4])

        data["Programmes Offered"] = {
            "Btech": [clean_text(overview_data[5]), clean_text(overview_data[6]), clean_text(overview_data[7]), clean_text(overview_data[8])],
            "Mtech": clean_text(overview_data[10])
        }
        data["Memorandum of Understanding"] = clean_text(overview_data[11].replace('\r',''))
        data["Student Professional Bodies"] = clean_text(overview_data[12])
        data["Data about College Library"] = clean_text(overview_data[13])
        data["Training and Placement Cell of CEK"] = clean_text(overview_data[14])
        data["Alumni details about CEK"] = clean_text(overview_data[15])
        data["Parent-Teacher Association (PTA) of CEK"] = clean_text(overview_data[16])
        data["College Hostel"] = clean_text(overview_data[17])
        data["Canteen"] = clean_text(overview_data[18])
        data["ATM Counter"] =  clean_text(overview_data[19])
        data["Sports and Cultural Festivals"] = clean_text(overview_data[20])
        self.total_overview_data = {
            "About the Overview of the college":data
        }

    def closed(self, response):
        with open('college_json_data/cek.json', 'r') as f:
            data = json.load(f)
            data.append(self.total_overview_data)
        with open('college_json_data/cek.json', 'w') as f:
            json.dump(data,f,indent=4)

class CEK_infrastructure(scrapy.Spider):
    name = 'infrastructure'
    start_urls = ['https://www.ceknpy.ac.in/infrastructure']

    total_infrastructure_data = {}

    def parse(self, response):
        data = {}
        infra_data = response.css('div.sec-title div.desc p::text').getall()
        for i in infra_data:
            i.replace('\r\n','')

        data["Data about building and Labs"] = clean_text(infra_data[0])
        data["Information about the roads to the college (CEK)"] = infra_data[1]
        data["About the placement activities"] = infra_data[2]
        data["PTA (parent teacher association) at CEK"] = infra_data[3]
        data["Transportation details at CEK"] = infra_data[4]
        data["Water supply at CEK"] = infra_data[5]
        self.total_infrastructure_data["About the Infrastructure at CEK"] = data

    def closed(self, response):
        with open('college_json_data/cek.json', 'r') as f:
            data = json.load(f)
            data.append(self.total_infrastructure_data)
        with open('college_json_data/cek.json', 'w') as f:
            json.dump(data,f,indent=4)
        
class CEK_anti_ragging_squad(scrapy.Spider):
    name = 'Anti_Ragging_squad'
    # allowed_domains = ['cea.ac.in']
    start_urls = ['https://www.ceknpy.ac.in/antiragging']

    total_Anti_Ragging_Squad = {}

    def parse(self, response):
        data = []
        ars_data = response.css('table tr td p span::text').getall()
        print(ars_data[13:])
        squad_list = ars_data[13:]
        print(squad_list)
        i = 0
        while i<len(squad_list):
            print(ars_data[i])
            data.append(
                {
                    "Name": squad_list[i],
                    "Phone Number": squad_list[i+1]
                }
            )
            i+=2
        self.total_Anti_Ragging_Squad["Data about the Anti Ragging Squad"] ={
            "List of Executive Commitee Members in Anti Ragging Squad": data
        } 
    
    def closed(self, response):
        with open('college_json_data/cek.json', 'r') as f:
            data = json.load(f)
            data.append(self.total_Anti_Ragging_Squad)
        with open('college_json_data/cek.json', 'w') as f:
            json.dump(data,f,indent=4)

class CEK_Departmentdata(scrapy.Spider):
    name = 'department'
    start_urls = ['https://www.ceknpy.ac.in/departments/'] 

    total_department_data = {
        "About the departments of CEK":[]
    }  # Change to a list to hold multiple department data

    def parse(self, response):
        department_links = response.css('div.content-part span a::attr(href)').getall()
        print(department_links)
        for department_link in department_links:
            yield response.follow(department_link, self.parse_department)  

    def parse_department(self, response):
        data = {}
        course_overview_data = response.css('div.course-overview div p::text, div.course-overview div h3::text').getall()
        department_title = response.css('div.breadcrumbs-text ul li::text').getall()
        department_title = department_title[-1]
        
        course_overview_data_cleaned = [clean_text(i) for i in course_overview_data if clean_text(i)]

        # for CS department 
        if(department_title == 'Department of Computer Science and Engineering'):
            cs_dep_data = {}
            temp = [course_overview_data_cleaned[i] for i in range(5)]
            cs_dep_data["About the Computer Science Department"] = ' '.join(temp)

            seat_table_data = {
                "BTech Computer Science": "120 Seats",
                "BTech Artificial Intelligence and Data Science": "60 Seats"
            }
            cs_dep_data["Information about the seats in CS departments"] = seat_table_data

            programme_outcomes = [course_overview_data_cleaned[i] for i in range(5,35)]
            cs_dep_data["Programme Outcome information of CS department"] = programme_outcomes
            hod_data = {}
            hod_data["Name"] = response.css("div.names::text").get()

            # Getting the data of CS HOD
            hod_qualifications = response.css('div#prod-curriculum div.right_con::text').getall()
            hod_qualifications = [clean_text(i) for i in hod_qualifications]
            hod_data["Qualifications of HOD"] = {
                "Qualificaion": hod_qualifications[0],
                "Department": hod_qualifications[1],
                "Years of Experience": hod_qualifications[2]
            }
            hod_data["Contact Information of HOD"] = {
                "Phone Number": hod_qualifications[3],
                "Email": hod_qualifications[4]
            }
            hod_publications = response.css('div#prod-curriculum div.inner-box div.box p::text').getall()
            hod_publications = [clean_text(i) for i in hod_publications[13:]]
            hod_data["Publications of HOD"] = hod_publications
            cs_dep_data["Information on Head of Department of Computer Science"] = hod_data

            # Getting the faculty list of CEK Computer Science
            faculty_cards = response.css('div.card.accordion.block')
            faculty_info = []
            for card in faculty_cards:
                name = card.css("div.names::text").get()
                phone_number = card.css("div.right_con::text").re_first(r"\d{10}")
                email = card.css("div.right_con::text").re_first(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9._%+-]+\.[a-zA-Z]{2,}")
                designation = card.css("div.col-lg-8 div.designation::text").get()
                if name:
                    faculty_info.append(
                        {
                            "Name": name,
                            "Designation": clean_text(designation),
                            "Phone Number": phone_number,
                            "Email": email
                        }
                    )
            cs_dep_data["Computer Science Faculty Information"] = faculty_info
            course_overview_data_cleaned ={
                "Department of Applied Science": cs_dep_data
            }
            self.total_department_data["About the departments of CEK"].append(course_overview_data_cleaned)
        
        # Getting the data of Electronice Department 
        if(department_title == "Department of Electronics and Communication"):
            ec_dep_data = {}
            ec_dep_data["About the Electronics Department of CEK"] = ''.join([course_overview_data_cleaned[i] for i in range(5)])

            hod_data = {}
            hod_qualifications = response.css('div#prod-curriculum div.right_con::text').getall()
            hod_qualifications = [clean_text(i) for i in hod_qualifications]
            print(hod_qualifications)
            if hod_qualifications[0]:
                hod_data["Qualifications of HOD"] = {
                    "Qualificaion": hod_qualifications[0],
                    "Department": hod_qualifications[1],
                    "Years of Experience": hod_qualifications[2]
                }
                hod_data["Contact Information of HOD"] = {
                    "Phone Number": hod_qualifications[3],
                    "Email": hod_qualifications[4]
                }
                hod_publications = response.css('div#prod-curriculum div.inner-box div.box p::text').getall()
                hod_publications = [clean_text(i) for i in hod_publications[13:]]
                hod_data["Publications of HOD"] = hod_publications
                ec_dep_data["Information on Head of Department of Electronics Department"] = hod_data
            else:
                hod_data = "None Specified"
                ec_dep_data["Information on Head of Department of Electronics Department"] = hod_data

            # Getting the faculty information of Electronics department of CEK
            faculty_cards = response.css('div.card.accordion.block')
            faculty_info = []
            for card in faculty_cards:
                name = card.css("div.names::text").get()
                phone_number = card.css("div.right_con::text").re_first(r"\d{10}")
                email = card.css("div.right_con::text").re_first(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9._%+-]+\.[a-zA-Z]{2,}")
                designation = card.css("div.col-lg-8 div.designation::text").get()
                if name:
                    faculty_info.append(
                        {
                            "Name": name,
                            "Designation": clean_text(designation),
                            "Phone Number": phone_number,
                            "Email": email
                        }
                    )
            ec_dep_data["Electronics Faculty Information"] = faculty_info
            course_overview_data_cleaned ={
                "Department of Applied Science": ec_dep_data
            }
            self.total_department_data["About the departments of CEK"].append(course_overview_data_cleaned)

        if(department_title == "Department of Mechanical Engineering"):
            mech_dep_data = {}
            mech_dep_data["About the Mechanical Engineering Department of CEK"] = ''.join([course_overview_data_cleaned[i] for i in range(4)])

            # Getting the information of HOD of mechanical Engineering
            hod_data = {}
            hod_qualifications = response.css('div#prod-curriculum div.right_con::text').getall()
            hod_qualifications = [clean_text(i) for i in hod_qualifications]
            print(hod_qualifications)
            if hod_qualifications[0]:
                hod_data["Qualifications of HOD"] = {
                    "Qualificaion": hod_qualifications[0],
                    "Department": hod_qualifications[1],
                    "Years of Experience": hod_qualifications[2]
                }
                hod_data["Contact Information of HOD"] = {
                    "Phone Number": hod_qualifications[3],
                    "Email": hod_qualifications[4]
                }
                hod_publications = response.css('div#prod-curriculum div.inner-box div.box p::text').getall()
                hod_publications = [clean_text(i) for i in hod_publications[13:]]
                hod_data["Publications of HOD"] = hod_publications
                mech_dep_data["Information on Head of Department of Mechanical Engineering Department"] = hod_data
            else:
                hod_data = "None Specified"
                mech_dep_data["Information on Head of Department of Mechanical Engineering Department"] = hod_data

            # Getting the faculty information of Mechanical department of CEK
            faculty_cards = response.css('div.card.accordion.block')
            faculty_info = []
            for card in faculty_cards:
                name = card.css("div.names::text").get()
                phone_number = card.css("div.right_con::text").re_first(r"\d{10}")
                email = card.css("div.right_con::text").re_first(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9._%+-]+\.[a-zA-Z]{2,}")
                designation = card.css("div.col-lg-8 div.designation::text").get()
                if name:
                    faculty_info.append(
                        {
                            "Name": name,
                            "Designation": clean_text(designation),
                            "Phone Number": phone_number,
                            "Email": email
                        }
                    )
            mech_dep_data["Mechanical Department Faculty Information"] = faculty_info
            course_overview_data_cleaned ={
                "Department of Applied Science": mech_dep_data
            }
            self.total_department_data["About the departments of CEK"].append(course_overview_data_cleaned)
        
        # Getting the information of Electrical Department of CEK
        if(department_title == "Department of Electrical Engineering"):
            eee_dep_data = {}
            eee_dep_data["About the Electrical Engineering Department of CEK"] = ''.join([course_overview_data_cleaned[i] for i in range(4)])

            # Getting the information on HOD of Electrical Engineering Department
            hod_data = {}
            hod_qualifications = response.css('div#prod-curriculum div.right_con::text').getall()
            hod_qualifications = [clean_text(i) for i in hod_qualifications]
            if hod_qualifications[0]:
                hod_data["Qualifications of HOD"] = {
                    "Qualificaion": hod_qualifications[0],
                    "Department": hod_qualifications[1],
                    "Years of Experience": hod_qualifications[2]
                }
                hod_data["Contact Information of HOD"] = {
                    "Phone Number": hod_qualifications[3],
                    "Email": hod_qualifications[4]
                }
                hod_publications = response.css('div#prod-curriculum div.inner-box div.box p::text').getall()
                hod_publications = [clean_text(i) for i in hod_publications[13:]]
                hod_data["Publications of HOD"] = hod_publications
                eee_dep_data["Information on Head of Department of Electrical Engineering Department"] = hod_data
            else:
                hod_data = "None Specified"
                eee_dep_data["Information on Head of Department of Electrical Engineering Department"] = hod_data

            # Getting the faculty information of Mechanical department of CEK
            faculty_cards = response.css('div.card.accordion.block')
            faculty_info = []
            for card in faculty_cards:
                name = card.css("div.names::text").get()
                phone_number = card.css("div.right_con::text").re_first(r"\d{10}")
                email = card.css("div.right_con::text").re_first(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9._%+-]+\.[a-zA-Z]{2,}")
                designation = card.css("div.col-lg-8 div.designation::text").get()
                if name:
                    faculty_info.append(
                        {
                            "Name": name,
                            "Designation": clean_text(designation),
                            "Phone Number": phone_number,
                            "Email": email
                        }
                    )
            eee_dep_data["ELectrical Department Faculty Information"] = faculty_info
            course_overview_data_cleaned ={
                "Department of Applied Science": eee_dep_data
            }
            self.total_department_data["About the departments of CEK"].append(course_overview_data_cleaned)

        if(department_title == "Department of Applied Sciences"):
            as_dep_data = {}
            as_dep_data["About the Applied Science Department of CEK"] = course_overview_data_cleaned[0]

            # Getting the information on HOD of Applied Science Department
            hod_data = {}
            hod_qualifications = response.css('div#prod-curriculum div.right_con::text').getall()
            hod_qualifications = [clean_text(i) for i in hod_qualifications]
            if hod_qualifications[0]:
                hod_data["Qualifications of HOD"] = {
                    "Qualificaion": hod_qualifications[0],
                    "Department": hod_qualifications[1],
                    "Years of Experience": hod_qualifications[2]
                }
                hod_data["Contact Information of HOD"] = {
                    "Phone Number": hod_qualifications[3],
                    "Email": hod_qualifications[4]
                }
                hod_publications = response.css('div#prod-curriculum div.inner-box div.box p::text').getall()
                hod_publications = [clean_text(i) for i in hod_publications[13:]]
                hod_data["Publications of HOD"] = hod_publications
                as_dep_data["Information on Head of Department of Applied Science Department"] = hod_data
            else:
                hod_data = "None Specified"
                as_dep_data["Information on Head of Department of Applied Science Department"] = hod_data

            # Getting the faculty information of Applied Science department of CEK
            faculty_cards = response.css('div.card.accordion.block')
            faculty_info = []
            for card in faculty_cards:
                name = card.css("div.names::text").get()
                phone_number = card.css("div.right_con::text").re_first(r"\d{10}")
                email = card.css("div.right_con::text").re_first(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9._%+-]+\.[a-zA-Z]{2,}")
                designation = card.css("div.col-lg-8 div.designation::text").get()
                if name:
                    faculty_info.append(
                        {
                            "Name": name,
                            "Designation": clean_text(designation),
                            "Phone Number": phone_number,
                            "Email": email
                        }
                    )
            as_dep_data["Applied Science Faculty Information"] = faculty_info
            course_overview_data_cleaned ={
                "Department of Applied Science": as_dep_data
            } 
            self.total_department_data["About the departments of CEK"].append(course_overview_data_cleaned)
        
    
    def closed(self, response):
        with open('college_json_data/cek.json', 'r') as f:
            data = json.load(f)
            data.append(self.total_department_data)
        with open('college_json_data/cek.json', 'w') as f:
            json.dump(data,f,indent=4)

class CEK_contact(scrapy.Spider):
    name = 'contact'
    # allowed_domains = ['cea.ac.in']
    start_urls = ['https://www.ceknpy.ac.in/contact-us']

    total_contact_data = {}

    def parse(self, response):
        data = []
        contact_ = response.css('div.img-part.js-tilt p::text').getall()
        # print(contact_)
        transportation = {
            "Way to reach College of Engineering Karungappally":{
                contact_[0]:contact_[1],
                contact_[2]:contact_[3],
                contact_[4]:contact_[5]
            }
        }
        data.append(transportation)
        phone_number = response.css('div.address-text span.des a::text').getall()
        print(phone_number)
        data.append({
            "Contact number of CEK":phone_number
        })
        self.total_contact_data["Contact information of CEK"] = data
    
    def closed(self, response):
        with open('college_json_data/cek.json', 'r') as f:
            data = json.load(f)
            data.append(self.total_contact_data)
        with open('college_json_data/cek.json', 'w') as f:
            json.dump(data,f,indent=4)

class CEK_placement(scrapy.Spider):
    name = 'placement_cell'
    start_urls = ['https://www.ceknpy.ac.in/campus']

    total_placement_data = {}

    def parse(self,response):
        data = []
        desc = response.css('div.sec-title div.desc p::text').get()
        data.append({
            "About the Training and Placement Cell of CEK": desc
        })
        placement_result = response.css("table tbody tr td::text").getall()

        for i in placement_result:
            print(i)
        count = 0
        i = 3
        placement_ls = []
        while count < 60:
            placement_ls.append({
                "SI":placement_result[i],
                "Name": placement_result[i+1],
                "Company Placed": placement_result[i+2]
            })
            count += 1
            i+=3
        data.append({
            "List of Student who got placed":placement_ls
        })
        self.total_placement_data = data
    
    def closed(self, response):
        with open('college_json_data/cek.json', 'r') as f:
            data = json.load(f)
            data.append(self.total_placement_data)
        with open('college_json_data/cek.json', 'w') as f:
            json.dump(data,f,indent=4)

class CEK_library(scrapy.Spider):
    name = 'Library'
    start_urls = ['https://www.ceknpy.ac.in/library']

    total_library_data = {}

    def parse(self,response):
        data = []
        desc = response.css('div.sec-title div.desc h5::text').getall()

        data.append({
            "About the Library": desc[0],
            "Library Timing": desc[2],
            "Library Collection": desc[4],
            "Journals and Magazines at the Library": desc[6],
            "Membership of Library": desc[10]
        })
        self.total_library_data = {
            "About the Library of CEK": data
        }

    def closed(self, response):
        with open('college_json_data/cek.json', 'r') as f:
            data = json.load(f)
            data.append(self.total_library_data)
        with open('college_json_data/cek.json', 'w') as f:
            json.dump(data,f,indent=4)


