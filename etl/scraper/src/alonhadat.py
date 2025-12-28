from scraper.src.base_scraper import BaseScraper

class AloNhaDatScraper(BaseScraper):
    def get_base_url(self)->str:
        return "https://alonhadat.com.vn/can-ban-nha-dat/trang-{}"

    def get_source_name(self)->str:
        return "alonhadat"