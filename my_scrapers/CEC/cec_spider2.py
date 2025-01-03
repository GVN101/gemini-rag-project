import scrapy
import json
from urllib.parse import urljoin

class principal_spider(scrapy.Spider):
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
        with open('output2.json', 'r') as f:
            existing_data  = json.load(f)
            existing_data.append(self.total_principal_details)
        with open('output2.json','w') as f:
            json.dump(existing_data, f, indent=4)

class PTASpider(scrapy.Spider):
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
        with open('output2.json', 'r') as f:
            existing_data  = json.load(f)
            existing_data.append(self.total_pta_data)
        with open('output2.json','w') as f:
            json.dump(existing_data, f, indent=4)

class NoticeSpider(scrapy.Spider):
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
        with open('output2.json', 'r') as f:
            existing_data  = json.load(f)
            existing_data.append(self.total_notice_data)
        with open('output2.json','w') as f:
            json.dump(existing_data, f, indent=4)