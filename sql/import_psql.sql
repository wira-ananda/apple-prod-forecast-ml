-- Execute AFTER schema.sql. All file paths refer to Docker container filesystem.
-- On macOS: docker exec pg-tableau mkdir -p /tmp/apple_retail_id
--           docker cp csv/. pg-tableau:/tmp/apple_retail_id/
\set ON_ERROR_STOP on
\copy apple_retail_id.category FROM '/tmp/apple_retail_id/category.csv' WITH (FORMAT csv, HEADER true, NULL '')
\copy apple_retail_id.stores FROM '/tmp/apple_retail_id/stores.csv' WITH (FORMAT csv, HEADER true, NULL '')
\copy apple_retail_id.products FROM '/tmp/apple_retail_id/products.csv' WITH (FORMAT csv, HEADER true, NULL '')
\copy apple_retail_id.campaigns FROM '/tmp/apple_retail_id/campaigns.csv' WITH (FORMAT csv, HEADER true, NULL '')
\copy apple_retail_id.sales FROM '/tmp/apple_retail_id/sales.csv' WITH (FORMAT csv, HEADER true, NULL '')
\copy apple_retail_id.warranty FROM '/tmp/apple_retail_id/warranty.csv' WITH (FORMAT csv, HEADER true, NULL '')
\copy apple_retail_id.daily_product_sales FROM '/tmp/apple_retail_id/daily_product_sales.csv' WITH (FORMAT csv, HEADER true, NULL '')
