from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

# COLLEGE OF ENGINEERING CHENGANNUR
from my_scrapers.CEC.cec_spider import * 
# from my_scrapers.CEC.cec_spider2 import * # Done by Govind

# COLLEGE OF ENGINEERING ADOOR
from my_scrapers.AEC.aec_scraper import *

# COLLEGE OF ENGINERRING KARUNGAPPALLY
from my_scrapers.CEK.cek_scraper import *

def main():

    
    process = CrawlerProcess(get_project_settings()) 

    clear_file() # defintion is in cec_scraper file

    #COLLEGE OF ENGINEERING CHENGANNUR
    # process.crawl(CEC_principal_spider)
    # process.crawl(CEC_PTASpider)
    # process.crawl(CEC_NoticeSpider)
    # process.crawl(CEC_DepartmentSpider) 
    # process.crawl(CEC_placementSpider)
    # process.crawl(CEC_AdmissionsSpider)
    # process.crawl(CEC_organisationSpider)
    # process.crawl(CEC_InternalQualityAssuranceSpider)
    # process.crawl(CEC_FacilitiesSpider)
    # process.crawl(CEC_CollegeInfoSpider)
    # process.crawl(CEC_CommitteeSpider)
    # process.crawl(CEC_BoardOfGovernorsSpider)
    # process.crawl(CEC_AntiRaggingSpider)
    # process.crawl(CEC_AnnounceSpider)
    # process.crawl(CEC_AICTEFeedbackSpider)
    # process.crawl(CEC_AdminStaffSpider)
    # process.crawl(CEC_nri_AdmissionSpider)

    #COLLEGE OF ENGINEERING ADOOR
    # process.crawl(AEC_DepartmentSpider)
    # process.crawl(AEC_AlumniSpider)

    #COLLEGE OF ENGINEERING KARUNAGAPPALLY
    # process.crawl(CEK_principal)
    # process.crawl(CEK_management)
    # process.crawl(CEK_admin_staff)
    # process.crawl(CEK_overview)
    # process.crawl(CEK_infrastructure)
    # process.crawl(CEK_anti_ragging_squad)
    process.crawl(CEK_Departmentdata)
    process.start()

if __name__ == "__main__":
    main()