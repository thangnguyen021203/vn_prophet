from scraper.src.services import BrowserService, MinIOService
from scraper.src.alonhadat import AloNhaDatScraper
from scraper.src.batdongsan import BatDongSanScraper
import os
from dotenv import load_dotenv

load_dotenv()

#Cau hinh (Nen load tu bien moi truong - Environment Variables)
SELENIUM_URL = os.getenv("SELENIUM_URL")
MINIO_ENDPOINT = os.getenv("MINIO_ENDPOINT")
MINIO_ACCESS_KEY = os.getenv("MINIO_ACCESS_KEY")
MINIO_SECRET_KEY = os.getenv("MINIO_SECRET_KEY")
BUCKET_NAME = os.getenv("BUCKET_NAME")

def main():
    print("Starting Enterprise Scraper System...")

    #1. Khoi tao cac Services (Facade)
    browser_service = BrowserService(SELENIUM_URL)
    print("Done set up browser!!!")
    minio_service = MinIOService(
        MINIO_ENDPOINT,
        MINIO_ACCESS_KEY,
        MINIO_SECRET_KEY,
        BUCKET_NAME
    )
    
    #2. Khoi tao Scraper cu the
    alonhadat_scraper = AloNhaDatScraper(browser=browser_service, storage=minio_service)
    batdongsan_scraper = BatDongSanScraper(browser=browser_service, storage=minio_service)
    #3. Run Template Method
    alonhadat_scraper.run(start_page=1, end_page=3)
    batdongsan_scraper.run(start_page=1, end_page=3)
    #4. Dong trinh duyet
    browser_service.close()
if __name__ == "__main__":
    main()