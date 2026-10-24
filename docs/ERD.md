# ERD — Apple Retail Indonesia (Simulasi)

```mermaid
erDiagram
    CATEGORY ||--o{ PRODUCTS : contains
    STORES ||--o{ SALES : records
    PRODUCTS ||--o{ SALES : sold_in
    CAMPAIGNS o|--o{ SALES : applied_to
    SALES ||--o{ WARRANTY : claimed_for
    STORES ||--o{ DAILY_PRODUCT_SALES : aggregates
    PRODUCTS ||--o{ DAILY_PRODUCT_SALES : aggregates

    CATEGORY {
      text category_id PK
      text category_name
    }
    PRODUCTS {
      text product_id PK
      text category_id FK
      bigint reference_price_idr
      date simulated_available_from
      text price_source_url
    }
    STORES {
      text store_id PK
      text city
      text province
      numeric simulated_traffic_index
    }
    CAMPAIGNS {
      text campaign_id PK
      date start_date
      date end_date
      int max_discount_pct
    }
    SALES {
      text sale_id PK
      date sale_date
      text store_id FK
      text product_id FK
      text campaign_id FK
      int quantity
      bigint net_amount_idr
    }
    WARRANTY {
      text claim_id PK
      text sale_id FK
      date claim_date
    }
    DAILY_PRODUCT_SALES {
      date date PK
      text store_id PK_FK
      text product_id PK_FK
      int units_sold
      int transaction_count
    }
```

## Granularity

- `sales`: **one simulated retail sale event of a single product**, quantity may be 1–3; `sale_id` unique.
- `daily_product_sales`: **one date × store × product** *within simulated availability*; includes zeros to prevent ML survivorship bias. Primary key (`date`, `store_id`, `product_id`).
- `warranty`: **one claim** linked to a valid sale; many possible claims to a sale, simulation currently <=1.
- `products`: one model/reference base variant, not full SKU inventory by color/storage.
- `stores`: a fictional retail network whose cities and provinces are real Indonesian locations.

Campaigns are conceptual synthetic promotions; only some sales during a campaign have a campaign ID. `campaign_active` means a campaign period exists for that date, not that every sale received a discount.
