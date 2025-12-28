# Ke thua tu image chinh hang
FROM apache/airflow:2.9.1

# Chuyen sang user root de cai goi he thong
USER root
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    && apt-get autoremove -yqq --purge \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# chuyen lai user airflow de cai thu vien Python
USER airflow

# Copy file requirements vao trong container
COPY requirements.txt /requirements.txt

# Cai dat thu vien
RUN pip install --no-cache-dir -r /requirements.txt