#!/bin/bash

mkdir -p airflow/dags airflow/logs airflow/plugins airflow/config
mkdir -p data/minio_storage data/postgre_storage
mkdir -p sql
mkdir -p docs/learning.md

touch sql/init_warehouse.sql
touch .env
touch gitignore.
touch docker-compose.yml
touch requirements.txt

echo "Project structure created."