import scrapy

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