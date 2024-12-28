from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

# COLLEGE OF ENGINEERING CHENGANNUR
from my_scrapers.CEC.cec_spider import *
from my_scrapers.CEC.aicte_page import *
from my_scrapers.CEC.board_of_governors import *
from my_scrapers.CEC.admin_staff import *
from my_scrapers.CEC.nri_admission import *

def main():
    #CEC SCRAPER
    process = CrawlerProcess(get_project_settings())
    # process.crawl(DepartmentSpider) 
    # process.crawl(placementSpider)
    # process.crawl(AdmissionsSpider)
    # process.crawl(organisationSpider)
    # process.crawl(AICTEFeedbackSpider)
    # process.crawl(BoardOfGovernorsSpider)
    process.crawl(AdminStaffSpider)
    process.crawl(NRI_admission_spider)
    
    process.start()

if __name__ == "__main__":
    main()