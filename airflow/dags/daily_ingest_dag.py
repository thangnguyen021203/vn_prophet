from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os

load_dotenv()

# 1. Default Args
default_args = {
  'owner': 'airflow',
  'depends_on_past': False,
  'email_on_failure': False,
  'retries': 1,
  'retry_delay': timedelta(minutes=1),
}

# 2. Khoi tao DAG

with DAG(
  'vn_prophet_daily_pipeline',
  default_args=default_args,
  description='Automated pipeline: Scrape -> Parse -> DB',
  schedule_interval='0 7 * * *',
  start_date=datetime(2023, 1, 1),
  catchup=False,
  tags=['proptech', 'scraping']
) as dag:
    scrape_env = {
      "SELENIUM_URL": os.getenv("SELENIUM_URL"),
      "MINIO_ENDPOINT": os.getenv("MINIO_ENDPOINT"),
      "MINIO_ACCESS_KEY": os.getenv("MINIO_ACCESS_KEY"),
      "MINIO_SECRET_KEY": os.getenv("MINIO_SECRET_KEY"),
      "BUCKET_NAME": os.getenv("BUCKET_NAME"),
      "PYTHONPATH": os.getenv("PYTHONPATH")
    }

    task_scrape = BashOperator(
      task_id = 'run_scraper',
      bash_command='python -m scraper.src.main',
      env=scrape_env,
      cwd='/opt/airflow'
    )

    parse_env = {
      # "MINIO_ENDPOINT": os.getenv("MINIO_ENDPOINT"),
      "MINIO_ENDPOINT": "minio:9000",
      "MINIO_ACCESS_KEY": os.getenv("MINIO_ACCESS_KEY"),
      "MINIO_SECRET_KEY": os.getenv("MINIO_SECRET_KEY"),
      "BUCKET_NAME": os.getenv("BUCKET_NAME"),
      "WAREHOUSE_HOST": os.getenv("WAREHOUSE_HOST"),
      "WAREHOUSE_PORT": os.getenv("WAREHOUSE_PORT", "5432"),
      "WAREHOUSE_DB": os.getenv("WAREHOUSE_DB"),
      "WAREHOUSE_USER": os.getenv("WAREHOUSE_USER"),
      "WAREHOUSE_PASSWORD": os.getenv("WAREHOUSE_PASSWORD"),
      "PYTHONPATH": os.getenv("PYTHONPATH")
    }

    task_parse = BashOperator(
      task_id='run_parser',
      bash_command='python -m parser.src.main',
      env=parse_env,
      cwd='/opt/airflow'
    )

    task_scrape >> task_parse