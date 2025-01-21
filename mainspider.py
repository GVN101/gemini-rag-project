from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from playwright.sync_api import sync_playwright

# COLLEGE OF ENGINEERING CHENGANNUR
from my_scrapers.CEC.cec_spider import * 

# COLLEGE OF ENGINEERING ADOOR
from my_scrapers.AEC.aec_scraper import *

# COLLEGE OF ENGINERRING KARUNGAPPALLY
from my_scrapers.CEK.cek_scraper import *

# MODEL ENGINEERING COLLEGE
from my_scrapers.MEC.mec_scraper import *

#COLLEGE OF APPLIED SCIENCE ADOOR
from my_scrapers.CASA.casa_scraper import *


def main():

    process = CrawlerProcess(get_project_settings()) 

    clear_file() # defintion is in cec_scraper file

    # COLLEGE OF ENGINEERING CHENGANNUR
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

    # # COLLEGE OF ENGINEERING ADOOR
    # process.crawl(AEC_DepartmentSpider)
    # process.crawl(AEC_AlumniSpider)

    # # COLLEGE OF ENGINEERING KARUNAGAPPALLY
    # process.crawl(CEK_principal)
    # process.crawl(CEK_management)
    # process.crawl(CEK_admin_staff)
    # process.crawl(CEK_overview)
    # process.crawl(CEK_infrastructure)
    # process.crawl(CEK_anti_ragging_squad)
    # process.crawl(CEK_Departmentdata)
    # process.crawl(CEK_contact)
    # process.crawl(CEK_placement)
    # process.crawl(CEK_library)
    # process.start()

    # MODEL ENGINEERING COLLEGE
    # with sync_playwright() as playwright:
    #     scrape_principal_details(playwright)
    #     scrape_about_section(playwright)
    #     scrape_board_of_governors_section(playwright)
    #     scrape_administrative_staff_section(playwright)
    #     scrape_academic_council_section(playwright)
    #     scrape_pta_section(playwright)
    #     scrape_senate_section(playwright)
    #     scrape_admission_details_section(playwright)
    #     scrape_facilities(playwright)
    #     scrape_about_statutory_committee(playwright)
    #     scrape_iqac_section(playwright)
    #     scrape_grievance_cell(playwright)
    #     scrape_anti_ragging_committee(playwright)
    #     scrape_anti_ragging_squad(playwright)
    #     scrape_anti_sexual_harassment_cell(playwright)
    #     scrape_safety_manual(playwright)
    #     comp_sci_section(playwright,"About")
    #     comp_sci_section(playwright,"Vision & Mission")
    #     comp_sci_section(playwright,"Courses Offered")
    #     comp_sci_section(playwright,"HOD")
    #     comp_sci_section(playwright,"Faculty")
    #     comp_sci_section(playwright,"Facilities")
    #     comp_sci_section(playwright,"Resources")
    #     comp_sci_section(playwright,"Associations")
    #     comp_sci_section(playwright,"Achievements")
    #     comp_sci_section(playwright,"Recent Projects")
    #     electronics_and_communication_section(playwright,"About")
    #     electronics_and_communication_section(playwright,"Vision & Mission")
    #     electronics_and_communication_section(playwright,"Courses Offered")
    #     electronics_and_communication_section(playwright,"HOD")
    #     electronics_and_communication_section(playwright,"Faculty")
    #     electronics_and_communication_section(playwright,"Facilities")
    #     electronics_and_communication_section(playwright,"Resources")
    #     electronics_and_communication_section(playwright,"Associations")
    #     electronics_and_communication_section(playwright,"Achievements")
    #     electronics_and_communication_section(playwright,"Recent Projects")
    #     electrical_and_electronics_section(playwright,"About")
    #     electrical_and_electronics_section(playwright,"Vision & Mission")
    #     electrical_and_electronics_section(playwright,"Courses Offered")
    #     electrical_and_electronics_section(playwright,"HOD")
    #     electrical_and_electronics_section(playwright,"Faculty")
    #     electrical_and_electronics_section(playwright,"Facilities")
    #     electrical_and_electronics_section(playwright,"Resources")
    #     electrical_and_electronics_section(playwright,"Associations")
    #     electrical_and_electronics_section(playwright,"Recent Projects")
    #     electronics_and_biomedical_section(playwright,"About")
    #     electronics_and_biomedical_section(playwright,"Vision & Mission")
    #     electronics_and_biomedical_section(playwright,"Courses Offered")
    #     electronics_and_biomedical_section(playwright,"HOD")
    #     electronics_and_biomedical_section(playwright,"Faculty")
    #     electronics_and_biomedical_section(playwright,"Facilities")
    #     electronics_and_biomedical_section(playwright,"Resources")
    #     electronics_and_biomedical_section(playwright,"Associations")
    #     electronics_and_biomedical_section(playwright,"Achievements")
    #     electronics_and_biomedical_section(playwright,"Recent Projects")
    #     mechanical_engineering_section(playwright,"About")
    #     mechanical_engineering_section(playwright,"Courses Offered")
    #     mechanical_engineering_section(playwright,"HOD")
    #     mechanical_engineering_section(playwright,"Faculty")
    #     mechanical_engineering_section(playwright,"Facilities")
    #     mechanical_engineering_section(playwright,"Resources")
    #     applied_science_section(playwright,"About")
    #     applied_science_section(playwright,"HOD")
    #     applied_science_section(playwright,"Faculty")
    #     applied_science_section(playwright,"Resources")
    #     placements_section(playwright,"Activities")
    #     placements_section(playwright,"Placement Statistics")
    #     placements_section(playwright,"Brochure")
    #     placements_section(playwright,"Student Verification")
    #     placements_section(playwright, "Contact Details")
    #     placements_section(playwright,"Training Cell")


    # COLLEGE OF APPLIED SCIENCE ADOOR
    # process.crawl(CASA_principal)
    # process.crawl(CASA_Committee)
    # process.crawl(CASA_overview)
    # process.crawl(CASA_Mission_and_Vision)
    # process.crawl(CASA_Anti_rag_cell)
    # process.crawl(CASA_NSS)
    # process.crawl(CASA_cs_department)
    # process.crawl(CASA_ec_department)
    # process.crawl(CASA_cm_department)
    # process.crawl(CASA_math_department)
    process.crawl(CASA_english_department)
    process.start()

if __name__ == "__main__":
    main()

    
    # schedule.every(1).minutes.do(main)
    # while True:
    # # Checks whether a scheduled task 
    # # is pending to run or not
    #     schedule.run_pending()
    #     time.sleep(1)
