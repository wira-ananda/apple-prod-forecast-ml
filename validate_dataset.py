#!/usr/bin/env python3
"""Integrity validation of generated CSVs (stdlib only, no database required)."""
from pathlib import Path
import csv,datetime as dt,collections,json
ROOT=Path(__file__).resolve().parent

def rows(fn):
 with (ROOT/'csv'/fn).open(encoding='utf-8',newline='') as fp:
  for row in csv.DictReader(fp):yield row

prods={r['product_id']:r for r in rows('products.csv')}
stores={r['store_id']:r for r in rows('stores.csv')}
categories={r['category_id'] for r in rows('category.csv')}
campaigns={r['campaign_id']:r for r in rows('campaigns.csv')}
assert len(prods)==24 and len(stores)==30 and len(categories)==5
assert all(p['category_id'] in categories and p['price_source_url'].startswith('https://') and p['currency']=='IDR' for p in prods.values())
assert all(s['country']=='Indonesia' for s in stores.values())
agg=collections.defaultdict(lambda:[0,0,0,0,0]);sale_dates={};tot=0; sales_count=0
for r in rows('sales.csv'):
 sales_count+=1
 sid=r['sale_id']; day=dt.date.fromisoformat(r['sale_date']);p=prods[r['product_id']];s=stores[r['store_id']]
 assert dt.date.fromisoformat(p['simulated_available_from'])<=day<=dt.date.fromisoformat(p['simulated_available_until']),sid
 assert day>=dt.date.fromisoformat(s['simulated_opening_date']),sid
 q=int(r['quantity']);price=int(r['unit_price_idr']);gross=int(r['gross_amount_idr']);disc=int(r['discount_amount_idr']);net=int(r['net_amount_idr'])
 assert price==int(p['reference_price_idr']) and gross==q*price and net==gross-disc and 0<=disc<=gross,sid
 assert r['sale_status']=='Selesai'
 assert r['payment_method']!='QRIS' or net<=10000000
 if r['campaign_id']:
  c=campaigns[r['campaign_id']]
  assert c['start_date']<=r['sale_date']<=c['end_date'] and int(r['discount_pct'])==int(c['max_discount_pct'])
 v=agg[(r['sale_date'],r['store_id'],r['product_id'])]
 v[0]+=q;v[1]+=1;v[2]+=gross;v[3]+=disc;v[4]+=net
 sale_dates[sid]=day
 tot+=net
assert sales_count==len(sale_dates)
count_daily=0
for r in rows('daily_product_sales.csv'):
 count_daily+=1
 key=(r['date'],r['store_id'],r['product_id'])
 expected=agg.pop(key,[0,0,0,0,0])
 actual=[int(r[k]) for k in ['units_sold','transaction_count','gross_revenue_idr','discount_total_idr','net_revenue_idr']]
 assert actual==expected,(key,actual,expected)
assert not agg, f'Sales have missing daily panel keys: {len(agg)}'
count_claim=0;claimed=set()
for r in rows('warranty.csv'):
 count_claim+=1
 assert r['sale_id'] in sale_dates
 assert dt.date.fromisoformat(r['claim_date'])>=sale_dates[r['sale_id']]
 assert r['sale_id'] not in claimed
 claimed.add(r['sale_id'])
m=json.loads((ROOT/'metadata.json').read_text(encoding='utf-8'))
assert count_daily==m['rows']['daily_product_sales.csv'] and sales_count==m['rows']['sales.csv'] and count_claim==m['rows']['warranty.csv'] and tot==m['net_revenue_idr']
print(f'VALIDATION PASSED: {len(prods)} products, {len(stores)} stores, {sales_count:,} sales, {count_daily:,} daily entries, {count_claim:,} claims; net Rp{tot:,}')
