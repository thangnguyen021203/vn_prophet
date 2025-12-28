from bs4 import BeautifulSoup
import re
from parser.src.base_parser import BaseParser

class AlonhadatParser(BaseParser):
  def get_source_folder(self) -> str:
    return "alonhadat"
  
  def parse_html(self, html_content: str, source_info: str) -> dict:
    """
    Input: 
    - html_content: html content of a page
    Output:
    - dictionary of information of each property
    """
    
    soup = BeautifulSoup(html_content, 'html.parser')
    data = {'source_url': source_info}
    print(data)
    try:
        list_property_box = soup.find_all(class_='property-item')
        data['each_property'] = []

        for property_box in list_property_box:
          each_property = {}

          # Date
          full_date = property_box.select_one('.created-date').get('datetime')
          year, month, day, date_sk = self._clean_date(full_date)
          each_property['date_sk'] = date_sk
          each_property['year'] = year
          each_property['month'] = month 
          each_property['day'] = day

          # Details
          property_detail = property_box.select_one('.property-details')

          street_width = property_detail.select_one('div .street-width')
          each_property['street_width'] = self._clean_street_width(street_width.get_text()) \
                                          if street_width else None

          floors = property_detail.select_one('div .floors')
          each_property['floors'] = self._clean_floor_count(floors.get_text()) \
                                    if floors else None

          bedroom_count = property_detail.select_one('div .bedroom')
          each_property['bedroom_count'] = self._clean_bedroom_count(bedroom_count.select_one('[itemprop="value"]').get_text()) \
                                           if bedroom_count else None
          
          # Coi co khong thi implement sau
          bathroom_count = None
          each_property['bathroom_count'] = self._clean_bathroom_count(bathroom_count)

          price = property_detail.select_one('div .price').select_one('[itemprop="price"]')
          each_property['price'] = self._clean_price(price.get_text()) \
                                   if price else None

          area = property_detail.select_one('div .area').select_one('[itemprop="value"]')
          each_property['area'] = self._clean_area(area.get_text()) \
                                  if area else None
          
          each_property['price_per_m2'] = self._clean_price_per_m2(each_property['price'], each_property['area'])\
                                         if price and area else None

          parking_loc = True if property_detail.select_one('div .parking') else False
          each_property['parking_loc'] = self._clean_parking_loc(parking_loc)
          
          # Address
          property_address = property_box.select_one('.property-address')
          new_address = property_address.select_one('.new-address')
          each_property['new_location'] = True

          new_street = new_address.select_one('[itemprop="streetAddress"]').get_text()
          each_property['street'] = new_street

          new_ward = new_address.select_one('[itemprop="addressLocality"]').get_text()
          each_property['ward'] = new_ward

          new_province = new_address.select_one('[itemprop="addressRegion"]').get_text()
          each_property['province'] = new_province

          data['each_property'].append(each_property)
        
    except Exception as e:
      print(f"Parse error {source_info}: {e}")
      return None
    
    return data

  # Helper methods (Private)
  def _clean_date(self, full_date):
    date = full_date.split("-")
    year = int(date[0])
    month = int(date[1])
    day = int(date[2])
    date_sk = int(str(year) + str(month) + str(day))
    return (year, month, day, date_sk)

  def _clean_price(self, raw):
    price_and_currency = raw.split(" ")
    currency = price_and_currency[1]
    price = price_and_currency[0].split(",")
    integer_price = float(price[0]) # So truoc dau phay 
    quotient_price = float("0." + price[1]) if len(price) > 1 else 0 # So sau dau phay
    whole_price = (integer_price + quotient_price)

    if len(currency) > 2: # Trieu
      return whole_price * 1000000
    else:
      return whole_price * 1000000000

  def _clean_area(self, raw):
    return int(raw.split(" ")[0])
  
  def _clean_price_per_m2(self, clean_price, clean_area):
    return round(clean_price/clean_area, 2)

  def _clean_street_width(self, raw):
    # print(raw)
    value = raw[:-1]
    split_value = value.split(",")
    return round(float(value.replace(',','.')),2)
    # return round(float("".join(split_value))/(10**len(split_value[1])),2)
  
  def _clean_bedroom_count(self, raw):
    return int(raw.split(" ")[0])

  def _clean_bathroom_count(self, raw):
    # Hien tai chua thay
    return raw
  
  def _clean_floor_count(self, raw):
    return int(raw.split(" ")[0])

  def _clean_parking_loc(self, raw):
    return raw