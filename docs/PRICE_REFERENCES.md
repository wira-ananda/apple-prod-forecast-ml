# Indonesia Price References (checked 2026-10-25)

- Currency is IDR. No USD-to-IDR heuristic conversion is used.
- Product names, model families, and advertised **starting/listed prices** are taken from Digimap Indonesia, an Apple Authorized Reseller. See `csv/price_sources.csv` for the 24 row-by-row URLs and values.
- **Important limitation:** Catalog/collection pages frequently say **"Mulai dari"**; that does not prove an exact color/capacity price unless the specific selected product page shows the variant. `products.price_basis` labels whether a figure is displayed as a listed variant, a starting price, or a category-page menu price. Some variant descriptions are explicitly marked `asumsi`.
- A 2026-10-25 catalog price may represent a discount, end-of-life offer or limited-stock price. Historical 2024-2026 simulated transaction amounts use 2026 price anchors for convenience, **not observed historical prices**; these aren't a historical price dataset.
- Price URLs may change in the future. Do not claim this file is a current live price feed.

## Reference websites

- iPhone 15: https://www.digimap.co.id/collections/iphone-15
- iPhone 16: https://www.digimap.co.id/collections/iphone-16
- iPhone 16 Pro: https://www.digimap.co.id/products/iphone-16-pro-7
- iPhone 16 Pro Max: https://www.digimap.co.id/collections/iphone-16-pro
- iPhone 17 and iPhone 17 Pro variant cards: https://www.digimap.co.id/collections/iphone-complete-collection?page=1
- MacBook Air M1–M4: https://www.digimap.co.id/collections/macbook-air
- Mac mini M4: https://www.digimap.co.id/collections/mac-mini
- iPad: https://www.digimap.co.id/collections/ipad
- iPad A16 example: https://www.digimap.co.id/products/2025-ipad-22
- Apple Watch Series 10: https://www.digimap.co.id/collections/apple-watch-series-10
- Apple Watch Series 11: https://www.digimap.co.id/pages/view-all-watch
- AirPods 4: https://www.digimap.co.id/products/airpods-4
- AirPods 4 ANC: https://www.digimap.co.id/products/airpods-4-active-noise-cancellation
- AirPods Pro 2 / AirPods 2: https://www.digimap.co.id/collections/airpods-4

## Indonesian launch checks / timeline

- Apple Indonesia confirms **iPhone 16 line starts sale on 2025-04-11**: https://www.apple.com/id/newsroom/2025/03/iphone-16-lineup-available-from-11-April/
- Apple Indonesia confirms **iPhone 17 and iPhone Air line starts sale on 2025-10-17**: https://www.apple.com/id/newsroom/2025/10/customers-in-indonesia-can-pre-order-the-latest-iphone-models-beginning-friday/
- Apple Indonesia announced **MacBook Air M4 2025-03-05** and said Indonesia would receive it later, without fixing a date: https://www.apple.com/id/newsroom/2025/03/apple-introduces-the-new-macbook-air-with-the-m4-chip-and-a-sky-blue-color/
- Other product `simulated_available_from` values are conservative CASE STUDY assumptions, **not claimed official release dates**.

## Pricing / transaction interpretation

- `reference_price_idr` and `unit_price_idr` are catalog price anchors, **not seller profit and not consumer observed receipts**.
- `discount_pct`, `discount_amount_idr` and `net_amount_idr` are all synthetic. No actual Indonesian taxes, returns, shipping fees, wholesale procurement costs, profit margins or authorized-reseller turnover are modeled.
- `gross_amount_idr = quantity * unit_price_idr`, `net_amount_idr = gross_amount_idr - discount_amount_idr`. Promotion fields are synthetic and based on calendar events, not observed store campaigns.
