from minio import Minio
import psycopg2
import io
from sqlalchemy import create_engine, MetaData, Table, Column,  ForeignKey, Integer, String, Numeric, Text, Boolean, Date, TIMESTAMP, func, insert, select, exists 
from sqlalchemy.orm import sessionmaker

class MinIOService:
  def __init__(self, endpoint, access_key, secret_key, bucket_name):
    self.client = Minio(
      endpoint=endpoint,
      access_key=access_key,
      secret_key=secret_key,
      secure=False
    )
    self.bucket_name = bucket_name

  def list_html_files(self, prefix=""):
    """Liet ke cac file HTML trong bucket"""
    objects = self.client.list_objects(self.bucket_name, prefix=prefix, recursive=True)
    return [obj.object_name for obj in objects if obj.object_name.endswith('.html')]

  def get_html_content(self, object_name):
    """
    Đọc nội dung file toan bo bucket
    => Phat trien them doc toan bo noi dung file trong hôm nay
    """
    response = None
    try:
      response = self.client.get_object(self.bucket_name, object_name)
      return response.read().decode('utf-8')
    finally:
      if response:
        response.close()
  
  def move_to_processed(self, object_name):
    """(Nang cao) Di chuyen file da xu ly sang folder khac de khong parse lai"""
    pass

class PostgresService:
  def __init__(self, db_config):
    self.db_config = db_config
    self.engine = self._create_engine()
    self.dim_date_table, self.dim_location_table, self.dim_property_type, self.fact_listing_table = self.mapping_table_to_db()


  def _create_engine(self):
    DATABASE_URL = f"postgresql+psycopg2://{self.db_config["user"]}:{self.db_config["password"]}@{self.db_config["host"]}:{self.db_config["port"]}/{self.db_config["database"]}"
    return create_engine(DATABASE_URL)

  def mapping_table_to_db(self):
    metadata = MetaData()

    dim_date_table = Table('dim_date', metadata,
                          Column('date_sk', Integer, primary_key=True, autoincrement=False),
                          Column('year', Integer),
                          Column('month', Integer),
                          Column('day', Integer)
                          )

    dim_location_table = Table('dim_location', metadata,
                              Column('location_sk', Integer, primary_key=True, autoincrement=True),
                              Column('province', String(100), default= 'Ho Chi Minh'),
                              Column('ward', String(100)),
                              Column('street', String(200)),
                              Column('new_location', Boolean)
                              )

    dim_property_type = Table('dim_property_type', metadata,
                              Column('type_sk', Integer, primary_key=True),
                              Column('type_name', String(100)),
                              Column('parking_loc', Boolean),
                              Column('residental_area', Boolean)
                              )
    
    fact_listing_table = Table('fact_listing', metadata,
                              Column('listing_sk', Integer, primary_key=True, autoincrement=True),
                              Column('date_sk', ForeignKey("dim_date.date_sk")),
                              Column('location_sk', ForeignKey("dim_location.location_sk")),
                              Column('type_sk', ForeignKey("dim_property_type.type_sk")),
                              Column('source_url', Text),
                              # Column('source_id', String(50)),
                              Column('price', Numeric(precision=18, scale=2)),
                              Column('area_m2', Numeric(10,2)),
                              Column('price_per_m2', Numeric(18,2)),
                              Column('street_width', Numeric(4,2)),
                              Column('bedroom_count', Integer),
                              Column('bathroom_count', Integer),
                              Column('floor_count', Integer),
                              Column('created_at', TIMESTAMP(timezone=True), default=func.now())
                              )

    return (dim_date_table, dim_location_table, dim_property_type, fact_listing_table)
  
  def save_listing(self, data:dict):
    Session = sessionmaker(bind=self.engine)
    session = Session()
    list_property = data['each_property']

    for each_property in list_property:
      # print(each_property)
      self.save_data(session, each_property, data['source_url'])


  def save_data(self, session, data:dict, source_url:str):
    """Luu du lieu vao warehouse (Star schema)"""    

    self.save_data_to_dim_location(session, data)
    self.save_data_to_dim_date(session, data)
    self.save_data_to_dim_property_type(session, data)
    self.save_data_to_fact_listing(session, data, source_url)
  
  def save_data_to_fact_listing(self, session, data:dict, source_url:str):

    # Column('date_sk', ForeignKey("dim_date.date_sk")),
    date_sk = session.query(self.dim_date_table).filter_by(date_sk=data['date_sk']).all()[0][0]

    # ['date_sk']
    # Column('location_sk', ForeignKey("dim_location.location_sk")),
    location_sk = session.query(self.dim_location_table).filter_by(
                                                    province=data["province"],
                                                    ward=data["ward"],
                                                    street=data["street"],
                                                    new_location=data["new_location"]).all()[0][0]
    # print(location_sk)

    # Column('type_sk', ForeignKey("dim_property_type.type_sk")),
    type_sk = session.query(self.dim_property_type).filter_by(
                                                    type_name="townhouse",
                                                    parking_loc=data["parking_loc"],
                                                    residental_area=True)[0][0]
    # print(type_sk)

    source_url
    price = data["price"]
    area_m2 = data["area"]
    price_per_m2 = data["price_per_m2"]
    street_width = data["street_width"]
    bedroom_count = data["bedroom_count"]
    bathroom_count = data["bathroom_count"]
    floor_count = data["floors"]

    q = session.query(self.fact_listing_table).filter_by(date_sk=date_sk,
                                                         location_sk=location_sk,
                                                         type_sk=type_sk,
                                                         source_url=source_url,
                                                         price=price,
                                                         area_m2=area_m2,
                                                         price_per_m2=price_per_m2,
                                                         street_width=street_width,
                                                         bedroom_count=bedroom_count,
                                                         bathroom_count=bathroom_count,
                                                         floor_count=floor_count
                                                        )
    
    record_exists = session.query(q.exists()).scalar()
    
    if not record_exists: 
      try:
        stmt = insert(self.fact_listing_table).values(
                                                      date_sk=date_sk,
                                                      location_sk=location_sk,
                                                      type_sk=type_sk,
                                                      source_url=source_url,
                                                      price=price,
                                                      area_m2=area_m2,
                                                      price_per_m2=price_per_m2,
                                                      street_width=street_width,
                                                      bedroom_count=bedroom_count,
                                                      bathroom_count=bathroom_count,
                                                      floor_count=floor_count
                                                    )
        with self.engine.connect() as conn:
          conn.execute(stmt)
          # conn.commit()
      except Exception as e:
        print("Error save to fact_listing: ",e)



  def save_data_to_dim_location(self, session, data:dict):
    q = session.query(self.dim_location_table).filter_by(
                                                    province=data["province"],
                                                    ward=data["ward"],
                                                    street=data["street"],
                                                    new_location=data["new_location"]).all()
    record_exists = True if len(q) > 0 else False
    # record_exists = session.query(q.exists()).scalar()
    
    if not record_exists: 
      try:
        stmt = insert(self.dim_location_table).values(
                                          province = data["province"],
                                          ward = data["ward"],
                                          street = data["street"],
                                          new_location = data["new_location"]
                                          )
        with self.engine.connect() as conn:
          conn.execute(stmt)
          # conn.commit()
      except Exception as e:
        print("Error save to dim location: ",e)

  def save_data_to_dim_date(self, session, data:dict):
    
    q = session.query(self.dim_date_table).filter_by(date_sk=data['date_sk'])
    record_exists = session.query(q.exists()).scalar()
    
    if not record_exists: 
      try:
        stmt = insert(self.dim_date_table).values(
                                          date_sk=data["date_sk"],
                                          year = data["year"],
                                          month = data["month"],
                                          day = data["day"]
                                          )
        with self.engine.connect() as conn:
          conn.execute(stmt)
          # conn.commit()
      except Exception as e:
        print("Error save to dim date: ", e)
  
  def save_data_to_dim_property_type(self, session, data: dict):
    # CREATE TABLE IF NOT EXISTS dim_property_type (
    # type_sk SERIAL PRIMARY KEY,
    # type_name VARCHAR(100), -- nha pho (townhouse), nha ngo (lanehouse), biet thu (vila), chung cu (apartment)
    # parking_loc BOOLEAN,
    # residental_area BOOLEAN
    # );
    # q = session.query(self.dim_property_type).filter_by(type_name="nha pho",)  
    q = session.query(self.dim_property_type).filter_by(
                                                    type_name="townhouse",
                                                    parking_loc=data["parking_loc"],
                                                    residental_area=True)
    record_exists = session.query(q.exists()).scalar()
    if not record_exists: 
      try:
        stmt = insert(self.dim_property_type).values(
                                          type_name = "townhouse",
                                          parking_loc=data["parking_loc"],
                                          residental_area=True
                                          )
        with self.engine.connect() as conn:
          conn.execute(stmt)
          # conn.commit()
      except Exception as e:
        print("Error save to dim property type: ",e)