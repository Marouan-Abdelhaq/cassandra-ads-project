from cassandra.cluster import Cluster
from collections import Counter

cluster = Cluster(['127.0.0.1'])
session = cluster.connect('ads')

rows = session.execute("""
    SELECT ad_id, clicks
    FROM clicks_by_campaign_ad
    WHERE campaign_id = %s
""", ("C1",))

# Trier par nombre de clics décroissant
top_ads = sorted(rows, key=lambda r: r.clicks, reverse=True)[:5]

print("Top 5 annonces par clics :")
for ad in top_ads:
    print(ad.ad_id, ad.clicks)

