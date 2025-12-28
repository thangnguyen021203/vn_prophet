from abc import ABC, abstractmethod
from parser.src.services import MinIOService, PostgresService

class BaseParser(ABC):
  def __init__(self, storage: MinIOService, warehouse: PostgresService):
    self.storage = storage
    self.warehouse = warehouse

  @abstractmethod
  def parse_html(self, html_content: str, source_info: str) -> dict:
    """Logic parse HTML (BeautifulSoup)"""
    pass

  @abstractmethod
  def get_source_folder(self) -> str:
    """Parser nay chiu trach nhiem folder nao?"""
    pass
  
  # TEMPLATE METHOD
  def run(self):
    print(f"Parser started for source: {self.get_source_folder()}")

    # 1. Lay danh sach file can xu ly
    files = self.storage.list_html_files(prefix=self.get_source_folder())
    print(f"Found {len(files)} files to process.")

    for file_path in files:
      print(f"Processing: {file_path}...")

      #2. Doc noi dung
      html_content = self.storage.get_html_content(file_path)

      #3. Parse (abstract - class con se lam)
      data = self.parse_html(html_content, file_path) 
      print("", data)
      #4. Luu vao Warehouse
      if data:
        self.warehouse.save_listing(data)
        pass