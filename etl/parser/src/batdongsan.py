from parser.src.base_parser import BaseParser

class BatDongSanParser(BaseParser):
    
    def get_source_folder(self) -> str:
        return "batdongsan"
    
    def parse(self, raw_data):
        # Implement parsing logic specific to BatDongSan here
        parsed_data = {}
        # Example parsing logic (to be replaced with actual implementation)
        parsed_data['title'] = raw_data.get('title', '')
        parsed_data['price'] = raw_data.get('price', 0)
        parsed_data['location'] = raw_data.get('location', '')
        return parsed_data