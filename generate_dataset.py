#!/usr/bin/env python3
"""Reproducible synthetic Indonesian Apple retail case study; Python stdlib only.
Pricing anchors are observed advertised starting prices from Digimap Indonesia around 2026-10-25.
NOT real orders, not real store sales, not historical realized price observations.
"""
from pathlib import Path
import csv, random, math, datetime as dt, json, collections
from decimal import Decimal, ROUND_HALF_UP

ROOT=Path(__file__).resolve().parent
OUT=ROOT/'csv'; OUT.mkdir(exist_ok=True)
SEED=20261025
R=random.Random(SEED)
START=dt.date(2024,1,1); END=dt.date(2026,9,30)
PRICE_OBSERVED='2026-10-25'

def file_write(name, header, rows):
    with (OUT/name).open('w',encoding='utf-8',newline='') as f:
        w=csv.writer(f); w.writerow(header); w.writerows(rows)

def dateparse(s):return dt.date.fromisoformat(s)

categories=[('CAT-01','iPhone'),('CAT-02','Mac'),('CAT-03','iPad'),('CAT-04','Apple Watch'),('CAT-05','AirPods')]
file_write('category.csv',['category_id','category_name'],categories)
# Retail reference price for ONE base model/configuration per row where possible.
# Collection 'mulai dari' prices are not guaranteed prices for every storage/color/region variant.
prod=[
# id, name, category, variant, price, available_from, available_to, source URL, basis, relative demand
('APL-001','iPhone 15','CAT-01','128GB (model dasar)',12499000,'2024-01-01','2026-09-30','https://www.digimap.co.id/collections/iphone-15','harga_mulai_dari',1.08),
('APL-002','iPhone 16','CAT-01','128GB (model dasar)',14999000,'2025-04-11','2026-09-30','https://www.digimap.co.id/collections/iphone-16','harga_mulai_dari',1.38),
('APL-003','iPhone 16 Plus','CAT-01','128GB (model dasar)',15999000,'2025-04-11','2026-09-30','https://www.digimap.co.id/collections/iphone-16','harga_mulai_dari',0.66),
('APL-004','iPhone 16 Pro','CAT-01','128GB (model dasar)',15499000,'2025-04-11','2026-09-30','https://www.digimap.co.id/products/iphone-16-pro-7','harga_varian_tercantum',0.85),
('APL-005','iPhone 16 Pro Max','CAT-01','256GB (model dasar)',20499000,'2025-04-11','2026-09-30','https://www.digimap.co.id/collections/iphone-16-pro','harga_mulai_dari',0.74),
('APL-006','iPhone 16e','CAT-01','128GB (model dasar)',8999000,'2025-04-11','2026-09-30','https://www.digimap.co.id/collections/iphone-16','harga_menu_iphone',0.78),
('APL-007','iPhone 17','CAT-01','256GB (model dasar)',19999000,'2025-10-17','2026-09-30','https://www.digimap.co.id/collections/iphone-complete-collection?page=1','harga_varian_tercantum',1.16),
('APL-008','iPhone 17 Pro','CAT-01','256GB (model dasar)',22999000,'2025-10-17','2026-09-30','https://www.digimap.co.id/collections/iphone-complete-collection?page=1','harga_varian_tercantum',0.75),
('APL-009','MacBook Air 13 M1','CAT-02','8GB/256GB (asumsi konfigurasi dasar)',9999000,'2024-01-01','2025-12-31','https://www.digimap.co.id/collections/macbook-air','harga_mulai_dari',0.40),
('APL-010','MacBook Air 13 M2','CAT-02','8GB/256GB (asumsi konfigurasi dasar)',13499000,'2024-01-01','2026-09-30','https://www.digimap.co.id/collections/macbook-air','harga_mulai_dari',0.59),
('APL-011','MacBook Air 13 M3','CAT-02','8GB/256GB (asumsi konfigurasi dasar)',13499000,'2024-06-01','2026-09-30','https://www.digimap.co.id/collections/macbook-air','harga_mulai_dari',0.53),
('APL-012','MacBook Air 13 M4','CAT-02','16GB/256GB (model dasar)',15999000,'2025-05-01','2026-09-30','https://www.digimap.co.id/collections/macbook-air','harga_mulai_dari',0.71),
('APL-013','MacBook Air 15 M4','CAT-02','16GB/256GB (model dasar)',19499000,'2025-05-01','2026-09-30','https://www.digimap.co.id/collections/macbook-air','harga_mulai_dari',0.46),
('APL-014','Mac mini M4','CAT-02','16GB/256GB (asumsi konfigurasi dasar)',9999000,'2025-01-01','2026-09-30','https://www.digimap.co.id/collections/mac-mini','harga_mulai_dari',0.37),
('APL-015','iPad Gen 10','CAT-03','Wi-Fi 64GB (model dasar)',4499000,'2024-01-01','2026-09-30','https://www.digimap.co.id/collections/ipad','harga_mulai_dari',0.80),
('APL-016','iPad A16 (Gen 11)','CAT-03','Wi-Fi 128GB (asumsi konfigurasi dasar)',8699000,'2025-05-01','2026-09-30','https://www.digimap.co.id/products/2025-ipad-22','harga_varian_tercantum',0.89),
('APL-017','iPad Air 11 M3','CAT-03','Wi-Fi konfigurasi dasar',10749000,'2025-05-01','2026-09-30','https://www.digimap.co.id/collections/ipad','harga_mulai_dari',0.61),
('APL-018','iPad Air 13 M3','CAT-03','Wi-Fi konfigurasi dasar',14149000,'2025-05-01','2026-09-30','https://www.digimap.co.id/collections/ipad','harga_mulai_dari',0.31),
('APL-019','Apple Watch Series 10','CAT-04','Sport Band, GPS (model dasar)',4499000,'2025-01-01','2026-09-30','https://www.digimap.co.id/collections/apple-watch-series-10','harga_mulai_dari',0.76),
('APL-020','Apple Watch Series 11','CAT-04','GPS (model dasar)',6799000,'2025-11-01','2026-09-30','https://www.digimap.co.id/pages/view-all-watch','harga_mulai_dari',0.74),
('APL-021','AirPods 4','CAT-05','tanpa ANC',2299000,'2025-01-01','2026-09-30','https://www.digimap.co.id/products/airpods-4','harga_varian_tercantum',1.53),
('APL-022','AirPods 4 ANC','CAT-05','Active Noise Cancellation',3099000,'2025-01-01','2026-09-30','https://www.digimap.co.id/products/airpods-4-active-noise-cancellation','harga_varian_tercantum',1.12),
('APL-023','AirPods Pro 2','CAT-05','USB-C / generasi 2 (asumsi)',3699000,'2024-01-01','2026-09-30','https://www.digimap.co.id/collections/airpods-4','harga_menu_apple',0.93),
('APL-024','AirPods 2','CAT-05','generasi 2',1499000,'2024-01-01','2026-09-30','https://www.digimap.co.id/collections/airpods-4','harga_menu_apple',0.85),
]
# availability dates are CONSERVATIVE synthetic start rules (only iPhone 16/17 Apple-ID confirmed launch dates).
products=[]
for pid,name,cat,variant,price,start,end,url,basis,weight in prod:
    products.append((pid,name,cat,variant,price,'IDR',start,end,'Digimap Indonesia',PRICE_OBSERVED,basis,url,'harga referensi 2026 bukan harga historis transaksi'))
file_write('products.csv',['product_id','product_name','category_id','variant_description','reference_price_idr','currency','simulated_available_from','simulated_available_until','price_source','price_observed_date','price_basis','price_source_url','price_notes'], products)
file_write('price_sources.csv',['product_id','product_name','reference_price_idr','currency','source_name','price_observed_date','price_basis','source_url'],[(r[0],r[1],r[4],'IDR','Digimap Indonesia',PRICE_OBSERVED,r[10],r[11]) for r in products])

city_specs=[
 ('Jakarta Selatan','DKI Jakarta','Jawa',1.45),('Jakarta Pusat','DKI Jakarta','Jawa',1.48),('Jakarta Barat','DKI Jakarta','Jawa',1.36),('Tangerang Selatan','Banten','Jawa',1.28),('Tangerang','Banten','Jawa',1.10),('Bekasi','Jawa Barat','Jawa',1.12),('Depok','Jawa Barat','Jawa',0.96),('Bandung','Jawa Barat','Jawa',1.19),('Bogor','Jawa Barat','Jawa',0.99),('Semarang','Jawa Tengah','Jawa',1.03),('Surakarta','Jawa Tengah','Jawa',0.82),('Yogyakarta','DI Yogyakarta','Jawa',1.02),('Surabaya','Jawa Timur','Jawa',1.35),('Malang','Jawa Timur','Jawa',0.96),('Denpasar','Bali','Bali Nusa Tenggara',1.13),('Mataram','Nusa Tenggara Barat','Bali Nusa Tenggara',0.78),('Makassar','Sulawesi Selatan','Sulawesi',1.10),('Gowa','Sulawesi Selatan','Sulawesi',0.71),('Manado','Sulawesi Utara','Sulawesi',0.82),('Balikpapan','Kalimantan Timur','Kalimantan',0.93),('Samarinda','Kalimantan Timur','Kalimantan',0.87),('Pontianak','Kalimantan Barat','Kalimantan',0.78),('Banjarmasin','Kalimantan Selatan','Kalimantan',0.75),('Medan','Sumatera Utara','Sumatera',1.22),('Palembang','Sumatera Selatan','Sumatera',0.86),('Pekanbaru','Riau','Sumatera',0.90),('Padang','Sumatera Barat','Sumatera',0.74),('Batam','Kepulauan Riau','Sumatera',1.05),('Lampung','Lampung','Sumatera',0.80),('Jayapura','Papua','Maluku Papua',0.66),
]
stores=[]
for i,(city,prov,reg,weight) in enumerate(city_specs,1):
    opening='2024-01-01' if i<=25 else '2025-01-01'
    stores.append((f'ST-{i:03}',f'Nusantara Digital Simulasi - {city}',city,prov,'Indonesia',reg,'Mitra Ritel Fiktif',opening,round(weight,2)))
file_write('stores.csv',['store_id','store_name','city','province','country','region','store_type','simulated_opening_date','simulated_traffic_index'],stores)

campaigns=[]
for y in [2024,2025,2026]:
    for name,a,b,disc in [
      ('Promo Awal Tahun',f'{y}-01-10',f'{y}-01-15',5),
      ('Promo Tengah Tahun',f'{y}-06-15',f'{y}-06-21',7),
      ('Promo Kemerdekaan',f'{y}-08-14',f'{y}-08-18',6),
      ('Harbolnas 11.11',f'{y}-11-09',f'{y}-11-12',9),
      ('Harbolnas 12.12',f'{y}-12-10',f'{y}-12-13',10),
    ]:
        if dateparse(a)>END:continue
        campaigns.append((f'PR-{len(campaigns)+1:03}',name,a,b,disc,'Semua kategori','PROMOSI SINTETIS: tanggal dan discount adalah asumsi simulasi'))
file_write('campaigns.csv',['campaign_id','campaign_name','start_date','end_date','max_discount_pct','scope','data_origin'], campaigns)
campaign_dates={}
for cid,nam,s,e,pct,scope,note in campaigns:
    d=dateparse(s)
    while d<=min(dateparse(e),END):
        campaign_dates[d]=(cid,pct); d+=dt.timedelta(days=1)

payments=['Kartu Kredit','Kartu Debit','Transfer Bank','QRIS','E-Wallet','Paylater']
channels=['Offline','Online']
statuses=['Selesai','Dalam Proses','Menunggu Sparepart','Ditolak']
# Full zero-filled daily panel for ML while transaction-level sales are sparse and plausible.
header_sales=['sale_id','sale_date','store_id','product_id','quantity','unit_price_idr','discount_pct','gross_amount_idr','discount_amount_idr','net_amount_idr','payment_method','sales_channel','campaign_id','sale_status']
header_daily=['date','store_id','product_id','units_sold','transaction_count','gross_revenue_idr','discount_total_idr','net_revenue_idr','campaign_active']
header_warranty=['claim_id','claim_date','sale_id','claim_type','repair_status','resolution_days','record_origin']
salesfile=(OUT/'sales.csv').open('w',encoding='utf-8',newline=''); sw=csv.writer(salesfile);sw.writerow(header_sales)
dailyfile=(OUT/'daily_product_sales.csv').open('w',encoding='utf-8',newline='');dw=csv.writer(dailyfile);dw.writerow(header_daily)
warrantyfile=(OUT/'warranty.csv').open('w',encoding='utf-8',newline='');ww=csv.writer(warrantyfile);ww.writerow(header_warranty)
sale_ct=0; daily_ct=0; claim_ct=0; total_units=0; total_revenue=0; discount_sum=0; by_cat=collections.Counter()
product_meta=[(p[0],p[2],p[4],dateparse(p[5]),dateparse(p[6]),p[9]) for p in prod]
category_weights={'CAT-01':.48,'CAT-02':.14,'CAT-03':.22,'CAT-04':.32,'CAT-05':.57}
# Base daily transaction expectation per store x product; trained models may explore day-of-week,
# store, product, campaign, year-end, release ramp, and small stochastic noise.
for dayoffset in range((END-START).days+1):
    d=START+dt.timedelta(days=dayoffset)
    payday=(d.day>=25 or d.day<=3)
    weekend=d.weekday()>=5
    yearend=d.month in (11,12)
    july=d.month==7
    campaign=campaign_dates.get(d)
    cyc=1+.12*math.sin(2*math.pi*(d.timetuple().tm_yday-50)/365.25)
    season=(1.21 if yearend else 1.0)*(1.08 if july else 1.0)*(1.13 if payday else 1.0)*(1.17 if weekend else 1.0)*cyc
    for store_id,store_name,city,province,country,region,typ,opening,traffic in stores:
        if d<dateparse(opening):continue
        for pid,cat,price,avail,retired,product_weight in product_meta:
            if not(avail<=d<=retired):continue
            active_days=(d-avail).days
            launch_effect=1.55 if active_days<32 else (1.18 if active_days<100 else 1.0)
            # no synthetic claim of true market trend; intentional nonstationarity
            growth=1+0.09*((d-START).days/365)
            lam=category_weights[cat]*traffic*product_weight*season*launch_effect*growth
            if campaign:lam*=1.23
            if R.random()<.012:lam*=1.9  # irregular local spikes
            # Poisson via fast approx for common rate (<2) using Knuth exact method
            left=math.exp(-lam); events=0; mult=1.0
            while True:
                mult*=R.random()
                if mult<=left:break
                events+=1
            units=0; gross=0; discount=0; revenue=0
            for e in range(events):
                q=1 if R.random()<.88 else (2 if R.random()<.93 else 3)
                # card/transfer favored for higher-ticket purchases
                chosen_payment=R.choices(payments,weights=[39,23,18,8,6,6],k=1)[0]
                base_discount=0
                cid=''
                if campaign and R.random()<.65:
                    cid=campaign[0];base_discount=campaign[1]
                elif R.random()<.12:base_discount=3
                elif R.random()<.045:base_discount=5
                gr=price*q
                disc=int((Decimal(gr)*Decimal(base_discount)/Decimal(100)/Decimal(1000)).quantize(Decimal('1'),rounding=ROUND_HALF_UP))*1000
                net=gr-disc
                if chosen_payment=='QRIS' and net>10000000:chosen_payment='Transfer Bank'
                sale_ct+=1
                sw.writerow((f'SALE-{sale_ct:08}',d.isoformat(),store_id,pid,q,price,base_discount,gr,disc,net,chosen_payment,R.choices(channels,weights=[64,36])[0],cid,'Selesai'))
                units+=q;gross+=gr;discount+=disc;revenue+=net
                if R.random()<.021:
                    lag=R.randint(10,330)
                    claim_date=d+dt.timedelta(days=lag)
                    if claim_date<=END:
                        claim_ct+=1
                        claim_status=R.choices(statuses,weights=[75,11,8,6],k=1)[0]
                        resolution=R.randint(2,20) if claim_status=='Selesai' else ''
                        ww.writerow((f'CL-{claim_ct:07}',claim_date.isoformat(),f'SALE-{sale_ct:08}',R.choice(['Baterai','Layar','Konektivitas','Audio','Lainnya']),claim_status,resolution,'klaim_simulasi'))
            daily_ct+=1
            dw.writerow((d.isoformat(),store_id,pid,units,events,gross,discount,revenue,int(campaign is not None)))
            total_units+=units;total_revenue+=revenue;discount_sum+=discount;by_cat[cat]+=units
salesfile.close();dailyfile.close();warrantyfile.close()
metadata={
 'name':'Apple Retail Indonesia - Synthetic Data Science Case Study',
 'generated_on':dt.date.today().isoformat(),
 'seed':SEED,'history_start':START.isoformat(),'history_end':END.isoformat(),
 'currency':'IDR','price_reference_observed_date':PRICE_OBSERVED,
 'price_reference_type':'advertised retailer catalog/starting price anchor; not actual historical realized sales prices',
 'sale_data_type':'fully synthetic; not Apple/Digimap actual transactions',
 'store_data_type':'fictional store network (city/province are real places)',
 'historical_prices_are_simulated':True,
 'rows':{'category.csv':len(categories),'products.csv':len(products),'stores.csv':len(stores),'campaigns.csv':len(campaigns),'sales.csv':sale_ct,'daily_product_sales.csv':daily_ct,'warranty.csv':claim_ct,'price_sources.csv':len(products)},
 'total_units':total_units,'net_revenue_idr':total_revenue,'total_discount_idr':discount_sum,
 'notes':['Calendar-based campaign and store opening dates are synthetic assumptions.','Dates for iPhone 16 and 17 availability are sourced from Apple Indonesia; most others conservatively simulated.','Sourced October 2026 catalog prices should NOT be interpreted as actual 2024 or 2025 market prices.','Customer data and store identities are deliberately not copied from real people/retail chains.'],
 'original_zip_name':'apple-retail-sales-dataset(1).zip',
 'original_counts':{'category.csv':10,'products.csv':89,'sales.csv':1040200,'stores.csv':75,'warranty.csv':30000},
}
(ROOT/'metadata.json').write_text(json.dumps(metadata,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(metadata['rows'],indent=2));print('units',total_units,'net',total_revenue)
