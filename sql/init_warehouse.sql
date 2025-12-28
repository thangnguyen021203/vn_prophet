-- 1. DIMENSION: LOCATION
-- 2. DIMENSION: PROPERTY TYPE
-- 3. DIMENSION: DATE
-- 4. FACT: LISTING

CREATE TABLE IF NOT EXISTS dim_location (
    location_sk SERIAL PRIMARY KEY,
    province VARCHAR(100) DEFAULT 'Ho Chi Minh',
    -- district VARCHAR(100), 
    ward VARCHAR(100), 
    street VARCHAR(200), 
    new_location BOOLEAN -- old or new location
);

CREATE TABLE IF NOT EXISTS dim_date (
    date_sk INT PRIMARY KEY, -- 20251231
    year INT,
    month INT,
    day INT
);

CREATE TABLE IF NOT EXISTS dim_property_type (
    type_sk SERIAL PRIMARY KEY,
    type_name VARCHAR(100), -- nha pho, nha ngo, nha hem, biet thu, chung cu
    parking_loc BOOLEAN,
    residental_area BOOLEAN
);

CREATE TABLE IF NOT EXISTS fact_listing (
    listing_sk SERIAL PRIMARY KEY,

    -- keys
    date_sk INT REFERENCES dim_date(date_sk),
    location_sk INT REFERENCES dim_location(location_sk),
    type_sk INT REFERENCES dim_property_type(type_sk),

    -- Source Info 
    source_url TEXT, -- link gocs
    -- source_id VARCHAR(50), -- ID tin dang goc

    -- Metrics
    price DECIMAL(18,2), -- Gia (VND)
    area_m2 DECIMAL (10,2), -- Dien tich (m2)
    price_per_m2 DECIMAL (18,2), -- Don gia/m2 (Tinh toan)
    street_width DECIMAL (4,2),
    bedroom_count INT,
    bathroom_count INT,
    floor_count INT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);