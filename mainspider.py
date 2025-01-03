from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

# COLLEGE OF ENGINEERING CHENGANNUR
from my_scrapers.CEC.cec_spider import *
from my_scrapers.AEC.aec_scraper import *
from my_scrapers.MEC.mec_scraper import *

def main():
    #CEC SCRAPER
    settings = get_project_settings()
    settings.set('ROBOTSTXT_OBEY',True)
    settings.set('USER_AGENT','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36')
    process = CrawlerProcess(settings)
    # process.crawl(DepartmentSpider) 
    # process.crawl(placementSpider)
    # process.crawl(AdmissionsSpider)
    # process.crawl(organisationSpider)
    # process.crawl(AECDepartmentSpider)
    process.crawl(MECDepartmentSpider)
    process.start()

if __name__ == "__main__":
    main()