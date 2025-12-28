from abc import ABC, abstractmethod
import time
import random
from datetime import datetime
from scraper.src.services import BrowserService, MinIOService

class BaseScraper(ABC):
    def __init__(self, browser: BrowserService, storage: MinIOService):
        self.browser = browser
        self.storage = storage
    
    @abstractmethod
    def get_base_url(self)->str:
        """Class con phai dinh nghia URL goc"""
        pass

    @abstractmethod
    def get_source_name(self)->str:
        """Ten nguon du lieu (vd: alonhadat)"""
        pass

    def generate_file_path(self, page:int)->str:
        now = datetime.now()
        return f"{self.get_source_name()}/year={now.year}/month={now.month:02d}/day={now.day:02d}/page_{page}.html"
    
    # Template Method
    def run(self, start_page=1, end_page=3):
        try:
            for page in range(start_page, end_page + 1):
                url = self.get_base_url().format(page)

                #1. Truy cap
                self.browser.get_page(url)

                #2. Hanh dong nguoi dung (Scroll)
                self.browser.scroll_page()

                #3. Lay du lieu
                html = self.browser.get_source()
                
                #4. Luu tru
                save_path = self.generate_file_path(page)
                self.storage.upload_html(save_path, html)

                #5. Nghi ngoi
                sleep_time = random.uniform(2,5)
                print(f"Sleeping {sleep_time:.2f}s...")
                time.sleep(sleep_time)
        except Exception as e:
            print(f"Error: {e}")
        finally:
            self.browser.close()
    