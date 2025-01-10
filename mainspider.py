from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

# COLLEGE OF ENGINEERING CHENGANNUR
from my_scrapers.CEC.cec_spider import * 
# from my_scrapers.CEC.cec_spider2 import * # Done by Govind

# COLLEGE OF ENGINEERING ADOOR
from my_scrapers.AEC.aec_scraper import *

# MODEL ENGINEERING COLLEGE
from my_scrapers.MEC.mec_scraper import *

# COLLEGE OF ENGINERRING KARUNGAPPALLY
from my_scrapers.CEK.cek_scraper import *

def main():

    #COLLEGE OF ENGINEERING CHENGANNUR
    process = CrawlerProcess(get_project_settings()) 
    clear_file()
    # process.crawl(principal_spider)
    # process.crawl(PTASpider)
    # process.crawl(NoticeSpider)

    # process.crawl(DepartmentSpider) 
    # process.crawl(placementSpider)
    # process.crawl(AdmissionsSpider)
    # process.crawl(organisationSpider)

    # process.crawl(InternalQualityAssuranceSpider)
    # process.crawl(FacilitiesSpider)
    # process.crawl(CollegeInfoSpider)
    # process.crawl(CommitteeSpider)
    # process.crawl(BoardOfGovernorsSpider)
    # process.crawl(AntiRaggingSpider)
    # process.crawl(AnnounceSpider)
    # process.crawl(AICTEFeedbackSpider)
    # process.crawl(AdminStaffSpider)
    # process.crawl(AdmissionSpider)

    # COLLEGE OF ENGINEERING ADOOR
    # process.crawl(AEC_DepartmentSpider)
    # process.crawl(AEC_AlumniSpider)

    # COLLEGE OF ENGINEERING KARUNAGAPPALLY
    # process.crawl(CEK_principal)
    # process.crawl(CEK_board_members)
    # process.crawl(CEK_management)
    # process.crawl(CEK_admin_staff)
    process.crawl(CEK_overview)
    process.start()

if __name__ == "__main__":
    main()