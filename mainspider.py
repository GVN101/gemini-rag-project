from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from my_scrapers.cec_spider import *

def main():
    process = CrawlerProcess(get_project_settings())
    process.crawl(DepartmentSpider) 
    process.crawl(placementSpider)
    process.crawl(AdmissionsSpider)
    process.crawl(organisationSpider)
    process.start()

if __name__ == "__main__":
    main()