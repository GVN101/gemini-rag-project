import scrapy
import json

import scrapy.spiderloader
# so basically we can add all our spider classes over here


# spider to get the details from the admission section
class AdmissionsSpider(scrapy.Spider):
    name = 'admissions'
    allowed_domains = ['ceconline.edu']
    start_urls = ['https://ceconline.edu/admission/btech_admissions/']

    total_admission_data = {}

    def parse(self, response):

        department_seat_capacity = {"department_wise_seat_capacity":{}} # main dictionary where all the admission data is 

        # get the pdf that contains the document to be submitted
        admission_document_list_link = response.css('div.elementor-widget-container p a::attr(href)').get()
        page_header = response.css('div.wpb_wrapper h2::text').get()
        page_admission_description = response.css('div.wpb_wrapper p::text').get()
        seat_capacity_table = response.css('tr td span::text').getall()

        
        for row in range(0,len(seat_capacity_table),2):
            department_seat_capacity['department_wise_seat_capacity'][seat_capacity_table[row]] = seat_capacity_table[row+1]
        
        btech_eligibility_criteria = response.css('ul li span::text').getall()

        # i just converted the list into a single string
        wrapped_text = ""
        for word in btech_eligibility_criteria:
            wrapped_text += word

        admission_data = {"admission_related_data":{}}
        admission_data['admission_related_data']['page_header'] = page_header
        admission_data['admission_related_data']['admission_description'] = page_admission_description
        admission_data['admission_related_data']['department_wise_seat_capacity'] = str(department_seat_capacity).replace('\u00a0','')
        admission_data['admission_related_data']['btech_eligibility_criteria'] = wrapped_text.replace('\u00a0','')
        admission_data['admission_related_data']['documents_to_be_submitted_during_admission_link'] = admission_document_list_link.replace(' ','%20')
        self.total_admission_data["All about admission data"] = admission_data

    def closed(self, response):

        with open('college_json_data/cec.json','r') as f:
            existing_data = json.load(f)
        existing_data.append(self.total_admission_data)

        with open('college_json_data/cec.json','w') as f:
            json.dump(existing_data,f,indent=4)
        

class DepartmentSpider(scrapy.Spider):
    name = 'admissions'
    allowed_domains = ['ceconline.edu']
    start_urls = ['https://ceconline.edu/departments'] 

    total_department_data = {"about_departments": []}  # Change to a list to hold multiple department data

    def parse(self, response):
        department_links = response.css('figure.wpb_wrapper.vc_figure a::attr(href)').getall()
        for department_link in department_links:
            yield response.follow(department_link, self.parse_department)  

    def parse_department(self, response):
        department_data = {}  # current department data

        department_title = response.css('h2.vc_custom_heading.vc_do_custom_heading::text').get()
        department_descriptions = response.css('div.wpb_text_column.wpb_content_element p::text').getall()
        wrapped_department_description = " ".join(department_descriptions) 

        department_data["department_title"] = department_title
        department_data["about_the_department"] = wrapped_department_description.strip()  # Clean up whitespace

        hod_details = {}
        hod_details["HOD image url"] = response.css('figure.wpb_wrapper.vc_figure div img::attr(src)').get()
        hod_details["HOD Name"] = response.css('div.stm-teacher-bio__text p span strong::text').get()
        hod_details["HOD Designation"] = response.css('div.stm-teacher-bio__text p strong span::text').get()
        hod_details["HOD Email"] = response.css('li.stm-contact-details__item.stm-contact-details__item_type_email a::text').get()

        department_data["About the HOD"] = hod_details

        total_faculty_list = []
        # for CS faculty
        faculty_list = response.css('td[width="319"] a::text,td[width="208"]::text,td[width="97"]::text').getall()

        if faculty_list:
            i = 2
            print(faculty_list[i])
            while(int(faculty_list[i])<30):
                faculty_individual_data = {}
                faculty_individual_data[faculty_list[i]] = {"faculty Name":faculty_list[i+1].replace('\u00a0',''), "faculty Designation": faculty_list[i+2]}
                total_faculty_list.append(faculty_individual_data)
                i+=3      
            department_data["Computer Department Faculty Data"] = total_faculty_list
        
        total_faculty_list = []

        # for EC faculty
        faculty_list = response.css('table[width="685"] td::text, table[width="685"] td a::text').getall()

        if faculty_list:
            i=0
            while(len(faculty_list)>=i+2):
                faculty_individual_data = {}
                faculty_individual_data[faculty_list[i]] = {"faculty Name":faculty_list[i+1], "faculty Designation": faculty_list[i+2].replace('\u00a0','')}
                # print(faculty_individual_data)
                total_faculty_list.append(faculty_individual_data)
                i+=3
            department_data["Electrical Department faculty Data"] = total_faculty_list
        
        total_faculty_list = []

        # for EEE faculty
        faculty_list = response.css('table.alt td a::text, table.alt td::text').getall()
        # print(faculty_list)
        faculty_list = faculty_list[1:40]
        print(faculty_list)

        if faculty_list and faculty_list[0][0] not in "4D":
            i=0
            while(len(faculty_list)>=i+2):
                faculty_individual_data = {}
                faculty_individual_data[faculty_list[i]] = {"faculty Name":faculty_list[i+1], "faculty Designation": faculty_list[i+2].replace('\u00a0','')}
                # print(faculty_individual_data)
                total_faculty_list.append(faculty_individual_data)
                i+=3
            department_data["Electrical Department faculty Data"] = total_faculty_list


        self.total_department_data["about_departments"].append(department_data)  # Append department data to the list

    def closed(self, reason):
        # This method is called when the spider is closed
        with open('college_json_data/cec.json', 'r') as f:
            existing_data  = json.load(f)
            existing_data.append(self.total_department_data)
        with open('college_json_data/cec.json','w') as f:
            json.dump(existing_data, f, indent=4)  # Write the collected data to a JSON file


class placementSpider(scrapy.Spider):
    name= "placementSpider"
    allowed_domains = ['ceconline.edu']
    start_urls = ['https://ceconline.edu/placement']

    total_placement_data = {"about placement cell": []}

    def parse(self, response):
        placement_cell_description = response.css('div.wpb_column.vc_column_container.vc_col-sm-12 p::text').getall()
        placement_cell_activities = response.css('div.wpb_column.vc_column_container.vc_col-sm-12 li::text').getall()
        print(placement_cell_description[:-2])
        print(placement_cell_activities[:-5])

        placement_cell_description_dict = {}
        placement_cell_activities_dict = {}

        placement_cell_description_dict["general description about TPC"] = ' '.join(placement_cell_description[:-2])
        placement_cell_activities_dict["placement cell activities"] = ' '.join(placement_cell_activities[:-5])

        self.total_placement_data['about placement cell'].append(placement_cell_description_dict)
        self.total_placement_data['about placement cell'].append(placement_cell_activities_dict)

    def closed(self, reason):
        # This method is called when the spider is closed
        with open('college_json_data/cec.json', 'r') as f:
            existing_data  = json.load(f)
            existing_data.append(self.total_placement_data)
        with open('college_json_data/cec.json','w') as f:
            json.dump(existing_data, f, indent=4)  # Write the collected data to a JSON file

class organisationSpider(scrapy.Spider):
    name= "organisationSpider"
    allowed_domains = ['ceconline.edu']
    start_urls = ['https://ceconline.edu/organizations']

    total_organisation_data = {"about organisations cell": []}

    def parse(self, response):
        organisation_links = response.css('div.wpb_wrapper h3 a::attr(href)').getall()
        organisation_links = [i for i in organisation_links if i] # removed some empty strings in the list 
        print(organisation_links)
        for organisation_link in organisation_links:
            yield response.follow(organisation_link, self.parse_organisation)  

    def parse_organisation(self, response):
        organisation_title = response.css('h1.vc_custom_heading.vc_do_custom_heading::text, h2.vc_custom_heading.vc_do_custom_heading::text, div.stm-title.stm-title_sep_bottom::text, h2.vc_custom_heading.vc_do_custom_heading a::text').get()
        organisation_website_link = response.css('div.wpb_wrapper p a::attr(href)').get(default = "No Link")
        print(organisation_title)
        if "Alumni" in organisation_title:
            organisation_title = "Alumni"

        organisation_description = response.css('div.wpb_text_column.wpb_content_element p::text, div.wpb_text_column.wpb_content_element p span::text').getall()
        print(organisation_description)

        # need to clean the data as it contained so many unwanted characters lmao!

        unwanted_chars = ["\u201c", "\u2019", "\u2013", "\u00a0", "\u201d", "\u2018", "\u201d"]
        cleaned_organisation_description = []

        for part in organisation_description:
            # Ensure part is a string
            if isinstance(part, str):
                for char in unwanted_chars:
                    part = part.replace(char, " ")
                if part.strip() and part.strip() is not '.':
                    cleaned_organisation_description.append(part.strip())  # Clean up spaces
            else:
                cleaned_organisation_description.append(part)

        cleaned_organisation_description = ' '.join(cleaned_organisation_description)
        
        bundled_data = []
        bundled_data.append(cleaned_organisation_description)
        bundled_data.append({})
        bundled_data[-1]["Offical website of this organisation"] = organisation_website_link
        
        organisation_data = {}
        organisation_data[organisation_title] = bundled_data

        self.total_organisation_data["about organisations cell"].append(organisation_data)

    def closed(self, reason):
        # This method is called when the spider is closed
        with open('college_json_data/cec.json', 'r') as f:
            existing_data  = json.load(f)
            existing_data.append(self.total_organisation_data)
        with open('college_json_data/cec.json','w') as f:
            json.dump(existing_data, f, indent=4)
