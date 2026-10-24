-- 1. Verify loaded record counts
SELECT 'products' AS tabel, COUNT(*) FROM apple_retail_id.products
UNION ALL SELECT 'stores',COUNT(*) FROM apple_retail_id.stores
UNION ALL SELECT 'sales',COUNT(*) FROM apple_retail_id.sales
UNION ALL SELECT 'daily_product_sales',COUNT(*) FROM apple_retail_id.daily_product_sales
UNION ALL SELECT 'warranty',COUNT(*) FROM apple_retail_id.warranty;

-- 2. Penjualan menurut kategori (synthetic revenue)
SELECT category_name, SUM(quantity) AS units_sold, SUM(net_amount_idr) AS revenue_idr
FROM apple_retail_id.vw_sales_detail
GROUP BY category_name ORDER BY revenue_idr DESC;

-- 3. Daily trend, zero sales included (Data Science friendly)
SELECT date,SUM(units_sold) AS units_sold,SUM(net_revenue_idr) AS revenue_idr
FROM apple_retail_id.daily_product_sales
GROUP BY date ORDER BY date;

-- 4. Top regions
SELECT region, SUM(quantity) AS units_sold, SUM(net_amount_idr) AS revenue_idr
FROM apple_retail_id.vw_sales_detail GROUP BY region ORDER BY revenue_idr DESC;

-- 5. Baseline model data at product+date grain
SELECT date,product_id,SUM(units_sold) AS units_sold,SUM(campaign_active) AS stores_with_campaign
FROM apple_retail_id.daily_product_sales GROUP BY date,product_id ORDER BY date,product_id;

-- 6. Check that daily panel matches sales (must return zero rows)
WITH source AS (
 SELECT sale_date AS date,store_id,product_id,SUM(quantity) AS units,SUM(net_amount_idr) AS revenue
 FROM apple_retail_id.sales GROUP BY 1,2,3
)
SELECT d.date,d.store_id,d.product_id
FROM apple_retail_id.daily_product_sales d
LEFT JOIN source s USING(date,store_id,product_id)
WHERE d.units_sold<>COALESCE(s.units,0) OR d.net_revenue_idr<>COALESCE(s.revenue,0);
