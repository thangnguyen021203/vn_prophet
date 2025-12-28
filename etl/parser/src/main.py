from parser.src.services import MinIOService, PostgresService
from parser.src.alonhadat import AlonhadatParser
import os
from dotenv import load_dotenv

load_dotenv()

MINIO_CONF = {
  "endpoint": os.getenv("MINIO_ENDPOINT"),
  "access_key": os.getenv("MINIO_ACCESS_KEY"),
  "secret_key": os.getenv("MINIO_SECRET_KEY"),
  "bucket_name": os.getenv("BUCKET_NAME")
}

DB_CONF = {
  "host": os.getenv("WAREHOUSE_HOST"),
  "port": os.getenv("WAREHOUSE_PORT"),
  "database": os.getenv("WAREHOUSE_DB"),
  "user": os.getenv("WAREHOUSE_USER"),
  "password": os.getenv("WAREHOUSE_PASSWORD")
}

def main():
  # 1. Init Services
  minio = MinIOService(**MINIO_CONF)
  postgres = PostgresService(DB_CONF)

  # 2. Init Parser
  parser = AlonhadatParser(storage=minio, warehouse=postgres)

  # 3. Run
  parser.run()

if __name__ == "__main__":
  main()