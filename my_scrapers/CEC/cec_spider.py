import scrapy
import json
from urllib.parse import urljoin
import scrapy.spiderloader

def clear_file():
    with open('college_json_data/cec.json','w') as f:
        f.write('[]')
    with open('college_json_data/cek.json','w') as f:
        f.write('[]')
    with open('college_json_data/aec.json','w') as f:
        f.write('[]')

# spider to get the details from the admission section
class CEC_AdmissionsSpider(scrapy.Spider):
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

class CEC_DepartmentSpider(scrapy.Spider):
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

class CEC_placementSpider(scrapy.Spider):
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

class CEC_organisationSpider(scrapy.Spider):
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

class CEC_principal_spider(scrapy.Spider):
    name = 'principal_spider'
    allowed_domains = ['ceconline.edu']
    start_urls = ['https://ceconline.edu/administrators/hari/']

    total_principal_details = ''

    def parse(self, response):
        principal_name = response.css('.stm-title.stm-title_sep_bottom::text').extract_first().strip()
        qualification_titles = response.css('.wpb_wrapper ul span::text').getall()
        qualification_details = [q.strip() for q in response.css('.wpb_wrapper ul li::text').getall()]
        qualifications = dict(zip(qualification_titles, qualification_details))
        principal_contact = {}
        contact_details = response.css('.stm-contact-details__items li')

        for detail in contact_details:

            text = detail.css('::text').get().strip()
            key = detail.css('::attr(class)').get().split('_')[-1]
            if text:
                principal_contact[key.replace('-', '')] = text
        positions = response.css('.vc_tta-panel-body ol li::text').getall()
        fields_of_expertise = response.css('.vc_tta-panel-body:contains("LabVIEW") .wpb_wrapper ul li::text').getall()
        industry_interactions = response.css('.vc_tta-panel-body:contains("Minimization of atomic norm in vibration signals") .wpb_wrapper ul li em::text').getall()
        research_activities = response.css('.vc_tta-panel-body:contains("Incorporated a company Rand Walk Research") .wpb_wrapper ul li p::text').getall()
        books = response.css('.vc_tta-panel-body:contains("Electronics Laboratory Handbook with Simulations using Quite Universal Circuit Simulator (Qucs), Authors Press,New Delhi,ISBN-978-93-5529-048-9") .wpb_wrapper ol li::text').getall()

        self.total_principal_details = {
            'principal_name': principal_name,
            'principal\'s-academic-qualifications': qualifications,
            'principal\'s-contact': principal_contact,
            'principal\'s-positions': positions,
            'principal\'s-fields-of-expertise': fields_of_expertise,
            'principal\'s-research': research_activities,
            'principal\'s-industry-interactions': industry_interactions,
            'principal\'s-books-published': books,
        }

    def closed(self, reason):
        # This method is called when the spider is closed
        with open('college_json_data/cec.json', 'r') as f:
            existing_data  = json.load(f)
            existing_data.append(self.total_principal_details)
        with open('college_json_data/cec.json','w') as f:
            json.dump(existing_data, f, indent=4)

class CEC_PTASpider(scrapy.Spider):
    name = "pta_spider"
    start_urls = ["https://ceconline.edu/about/committees/pta/"]

    total_pta_data = ''

    def parse(self, response):
        pta_section = response.xpath('//div[contains(@class, "wpb_wrapper")]/div[contains(@class, "pta-section")]')

        if pta_section:
            pta_details = {}
            tables = pta_section.xpath(".//table")

            for table_index, table in enumerate(tables):
                members = []
                rows = table.xpath(".//tr[position()>1]")  # Skip header row
                for row in rows:
                    cols = row.xpath(".//td")
                    if cols:  # Check if the row has any columns at all
                        member = {}
                        try:
                            name_parts = cols[1].xpath(".//text()").getall()
                            member["name"] = "".join(name_parts).strip()
                            member["phone"] = cols[2].xpath(".//text()").get("").strip()
                            member["student_name"] = cols[3].xpath(".//text()").get("").strip() if len(cols) > 3 else "" #handle missing student name
                            members.append(member)
                        except IndexError as e:
                            self.log(f"IndexError in table {table_index + 1}: {e}. Row content: {row.get()}") #log the row content
                            continue #skip to next row
                    else:
                        self.log(f"Empty row found in table {table_index + 1}. Skipping.")

                if members: #only add if there are any members
                    if table_index == 0:
                        pta_details["executive_members"] = members
                    elif table_index == 1:
                        pta_details["faculty_representatives"] = members
                    elif table_index == 2:
                        pta_details["special_invitees"] = members

            if pta_details:
                self.total_pta_data = {"pta_details": pta_details}
            else:
                self.log("No PTA data found in tables.")
        else:
            self.log("PTA section not found. Check the XPath.")

    def closed(self, reason):
        # This method is called when the spider is closed
        with open('college_json_data/cec.json', 'r') as f:
            existing_data  = json.load(f)
            existing_data.append(self.total_pta_data)
        with open('college_json_data/cec.json','w') as f:
            json.dump(existing_data, f, indent=4)

class CEC_NoticeSpider(scrapy.Spider):
    name = 'notice_spider'
    start_urls = ['https://ceconline.edu/notifications-2/']

    total_notice_data = []
    
    def parse(self, response):
        notice_identifiers = {
            'semester_registration_revised': 'Revised notice for  Semester Registration',
            'semester_registration': 'Semester Registration for B.Tech  and MCA',
            'fees_payment': 'Fees Payment for Semester registration',
            'induction_programme': 'Student Induction Programme 2024',
            'btech_documents': 'B.Tech Documents To Be Submitted',
            'ladies_hostel': 'Ladies Hostel List',
            'answer_book': 'Purchase Of Main Answer Book'
        }
        
        for notice_id, notice_text in notice_identifiers.items():
            notice_element = response.xpath(
                f"//div[contains(@class, 'elementor-widget-container')]"
                f"//h2[contains(@class, 'elementor-heading-title')]"
                f"//a[contains(., '{notice_text}')]"
            )
            
            if notice_element:
                link = notice_element.attrib.get('href', '')
                text = notice_element.css('u::text').get('').strip()
                
                if not text:
                    text = notice_element.get().strip()
                
                if link.startswith('/'):
                    link = urljoin(response.url, link)
                    
                doc_type = self.get_document_type(link)
                self.total_notice_data.append({
                    'data_type': 'notice',  
                    'id': notice_id,
                    'title': text,
                    'url': link,
                    'type': doc_type,
                    'matched_text': notice_text
                })

                print(self.total_notice_data)
                
                if doc_type == 'pdf':
                    yield scrapy.Request(
                        url=link,
                        callback=self.save_pdf,
                        meta={
                            'title': text,
                            'notice_id': notice_id
                        },
                        errback=self.handle_error
                    )
    def get_document_type(self, url):
        if url.endswith('.pdf'):
            return 'pdf'
        elif 'onlinesbi.sbi' in url:
            return 'payment_portal'
        elif url.startswith('http') or url.startswith('https'):
            return 'external_link'
        return 'other'

    def closed(self, reason):
        # This method is called when the spider is closed
        with open('college_json_data/cec.json', 'r') as f:
            existing_data  = json.load(f)
            existing_data.append(self.total_notice_data)
        with open('college_json_data/cec.json','w') as f:
            json.dump(existing_data, f, indent=4)

class CEC_InternalQualityAssuranceSpider(scrapy.Spider):
    name = "iqac_spider"
    start_urls = ["https://ceconline.edu/about/committees/internal-quality-assurance-cell-or-internal-audit-cell-iqac-iac/#1608789190414-66d69914-5d08"]

    total_internal_quality_assurance_data = ''
    def parse(self, response):
        # Extremely specific XPath using multiple conditions and text content
        iqac_div = response.xpath(
            '//div[contains(@class, "wpb_text_column") and contains(@class, "wpb_content_element")]'
            '/div[contains(@class, "wpb_wrapper")]'
            '/h2/strong[contains(text(), "Internal Quality Assurance Cell")]/ancestor::div[contains(@class,"wpb_wrapper")]' #go to the parent div
        )

        if iqac_div:
           
            text_content = iqac_div.xpath('.//p/text()').get()
            if text_content:
                self.total_internal_quality_assurance_data = {'iqac_description': text_content.strip()}
            else:
                self.log("No <p> tag or text content found within the IQAC div.")
        else:
            self.log("IQAC div not found. Check the XPath.")
    
    def closed(self, reason):
        # This method is called when the spider is closed
        with open('college_json_data/cec.json', 'r') as f:
            existing_data  = json.load(f)
            existing_data.append(self.total_internal_quality_assurance_data)
        with open('college_json_data/cec.json','w') as f:
            json.dump(existing_data, f, indent=4)

class CEC_FacilitiesSpider(scrapy.Spider):
    name = "facilities_spider"
    start_urls = ["https://ceconline.edu/about/facilities/"]

    total_facility_data = ''

    def parse(self, response):
        # Target the paragraph directly and extract text
        facility_description = response.xpath('//h2[text()="Facilities"]/following-sibling::div//p/text()').get()
        if facility_description:
            self.total_facility_data = {"facility description in CEC": facility_description.strip()}
        else:
            self.log("Facility description not found.")
    
    def closed(self, reason):
        # This method is called when the spider is closed
        with open('college_json_data/cec.json', 'r') as f:
            existing_data  = json.load(f)
            existing_data.append(self.total_facility_data)
        with open('college_json_data/cec.json','w') as f:
            json.dump(existing_data, f, indent=4)

class CEC_CollegeInfoSpider(scrapy.Spider):
    name = "college_info_spider"
    start_urls = ["https://ceconline.edu/contact-us/"]

    total_college_contact_info_data = ''

    def parse(self, response):
        contact_items = response.xpath('//div[contains(@class, "stm-map__content")]//ul[@class="stm-contact-details__items"]/li')
        contacts = {}
        for item in contact_items:
            detail_text = item.xpath('.//text()').get().strip()
            detail_type = item.xpath('@class').get()
            if detail_type:
                detail_type = detail_type.split("_")[-1]
                contacts[detail_type] = detail_text
            else:
                pass  

        location_section = response.xpath('//div[contains(@class, "entry-content")]//div[@class="wpb_wrapper"]')
        if location_section:
            location_details = {}
            main_description = location_section.xpath('./p[1]/text()').get("").strip()
            if main_description:
                location_details["main_description"] = main_description

            transit_details = {}
            transit_paragraphs = location_section.xpath('./p[position() > 1]')
            for p in transit_paragraphs:
                strong_text = p.xpath('./strong/text()').get("").strip()
                if strong_text:
                    rest_of_text = "".join(p.xpath('./text()[not(ancestor::strong)]').getall()).strip()
                    transit_details[strong_text.replace(":", "").strip()] = rest_of_text.strip()
            if transit_details:
                location_details["transit_distances"] = transit_details

        google_maps_info = {}
        google_maps_card = response.xpath('//div[contains(@class, "place-card") and contains(@jsaction, "placeCard.directions")]')

        if google_maps_card:
            google_maps_info = {}
            link = google_maps_card.xpath('.//a[contains(@class, "navigate-link")]/@href').get()
            if link:

                google_maps_info["college_name"] = link.split("+")[0].replace("College+of+Engineering+", "").strip()

        self.total_college_contact_info_data = {
            "contact_details about CEC": contacts,
            "CEC College Location Details": location_details,
            "google_maps_info": google_maps_info if google_maps_info else None  
        }
    
    def closed(self, reason):
        # This method is called when the spider is closed
        with open('college_json_data/cec.json', 'r') as f:
            existing_data  = json.load(f)
            existing_data.append(self.total_college_contact_info_data)
        with open('college_json_data/cec.json','w') as f:
            json.dump(existing_data, f, indent=4)

class CEC_CommitteeSpider(scrapy.Spider):
    name = "committee_spider"
    start_urls = ["https://ceconline.edu/about/committees/rti/"]

    total_commitee_data = ''

    def parse(self, response):
        committees_xpath = response.xpath(
            '//div[contains(@class, "vc_column-inner")]'
            '/div[contains(@class, "wpb_wrapper")]'
            '/div[contains(@class, "wpb_text_column") and contains(@class, "wpb_content_element")]'
        )

        committee_details = []
        for committee_section in committees_xpath:
            committee_title = committee_section.xpath(".//h3/strong/text()").get().strip()
            if committee_title:
                details = {"name": committee_title, "officers": []} 
                officer_info = committee_section.xpath(".//p")
                for officer in officer_info:
                    text_parts = officer.xpath(".//span/text()").getall() 
                    if text_parts:
                        name = text_parts[0].strip()
                        designation = text_parts[1].strip() if len(text_parts)>1 else None
                        contact= None
                        if officer.xpath('.//a/@href').get():
                            contact = officer.xpath('.//a/@href').get()
                        details["officers"].append({
                            "name": name,
                            "designation": designation,
                            "contact": contact,
                        })

                committee_details.append(details)

        if committee_details:
            self.total_commitee_data = {"committee_details": committee_details}
        else:
            self.log("No committee sections found. Check the XPath.")
    
    def closed(self, reason):
        # This method is called when the spider is closed
        with open('college_json_data/cec.json', 'r') as f:
            existing_data  = json.load(f)
            existing_data.append(self.total_commitee_data)
        with open('college_json_data/cec.json','w') as f:
            json.dump(existing_data, f, indent=4)
        
class CEC_BoardOfGovernorsSpider(scrapy.Spider):
    name = "bog"
    start_urls = ['https://ceconline.edu/board-of-governors/']

    total_bog_data = []
    
    def parse(self, response):
        table = response.xpath('//div[@class="wpb_wrapper"]//table[contains(., "Board of Governors")]')
        rows = table.xpath('.//tr[td]') 

        for row in rows:
            # sl_no = row.xpath('td[1]/strong/text()').get()
            name_designation = row.xpath('td[2]/strong/text()').get()
            designation = row.xpath('td[3]/strong/text()').get()
            role = row.xpath('td[4]/strong/text()').get()
            if  name_designation and designation:
                self.total_bog_data.append({
                    # 'Sl.No': sl_no.strip(),
                    'Name and Designation': name_designation.strip(),
                    'Designation': designation.strip(),
                    'Role': role.strip() if role else '',
                })

    def closed(self, reason):
        # This method is called when the spider is closed
        with open('college_json_data/cec.json', 'r') as f:
            existing_data  = json.load(f)
            existing_data.append(self.total_bog_data)
        with open('college_json_data/cec.json','w') as f:
            json.dump(existing_data, f, indent=4)

class CEC_AntiRaggingSpider(scrapy.Spider):
    name = "antiragging_spider"
    start_urls = ["https://ceconline.edu/about/committees/anti_ragging/"]

    total_anti_ragging_cell_data = ''

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
                self.total_anti_ragging_cell_data = {"details_about_anti_ragging_cell": details}
            else:
                self.log("No functions found within the anti-ragging section.")
        else:
            self.log("Anti-ragging section not found. Check the XPath.")
    
    def closed(self, reason):
        # This method is called when the spider is closed
        with open('college_json_data/cec.json', 'r') as f:
            existing_data  = json.load(f)
            existing_data.append(self.total_anti_ragging_cell_data)
        with open('college_json_data/cec.json','w') as f:
            json.dump(existing_data, f, indent=4)
    
class CEC_AnnounceSpider(scrapy.Spider):
    name = 'announce_spider'
    start_urls = ['https://ceconline.edu/announcements/']

    total_announcement_data = []
    
    def parse(self, response):
        # Dictionary mapping element IDs to notice identifiers and texts
        notice_mapping = {
            '0fa72ab': {
                'id': 'btech_registration',
                'text': 'Registration Form - B.Tech Admission 2024'
            },
            '7089465': {
                'id': 'btech_fee',
                'text': 'B.Tech  Fee Structure 2024-25'
            },
            '2099742': {
                'id': 'nri_fee',
                'text': 'NRI Fee Structure'
            },
            'd2d9dc9': {
                'id': 'let_fee',
                'text': 'LET Fee Structure'
            },
            '4b5f897': {
                'id': 'mca_fee',
                'text': 'MCA Fee Structure'
            }
        }
        
        for element_id, info in notice_mapping.items():
            notice_element = response.xpath(
                f"//div[contains(@class, 'elementor-element-{element_id}')]"
                "//div[contains(@class, 'elementor-widget-container')]"
                "//h2[contains(@class, 'elementor-heading-title')]"
                "//a"
            ).get() 
            
            if notice_element:
                notice_selector = scrapy.Selector(text=notice_element)
                link = notice_selector.xpath('//a/@href').get('')
                text = notice_selector.css('u::text').get('')
                
                if not text: 
                    text = notice_selector.xpath('//a/text()').get('').strip()
                if link and link.startswith('/'):
                    link = urljoin(response.url, link)
                    
                if link:  
                    doc_type = self.get_document_type(link)

                    print("hello???")
                    
                    self.total_announcement_data.append({
                        'data_type': 'notice',
                        'id': info['id'],
                        'title': text,
                        'url': link,
                        'type': doc_type,
                        'element_id': element_id,
                        'matched_text': info['text']
                    })
                    
                    if doc_type == 'pdf':
                        yield scrapy.Request(
                            url=link,
                            callback=self.save_pdf,
                            meta={
                                'title': text,
                                'notice_id': info['id']
                            },
                            errback=self.handle_error
                        )
    def get_document_type(self, url):
        if url.endswith('.pdf'):
            return 'pdf'
        elif 'forms.gle' in url:
            return 'google_form'
        elif url.startswith('http') or url.startswith('https'):
            return 'external_link'
        return 'other'

    def closed(self, reason):
        # This method is called when the spider is closed
        with open('college_json_data/cec.json', 'r') as f:
            existing_data  = json.load(f)
            existing_data.append(self.total_announcement_data)
        with open('college_json_data/cec.json','w') as f:
            json.dump(existing_data, f, indent=4)

class CEC_AICTEFeedbackSpider(scrapy.Spider):
    name = "aicte_feedback_spider"
    start_urls = ["https://ceconline.edu/aicte-feedback/"]

    total_aicte_data = ''

    def parse(self, response):
        notice_div = response.xpath(
            '//div[contains(@class, "wpb_wrapper")]'
            '/h1[contains(text(), "NOTICE")]'
            '/following-sibling::node()' 
        )
        if notice_div:
            feedback_links = {}
            for sibling in notice_div:
                if sibling.xpath('self::p'): #check if the sibling is a p tag
                    links = sibling.xpath(".//a")
                    for link in links:
                        text = link.xpath(".//text()").get()
                        href = link.xpath("@href").get()
                        if text and href:
                            feedback_links[text.strip()] = href.strip()

            if feedback_links:
                self.total_aicte_data = {'aicte_feedback_links': feedback_links}
            else:
                self.log("No links found within the AICTE feedback notice.")
        else:
            self.log("Notice div 'NOTICE' not found. Check the XPath.")
    
    def closed(self, reason):
        # This method is called when the spider is closed
        with open('college_json_data/cec.json', 'r') as f:
            existing_data  = json.load(f)
            existing_data.append(self.total_aicte_data)
        with open('college_json_data/cec.json','w') as f:
            json.dump(existing_data, f, indent=4)
    
class CEC_AdminStaffSpider(scrapy.Spider):
    name = "admin_staff"
    start_urls = ["https://ceconline.edu/about/administration/administrative-staff/"]

    total_admin_staff_data = ''

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
           self.total_admin_staff_data = {"administrative_staff": staff_data}
    
    def closed(self, reason):
        # This method is called when the spider is closed
        with open('college_json_data/cec.json', 'r') as f:
            existing_data  = json.load(f)
            existing_data.append(self.total_admin_staff_data)
        with open('college_json_data/cec.json','w') as f:
            json.dump(existing_data, f, indent=4)

class CEC_nri_AdmissionSpider(scrapy.Spider):
    name = 'nri_admission_spider'
    start_urls = [
        'https://ceconline.edu/b-tech-nri-admission-2024-25/'  # Replace with the actual URL
    ]
    
    total_admission_data = ''

    def parse(self, response):
        # Using specific data-id attributes to target exact elements
        admission_links = {
            "candidate_details": "//div[@data-id='db33835']//a/@href",
            "original_certificates": "//div[@data-id='7e372bc']//a/@href",
            "admission_schedule": "//div[@data-id='cd4f4f3']//a/@href"
        }
        
        # Get all PDF links
        pdf_links = []
        for key in admission_links:
            link = response.xpath(admission_links[key]).get()
            if link:
                # Convert relative URLs to absolute URLs
                absolute_url = urljoin(response.url, link)
                pdf_links.append(absolute_url)
        
        item = {}
        item['file_urls'] = pdf_links  # FilesPipeline will use this field
        
        # Store the original data as well
        item['candidate_details_link'] = response.xpath(admission_links['candidate_details']).get()
        item['original_certificates_link'] = response.xpath(admission_links['original_certificates']).get()
        item['admission_schedule_link'] = response.xpath(admission_links['admission_schedule']).get()
        
        item['candidate_details_text'] = response.xpath("//div[@data-id='db33835']//a/u/text()").get()
        item['original_certificates_text'] = response.xpath("//div[@data-id='7e372bc']//a/u/text()").get()
        item['admission_schedule_text'] = response.xpath("//div[@data-id='cd4f4f3']//a/u/text()").get()
        
        self.total_admission_data = item
    
    def closed(self, reason):
        # This method is called when the spider is closed
        with open('college_json_data/cec.json', 'r') as f:
            existing_data  = json.load(f)
            existing_data.append(self.total_admission_data)
        with open('college_json_data/cec.json','w') as f:
            json.dump(existing_data, f, indent=4)

