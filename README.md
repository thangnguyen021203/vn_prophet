# VN Prophet - Hệ thống ETL cho dữ liệu bất động sản Việt Nam

## Mô tả dự án

VN Prophet là một hệ thống ETL (Extract, Transform, Load) tự động để thu thập, xử lý và lưu trữ dữ liệu bất động sản từ các nguồn trực tuyến Việt Nam. Dự án sử dụng Apache Airflow để quản lý workflow, Selenium để scraping dữ liệu, MinIO để lưu trữ file, và PostgreSQL để lưu trữ dữ liệu đã xử lý.

Dự án tuân theo phương pháp thiết kế Kimball Warehouse, sử dụng dimensional modeling với star schema bao gồm các bảng dimension (dim_date, dim_location, dim_property_type) và bảng fact (fact_listing) để tối ưu hóa truy vấn và phân tích dữ liệu.

## Tính năng chính

- **Thu thập dữ liệu tự động**: Sử dụng Selenium để crawl dữ liệu từ các trang web bất động sản như Alonhadat.
- **Xử lý dữ liệu**: Phân tích và làm sạch dữ liệu thu thập được.
- **Lưu trữ phân tán**: Sử dụng MinIO cho lưu trữ file và PostgreSQL cho dữ liệu cấu trúc.
- **Workflow orchestration**: Apache Airflow quản lý và theo dõi các tác vụ ETL.
- **Container hóa**: Chạy toàn bộ hệ thống trong Docker để dễ dàng triển khai.

## Công nghệ sử dụng

- **Apache Airflow**: Quản lý workflow và scheduling.
- **Selenium**: Web scraping với Chrome headless.
- **MinIO**: Object storage cho file dữ liệu.
- **PostgreSQL**: Database cho dữ liệu warehouse.
- **Docker & Docker Compose**: Container hóa và orchestration.
- **Python**: Ngôn ngữ chính cho ETL scripts.

## Cấu trúc dự án

```
vn_prophet/
├── airflow/                 # Airflow configuration và DAGs
│   ├── dags/               # Directed Acyclic Graphs
│   ├── logs/               # Logs của Airflow
│   ├── plugins/            # Plugins tùy chỉnh
│   └── Dockerfile          # Docker image cho Airflow
├── etl/                    # Scripts ETL
│   ├── scraper/            # Module thu thập dữ liệu
│   └── parser/             # Module xử lý dữ liệu
├── data/                   # Thư mục lưu trữ dữ liệu
│   ├── airflow_metadata_storage/  # Metadata của Airflow
│   ├── minio/              # Dữ liệu MinIO
│   └── warehouse_storage/  # Dữ liệu PostgreSQL
├── setup/                  # Scripts setup
├── sql/                    # Scripts SQL cho database
├── docker-compose.yml      # Orchestration Docker
├── requirements.txt        # Dependencies Python
└── .env                    # Environment variables
```

## Cài đặt và chạy

### Yêu cầu hệ thống

- Docker và Docker Compose
- Ít nhất 4GB RAM (Chrome & Airflow)
- Linux/MacOS (khuyến nghị)

### Các bước cài đặt

1. **Clone repository**:
   ```bash
   git clone <repository-url>
   cd vn_prophet
   ```

2. **Cấu hình environment**:
   Chỉnh sửa file `.env` nếu cần thiết (các giá trị mặc định đã được thiết lập).

3. **Khởi chạy hệ thống**:
   ```bash
   sudo docker-compose up -d
   ```

4. **Truy cập các dịch vụ**:
   - **Airflow Web UI**: http://localhost:8080 (user: <$env>, password: <$env>)
   - **MinIO Console**: http://localhost:9001 (user: <$env>, password: <$env>)
   - **PostgreSQL Warehouse**: localhost:5432 (user: <$env>, password: <$env>)

### Chạy DAG

1. Truy cập Airflow Web UI.
2. Bật DAG `vn_prophet_daily_pipeline`.
3. Trigger DAG thủ công hoặc chờ schedule (7:00 AM hàng ngày).

## Sử dụng

### Workflow ETL

1. **Scraper**: Thu thập dữ liệu từ web và lưu vào MinIO.
2. **Parser**: Đọc dữ liệu từ MinIO, xử lý và lưu vào PostgreSQL warehouse.

### Giám sát

- Sử dụng Airflow UI để theo dõi trạng thái các task.
- Kiểm tra logs trong thư mục `airflow/logs/`.
- Giám sát MinIO và PostgreSQL qua các console tương ứng.

## Phát triển

### Thêm scraper mới

1. Tạo module mới trong `etl/scraper/src/`.
2. Implement class kế thừa từ `BaseScraper`.
3. Cập nhật DAG trong `airflow/dags/daily_ingest_dag.py`.

### Thêm parser mới

1. Tạo module mới trong `etl/parser/src/`.
2. Implement class kế thừa từ base parser.
3. Cập nhật DAG tương ứng.

## Lộ trình phát triển tương lai

- **Mở rộng scraper**: Thêm nhiều scraper từ các website bất động sản khác như Batdongsan, Nhà đất 24h, etc. để tăng độ phủ sóng dữ liệu.
- **Module BI**: Phát triển dashboard và báo cáo sử dụng công cụ như Apache Superset hoặc Tableau để trực quan hóa dữ liệu.
- **Ứng dụng ML/AI**: Tích hợp machine learning và AI để phân tích dự đoán giá bất động sản, xu hướng thị trường, và đề xuất đầu tư.

## Troubleshooting

### Lỗi thường gặp

1. **Connection refused đến MinIO/PostgreSQL**:
   - Đảm bảo tất cả containers đang chạy: `docker-compose ps`
   - Kiểm tra logs: `docker-compose logs <service-name>`

2. **DAG không load được**:
   - Kiểm tra syntax errors trong DAG file.
   - Restart Airflow: `docker-compose restart airflow-webserver`

3. **Scraper bị block**:
   - Thêm delay giữa các request.
   - Sử dụng proxy hoặc thay đổi user agent.

### Logs và debugging

- Airflow logs: `airflow/logs/`
- Container logs: `docker-compose logs`

