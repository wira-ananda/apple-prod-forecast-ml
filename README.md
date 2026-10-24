# Apple Retail Indonesia — Synthetic Analytics & Forecasting Dataset

**Version**: 1.0 (25 October 2026)  
**Language**: Indonesian context / English snake_case fields  
**Currency**: `IDR` (integer rupiah, no currency conversion)  
**Period**: 2024-01-01 to 2026-09-30  
**Scope**: Apple product retail *case study* in 30 **fictional** Indonesian outlets

> **IMPORTANT: NOT REAL APPLE SALES DATA.** All sales quantities, transactions, payments, discounts, warranty claims, and store identities are programmatically **synthetic**. Model names are real Apple products. `reference_price_idr` values are advertised price/reference anchors from Digimap Indonesia pages checked around 2026-10-25; they are **not** real historical transacted prices in 2024–2026 and could differ by variant, store, stock, sale period, and the time a website is viewed. Do not claim actual revenue or sales performance for Apple/Digimap from these data.

## What changed from the uploaded archive?

Original ZIP had 5 **non-empty** files: `category.csv` (10 rows), `products.csv` (89), `stores.csv` (75), `sales.csv` (1,040,200), `warranty.csv` (30,000). Product prices had unclear currencies and some `Launch_Date` values were historically inconsistent. Instead of blindly changing foreign cities/currency, this release generates a brand-new, referentially consistent synthetic Indonesian network, documented independently of the original transactions.

## Included files

| File | Grain / purpose |
|------|-----------------|
| csv/category.csv | 5 product groups |
| csv/products.csv | 24 Apple product configurations + reference list prices, price basis/source URL |
| csv/stores.csv | 30 fictional outlets in real Indonesian cities |
| csv/sales.csv | Synthetic transaction facts with IDR amounts, discounts, payment and channel |
| csv/warranty.csv | Synthetic service claims linked to sales |
| csv/campaigns.csv | Synthetic promotional calendar |
| csv/daily_product_sales.csv | **Zero-filled daily date×store×product** forecast-ready series |
| csv/price_sources.csv | Auditable Indonesia advertised prices for product catalog |
| csv/data_dictionary.csv | Column-by-column definitions |
| metadata.json | Scope, row counts, generator seed and caveats |
| docs/ERD.md | Mermaid ERD and facts granularity |
| docs/PRICE_REFERENCES.md | Price methodology and sources |
| sql/schema.sql | Safe schema creation: `apple_retail_id` (no drop/truncate) |
| sql/import_psql.sql | PostgreSQL CSV import statements |
| sql/analysis_examples.sql | SQL sample queries and integrity check |
| generate_dataset.py | Deterministic generation (stdlib Python 3) |
| validate_dataset.py | Multi-table referential and arithmetic validation |

## How to use with an EXISTING PostgreSQL Docker container (Mac)

**Do not alter your existing project database.** The following commands assume a *separate* container named `pg-tableau` and database `business_analytics` exist and run, created in previous setup. Commands never use DROP, delete a volume, or mutate another project's DB.

Open Terminal in the **unzipped project folder**:

```bash
# 1. Test isolated PostgreSQL container
docker exec pg-tableau psql -U analytics -d business_analytics -c 'SELECT current_database();'

# 2. Copy data (not old database contents) into a temporary path inside container
docker exec pg-tableau mkdir -p /tmp/apple_retail_id
docker cp csv/. pg-tableau:/tmp/apple_retail_id/

# 3. Create tables under dedicated schema named apple_retail_id
docker exec -i pg-tableau psql -v ON_ERROR_STOP=1 -U analytics -d business_analytics < sql/schema.sql

# 4. Import ONCE into empty tables. This could take a little time.
docker exec -i pg-tableau psql -v ON_ERROR_STOP=1 -U analytics -d business_analytics < sql/import_psql.sql

# 5. Inspect results
docker exec -i pg-tableau psql -v ON_ERROR_STOP=1 -U analytics -d business_analytics < sql/analysis_examples.sql
```

If you previously created `public.penjualan`, these steps **leave it unchanged**. Imported tables live in a new schema `apple_retail_id`.

**Tableau Desktop Free Edition:** connect to host `127.0.0.1`, port `55432`, database `business_analytics`, username `analytics`, password established for pg-tableau. On Data Source choose schema **`apple_retail_id`**, then `vw_sales_detail` or `vw_forecast_daily`. Driver may be requested by Tableau.

## Forecasting learning plan

1. Data understanding, audit data dictionary, inspect category/product/store keys.
2. SQL aggregations, joins, views and Tableau dashboards.
3. Python + Pandas EDA, daily zero handling, date encodings, lag and rolling windows.
4. Forecast **unit sales**, e.g. 14-day-ahead; use a *time-based* validation and rolling backtest.
5. Compare naive/seasonal-naive vs gradient boosting (XGBoost) or other baselines.
6. Report MAE and WAPE (watch division by zero) with performance by product and store.
7. Once model is sufficiently validated, serve forecasts via FastAPI and integrate a Next.js UI.

Do **not** randomly shuffle records before splitting training and validation. Do **not** use future sales/revenue or future warranty claims as forecast features. Promotion calendar is known by assumption but actual future campaigns would require confirmation in a real business. The synthetic generator embeds learnable patterns; excellent fit on simulation does not imply real-world forecasting accuracy.

## Rerun and inspect

```bash
python3 validate_dataset.py
python3 generate_dataset.py    # OVERWRITES generated CSVs using fixed seed
python3 validate_dataset.py
```

## Price provenance

For every product use `products.price_source_url` and `price_sources.csv`. Reference prices are **snapshots**, mostly starting/from prices shown on retailer pages, and **not Apple-set official national MSRP**. See `docs/PRICE_REFERENCES.md` for source details and verified iPhone Indonesia launch dates.
