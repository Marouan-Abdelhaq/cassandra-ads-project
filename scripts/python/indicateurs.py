from cassandra.cluster import Cluster

cluster = Cluster(['127.0.0.1'])
session = cluster.connect('ads')

campaign_id = "C1"

# Récupérer clics
clicks = session.execute("""
    SELECT ad_id, clicks FROM clicks_by_campaign_ad
    WHERE campaign_id = %s
""", (campaign_id,))

# Récupérer impressions
impressions = session.execute("""
    SELECT ad_id, impressions FROM impressions_by_campaign_ad
    WHERE campaign_id = %s
""", (campaign_id,))

# Récupérer coût total
costs = session.execute("""
    SELECT cost FROM events_by_campaign_day
    WHERE campaign_id = %s
      AND event_date = '2026-01-15'
""", (campaign_id,))

total_cost = sum([row.cost for row in costs])

# Calcul indicateurs par annonce
impressions_dict = {row.ad_id: row.impressions for row in impressions}
clicks_dict = {row.ad_id: row.clicks for row in clicks}

for ad_id in clicks_dict:
    c = clicks_dict.get(ad_id, 0)
    i = impressions_dict.get(ad_id, 0)
    ctr = c / i if i > 0 else 0
    cpc = total_cost / c if c > 0 else 0
    print(f"Annonce {ad_id} → CTR={ctr:.2f}, CPC={cpc:.2f}, Coût total={total_cost:.2f}")

