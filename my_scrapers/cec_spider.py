import scrapy
import json
# so basically we can add all our spider classes over here


# spider to get the details from the admission section
# class AdmissionsSpider(scrapy.Spider):
#     name = 'admissions'
#     allowed_domains = ['ceconline.edu']
#     start_urls = ['https://ceconline.edu/admission/btech_admissions/']

#     def parse(self, response):

#         department_seat_capacity = {"department_wise_seat_capacity":{}} # main dictionary where all the admission data is 

#         # get the pdf that contains the document to be submitted
#         admission_document_list_link = response.css('div.elementor-widget-container p a::attr(href)').get()
#         page_header = response.css('div.wpb_wrapper h2::text').get()
#         page_admission_description = response.css('div.wpb_wrapper p::text').get()
#         seat_capacity_table = response.css('tr td span::text').getall()

        
#         for row in range(0,len(seat_capacity_table),2):
#             department_seat_capacity['department_wise_seat_capacity'][seat_capacity_table[row]] = seat_capacity_table[row+1]
        
#         btech_eligibility_criteria = response.css('ul li span::text').getall()

#         # i just converted the list into a single string
#         wrapped_text = ""
#         for word in btech_eligibility_criteria:
#             wrapped_text += word

#         admission_data = {"admission_related_data":{}}
#         admission_data['admission_related_data']['page_header'] = page_header
#         admission_data['admission_related_data']['admission_description'] = page_admission_description
#         admission_data['admission_related_data']['department_wise_seat_capacity'] = str(department_seat_capacity).replace('\u00a0','')
#         admission_data['admission_related_data']['btech_eligibility_criteria'] = wrapped_text.replace('\u00a0','')
#         admission_data['admission_related_data']['documents_to_be_submitted_during_admission_link'] = admission_document_list_link.replace(' ','%20')

#         print(admission_data)
#         print(type(admission_data))
#         with open('output.json','w') as f:
#             json.dump(admission_data,f)

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

        total_faculy_list = []
        # for CS faculty
        faculty_list = response.css('td[width="319"] a::text,td[width="208"]::text,td[width="97"]::text').getall()
        print(faculty_list)


        if faculty_list:
            i = 2
            print(faculty_list[i])
            while(int(faculty_list[i])<30):
                faculty_individual_data = {}
                faculty_individual_data[faculty_list[i]] = {"faculty Name":faculty_list[i+1].replace('\u00a0',''), "faculty Designation": faculty_list[i+2]}
                print(faculty_individual_data)
                total_faculy_list.append(faculty_individual_data)
                i+=3      
        department_data["Department Faculty Data"] = total_faculy_list

        print("\n\n\n\n\n\n\n\n\n\n\n")

        self.total_department_data["about_departments"].append(department_data)  # Append department data to the list

    def closed(self, reason):
        # This method is called when the spider is closed
        with open('output.json', 'a') as f:
            json.dump(self.total_department_data, f, indent=4)  # Write the collected data to a JSON file

if __name__ == "__main__":
    from scrapy.crawler import CrawlerProcess
    from scrapy.utils.project import get_project_settings

    process = CrawlerProcess(get_project_settings())
    process.crawl(DepartmentSpider) 
    process.start()