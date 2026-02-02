import random
import datetime
from cassandra.cluster import Cluster

# Connexion au cluster Cassandra
cluster = Cluster(['127.0.0.1'])   # adapte l'adresse si nécessaire
session = cluster.connect()

# Sélection du keyspace
session.set_keyspace('ads')

# Listes de campagnes et annonces fictives
campaigns = [f"C{i}" for i in range(1, 6)]   # C1 → C5
ads = [f"A{i}" for i in range(1, 21)]        # A1 → A20
placements = ["instagram", "facebook", "google"]

# G
for i in range(100000):
    campaign_id = random.choice(campaigns)
    ad_id = random.choice(ads)
    placement = random.choice(placements)

    day = random.randint(1, 30)
    event_date = datetime.date(2026, 1, day)
    event_time = datetime.datetime(2026, 1, day,
                                   random.randint(0, 23),
                                   random.randint(0, 59),
                                   random.randint(0, 59))

    event_type = random.choice(["impression", "click"])
    cost = 0.01 if event_type == "impression" else 0.20

    session.execute("""
        INSERT INTO events_by_campaign_day (campaign_id, event_date, event_time, ad_id, placement, event_type, cost)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (campaign_id, event_date, event_time, ad_id, placement, event_type, cost))

    if event_type == "click":
        session.execute("""
            UPDATE clicks_by_campaign_ad SET clicks = clicks + 1
            WHERE campaign_id = %s AND ad_id = %s
        """, (campaign_id, ad_id))
    else:
        session.execute("""
            UPDATE impressions_by_campaign_ad SET impressions = impressions + 1
            WHERE campaign_id = %s AND ad_id = %s
        """, (campaign_id, ad_id))
