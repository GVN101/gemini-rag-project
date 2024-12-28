import scrapy
import json

class AICTEFeedbackSpider(scrapy.Spider):
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
                print("No links found within the AICTE feedback notice.")
        else:
            print("Notice div 'NOTICE' not found. Check the XPath.")

    def closed(self, response):
        data_dict = {"AICTE Feedback Links": self.total_aicte_data}
        with open('output.json','r') as f:
            data = json.load(f)
            data.append(data_dict)
        with open('output.json','w') as f:
            json.dump(data, f, indent=4)
