-- Apple Retail Indonesia Synthetic Case Study. Safe: creates a NEW named schema.
-- NO DROP/TRUNCATE or modification to public / other schemas.
CREATE SCHEMA IF NOT EXISTS apple_retail_id;

CREATE TABLE IF NOT EXISTS apple_retail_id.category (
 category_id TEXT PRIMARY KEY,
 category_name TEXT NOT NULL UNIQUE
);
CREATE TABLE IF NOT EXISTS apple_retail_id.stores (
 store_id TEXT PRIMARY KEY,
 store_name TEXT NOT NULL,
 city TEXT NOT NULL,
 province TEXT NOT NULL,
 country TEXT NOT NULL CHECK(country='Indonesia'),
 region TEXT NOT NULL,
 store_type TEXT NOT NULL,
 simulated_opening_date DATE NOT NULL,
 simulated_traffic_index NUMERIC(6,2) NOT NULL
);
CREATE TABLE IF NOT EXISTS apple_retail_id.products (
 product_id TEXT PRIMARY KEY,
 product_name TEXT NOT NULL,
 category_id TEXT NOT NULL REFERENCES apple_retail_id.category(category_id),
 variant_description TEXT NOT NULL,
 reference_price_idr BIGINT NOT NULL CHECK(reference_price_idr>0),
 currency CHAR(3) NOT NULL DEFAULT 'IDR' CHECK(currency='IDR'),
 simulated_available_from DATE NOT NULL,
 simulated_available_until DATE NOT NULL,
 price_source TEXT NOT NULL,
 price_observed_date DATE NOT NULL,
 price_basis TEXT NOT NULL,
 price_source_url TEXT NOT NULL,
 price_notes TEXT NOT NULL,
 CHECK(simulated_available_until>=simulated_available_from)
);
CREATE TABLE IF NOT EXISTS apple_retail_id.campaigns (
 campaign_id TEXT PRIMARY KEY,
 campaign_name TEXT NOT NULL,
 start_date DATE NOT NULL,
 end_date DATE NOT NULL,
 max_discount_pct INT NOT NULL CHECK(max_discount_pct BETWEEN 0 AND 100),
 scope TEXT NOT NULL,
 data_origin TEXT NOT NULL,
 CHECK(end_date>=start_date)
);
CREATE TABLE IF NOT EXISTS apple_retail_id.sales (
 sale_id TEXT PRIMARY KEY,
 sale_date DATE NOT NULL,
 store_id TEXT NOT NULL REFERENCES apple_retail_id.stores(store_id),
 product_id TEXT NOT NULL REFERENCES apple_retail_id.products(product_id),
 quantity INT NOT NULL CHECK(quantity>0),
 unit_price_idr BIGINT NOT NULL CHECK(unit_price_idr>0),
 discount_pct INT NOT NULL CHECK(discount_pct BETWEEN 0 AND 100),
 gross_amount_idr BIGINT NOT NULL CHECK(gross_amount_idr>=0),
 discount_amount_idr BIGINT NOT NULL CHECK(discount_amount_idr>=0),
 net_amount_idr BIGINT NOT NULL CHECK(net_amount_idr>=0),
 payment_method TEXT NOT NULL,
 sales_channel TEXT NOT NULL,
 campaign_id TEXT NULL REFERENCES apple_retail_id.campaigns(campaign_id),
 sale_status TEXT NOT NULL,
 CHECK(gross_amount_idr=quantity*unit_price_idr),
 CHECK(net_amount_idr=gross_amount_idr-discount_amount_idr)
);
CREATE TABLE IF NOT EXISTS apple_retail_id.warranty (
 claim_id TEXT PRIMARY KEY,
 claim_date DATE NOT NULL,
 sale_id TEXT NOT NULL REFERENCES apple_retail_id.sales(sale_id),
 claim_type TEXT NOT NULL,
 repair_status TEXT NOT NULL,
 resolution_days INT NULL CHECK(resolution_days>=0),
 record_origin TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS apple_retail_id.daily_product_sales (
 date DATE NOT NULL,
 store_id TEXT NOT NULL REFERENCES apple_retail_id.stores(store_id),
 product_id TEXT NOT NULL REFERENCES apple_retail_id.products(product_id),
 units_sold INT NOT NULL CHECK(units_sold>=0),
 transaction_count INT NOT NULL CHECK(transaction_count>=0),
 gross_revenue_idr BIGINT NOT NULL CHECK(gross_revenue_idr>=0),
 discount_total_idr BIGINT NOT NULL CHECK(discount_total_idr>=0),
 net_revenue_idr BIGINT NOT NULL CHECK(net_revenue_idr>=0),
 campaign_active INT NOT NULL CHECK(campaign_active IN (0,1)),
 PRIMARY KEY(date,store_id,product_id),
 CHECK(net_revenue_idr=gross_revenue_idr-discount_total_idr)
);
CREATE INDEX IF NOT EXISTS sales_date_idx ON apple_retail_id.sales(sale_date);
CREATE INDEX IF NOT EXISTS sales_product_date_idx ON apple_retail_id.sales(product_id,sale_date);
CREATE INDEX IF NOT EXISTS sales_store_date_idx ON apple_retail_id.sales(store_id,sale_date);
CREATE INDEX IF NOT EXISTS claim_sale_idx ON apple_retail_id.warranty(sale_id);

CREATE OR REPLACE VIEW apple_retail_id.vw_sales_detail AS
 SELECT s.sale_id,s.sale_date,s.store_id,st.city,st.province,st.region,
        s.product_id,p.product_name,c.category_name,s.quantity,s.unit_price_idr,
        s.discount_amount_idr,s.gross_amount_idr,s.net_amount_idr,
        s.payment_method,s.sales_channel,s.campaign_id
 FROM apple_retail_id.sales s
 JOIN apple_retail_id.products p USING(product_id)
 JOIN apple_retail_id.category c USING(category_id)
 JOIN apple_retail_id.stores st USING(store_id);

CREATE OR REPLACE VIEW apple_retail_id.vw_forecast_daily AS
 SELECT d.date,d.store_id,st.city,st.province,d.product_id,p.product_name,
        c.category_name,d.units_sold,d.transaction_count,d.net_revenue_idr,
        d.campaign_active,EXTRACT(DOW FROM d.date)::INT AS day_of_week,
        EXTRACT(MONTH FROM d.date)::INT AS month_of_year
 FROM apple_retail_id.daily_product_sales d
 JOIN apple_retail_id.products p USING(product_id)
 JOIN apple_retail_id.category c USING(category_id)
 JOIN apple_retail_id.stores st USING(store_id);
