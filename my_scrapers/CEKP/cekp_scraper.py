import scrapy
import json
import re

import scrapy.crawler

def clean_text(item):
    item = re.sub(r'\\u[0-9a-fA-F]{4}', '', item)
    item = re.sub(r'[\u2013\u2019\u2022\u201a\u201c\u201d\u00b1\u00a0]', '-', item)
    item = re.sub(r'\s+', ' ', item).strip()
    item = re.sub(r'<br>','',item)
    item = re.sub(r'<strong>','',item)
    item = re.sub(r'\u00a0','',item)
    item = re.sub(r'-','',item).strip()
    item = re.sub(r'[^\x00-\x7F]+', '', item)
    return item

class CEKP_principal(scrapy.Spider):
    name = 'principal'
    start_urls = ['https://www.cek.ac.in/index.php/administration/principal']

    total_principal_data = {}

    def parse(self, response):
        principal_data = response.css('p.MsoNormal span::text, p.MsoNormal span::text').getall()
        cleaned_principal_data = [clean_text(i) for i in principal_data]
        data = {}
        data['Principal Name'] = cleaned_principal_data[0]
        data['principal Desgination'] = cleaned_principal_data[1]
        data["phone or contact number of the principal"] = cleaned_principal_data[2]
        data['fax Number of the principal'] = cleaned_principal_data[3]
        data['Mobile Number of the principal'] = cleaned_principal_data[5]
        data['Email ID of the principal'] = "principal@cek.ac.in"
        self.total_principal_data['information about the principal'] = data

    def closed(self, response):
        with open('college_json_data/cekp.json', 'r') as f:
            data = json.load(f)
            data.append(self.total_principal_data)
        with open('college_json_data/cekp.json', 'w') as f:
            json.dump(data,f,indent=4)

class CEKP_admission_mtech(scrapy.Spider):
    name = 'admission'
    start_urls = ['https://www.cek.ac.in/index.php/academics/admission/m-tech']

    total_admission_data = {
        "Basic data on the courses or programmes offered": "College of Engineering Kalloopaara offers two programmes or courses for students: Btech and Mtech"
    }
    

    def parse(self, response):
        # Extract course information
        course_text = response.css('title::text').get()
        
        data = response.css('p.MsoNormal b span::text').getall()
        desc = response.css('p.MsoNormal span::text').getall()
        clean_data = [clean_text(i) for i in data]
        clean_desc = [clean_text(i) for i in desc]

        desc_new = ' '.join(clean_desc)

        course_name = clean_data[1]
        course_seats = clean_data[2] + 'seats'
        desciption = desc_new
        
        print(clean_data)

        # Extract important links
        dte_link = response.xpath('//a[contains(@href, "dtekerala.gov.in")]/@href').get()
        portal_link = response.xpath('//a[contains(@href, "dtekerala.co.in/site/login")]/@href').get()

        # Extract description paragraphs
        description = []
        for para in response.xpath('//p[@class="MsoNormal" and contains(., "eligible for admission")]/text()').getall():
            description.append(para.strip())

        self.total_admission_data['Information about the Mtech Programme in Kalloopaara'] = {
            "Course Name offered in Mtech": course_name,
            'Number of seats in Mtech course': course_seats,
            'Description of the Mtech course': desciption,
            'dte_website': dte_link,
            'admission_portal for Mtech Course': portal_link,
            'description about Mtech Course or Programme': ' '.join(description),
            'university under': "APJ Abdul Kalam Technological University (KTU)",
            'admission_process of Mtech Course or progammes': "Through Directorate of Technical Education Kerala",
        }

    def closed(self, response):
        with open('college_json_data/cekp.json', 'r') as f:
            data = json.load(f)
            data.append(self.total_admission_data)
        with open('college_json_data/cekp.json', 'w') as f:
            json.dump(data,f,indent=4)


class CEKP_admission_btech(scrapy.Spider):
    name = 'btech_admission'
    start_urls = ['https://www.cek.ac.in/index.php/academics/admission/b-tech']
    
    total_btech_admission_data = {}

    def parse(self, response):
        # Extract the course information
        courses = response.css('ul li span::text').getall()
        courses = [course.strip() for course in courses]
        courses = [clean_text(courses[i]) for i in range(6,len(courses))]

        print(courses)

        other_data = response.css('p.MsoNormal span::text').getall()
        other_data = [clean_text(other_data[i]) for i in range(0, len(other_data))]
        other_data = [i for i in other_data if i]

        total_seat_intake = other_data[4]

        # Extract the seat information
        seat_info = [other_data[i] for i in range(5,9)]
        seat_info = ' and '.join(seat_info)
        print(seat_info, "seat")

        # Extract the eligibility information
        eligibility_info = other_data[16] + other_data[19]

        # Yield the extracted information
        self.total_btech_admission_data = {
            'Courses or Programmes Offered in Btech by kalloopaara ': courses,
            'Total Seat intake in Btech Information': total_seat_intake,
            'Seat in Btech information': seat_info,
            'Btech Critiriea for Eligibility and also Age critiriea': eligibility_info,
        }
    
    def closed(self, response):
        with open('college_json_data/cekp.json', 'r') as f:
            data = json.load(f)
            data.append(self.total_btech_admission_data)
        with open('college_json_data/cekp.json', 'w') as f:
            json.dump(data,f,indent=4)

class CEKP_department_ec(scrapy.Spider):
    name = "department_ec"
    start_urls = [
        'https://cek.ac.in/index.php/departments/electronics-and-communication-engineering',  # Replace with the actual URL
    ]

    total_ec_data = {}

    def parse(self, response):
        # Extract the department head information
        hod_and_faculty_data = response.css('p.MsoNormal span::text, p.MsoNormal b span::text').getall()
        desc = response.css('p span::text').getall()
        print(desc)
        hod_and_faculty_data = [clean_text(i) for i in hod_and_faculty_data]
        print(hod_and_faculty_data)
        hod_data = {
            "Name of Hod of EC department": hod_and_faculty_data[0],
            "Designation of HOD of EC Department": hod_and_faculty_data[1],
            "Phone Number and Email of Hod of EC Department": hod_and_faculty_data[2] + "and Email is philipcherian@cek.ac.in and hodece@cek.ac.in"
        }
        print(hod_and_faculty_data[12])
        count = 1
        faculty_details = []
        for i in range(12, len(hod_and_faculty_data),3):
            faculty_details.append(f"Name: {hod_and_faculty_data[i+1]} and his/her designation is {hod_and_faculty_data[i+2]}")
            count += 1
        self.total_ec_data["Data about the Electronics Department"] = {
            "Data about the HOD of EC": hod_data,
            "Data about the Faculty of EC": faculty_details,
            "Description of EC Department": desc[-6]
        }

    def closed(self, response):
        with open('college_json_data/cekp.json', 'r') as f:
            data = json.load(f)
            data.append(self.total_ec_data)
        with open('college_json_data/cekp.json', 'w') as f:
            json.dump(data,f,indent=4)

class CEKP_department_cs(scrapy.Spider):
    name = "department_cs"
    start_urls = [
        'https://cek.ac.in/index.php/departments/computer-science-and-engineering',  # Replace with the actual URL
    ]

    total_cs_data = {}

    def parse(self, response):
        # Extract the department head information
        data = response.css('p.MsoNormal span::text, p.MsoNormal b span::text').getall()
        desc = ' '.join([data[i] for i in range(0, 5)])
        print(desc)
        data = [clean_text(i) for i in data]
        print(data)
        hod_data = {
            "Name of Hod of CS department": data[6],
            "Designation of HOD of CS Department": data[7],
            "Phone Number and Email of Hod of CS Department": data[8] + "and Email is hodcse@cek.ac.in"
        }
        # print(hod_and_faculty_data[12])
        # count = 1
        # faculty_details = []
        # for i in range(12, len(hod_and_faculty_data),3):
        #     faculty_details.append(f"Name: {hod_and_faculty_data[i+1]} and his/her designation is {hod_and_faculty_data[i+2]}")
        #     count += 1
        # self.total_cs_data["Data about the Computer Science Department"] = {
        #     "Data about the HOD of CS": hod_data,
        #     "Data about the Faculty of CS": faculty_details,
        #     "Description of CS Department": desc[-6]
        # }
        self.total_cs_data  = data

    def closed(self, response):
        with open('college_json_data/cekp.json', 'r') as f:
            data = json.load(f)
            data.append(self.total_cs_data)
        with open('college_json_data/cekp.json', 'w') as f:
            json.dump(data,f,indent=4)
