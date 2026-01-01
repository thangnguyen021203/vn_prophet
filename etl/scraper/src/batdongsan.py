from scraper.src.base_scraper import BaseScraper

class BatDongSanScraper(BaseScraper):
    def get_base_url(self)->str:
        return "https://batdongsan.com.vn/nha-dat-ban/p{}"
    
    def get_source_name(self)->str:
        return "batdongsan"