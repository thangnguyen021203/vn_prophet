from minio import Minio
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import io

class MinIOService:
    "class responsible for communicate with Data Lake"
    def __init__(self, endpoint, access_key, secret_key, bucket_name):
        self.client = Minio(
            endpoint,
            access_key,
            secret_key,
            secure=False
        )
        self.bucket_name = bucket_name
        self._ensure_bucket_exists()
    
    def _ensure_bucket_exists(self):
        if not self.client.bucket_exists(self.bucket_name):
            self.client.make_bucket(self.bucket_name)
    
    def upload_html(self, path: str, html_content: str):
        data_bytes = html_content.encode('utf-8')
        data_stream = io.BytesIO(data_bytes)
        self.client.put_object(
            self.bucket_name,
            path,
            data_stream,
            length=len(data_bytes),
            content_type="text/html"
        )
        print(f"[MinIO] Saved: {path}")

class BrowserService:
    """Class responsible for control the brownser"""
    def __init__(self, selenium_url):
        self.selenium_url = selenium_url
        self.driver = self._init_driver()
    
    def _init_driver(self):
        opts = Options()
        opts.add_argument("--no-sandbox")
        opts.add_argument("--disable-dev-shm-usage")
        opts.add_argument("--window-size=1920,1080")
        opts.add_argument("--diasble-gpu")
        opts.add_argument("--headless=new")
        print("Toi day roi")
        return webdriver.Remote(command_executor=self.selenium_url, options=opts)
    
    def get_page(self, url):
        print(f"[Brownser] Visiting: {url}")
        self.driver.get(url)
    
    def get_source(self):
        return self.driver.page_source
    
    def scroll_page(self, steps=4):
        import time
        import random
        for i in range(1, steps):
            self.driver.execute_script(f"window.scrollTo(0, document.body.scrollHeight * {i/steps});")
            time.sleep(random.uniform(0.5,1.0))
        
    
    def close(self):
        self.driver.quit()