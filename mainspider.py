from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

# COLLEGE OF ENGINEERING CHENGANNUR
from my_scrapers.CEC.cec_spider import *
from my_scrapers.CEC.cec_spider2 import *
from my_scrapers.AEC.aec_scraper import *
from my_scrapers.MEC.mec_scraper import *

def main():
    #CEC SCRAPER
    process = CrawlerProcess(get_project_settings())
    # process.crawl(principal_spider)
    # process.crawl(PTASpider)
    # process.crawl(NoticeSpider)

    process.crawl(DepartmentSpider) 
    process.crawl(placementSpider)
    process.crawl(AdmissionsSpider)
    process.crawl(organisationSpider)
    process.crawl(AECDepartmentSpider)
    process.start()

if __name__ == "__main__":
    main()