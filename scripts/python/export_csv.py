import csv
import datetime
from cassandra.cluster import Cluster

# Connexion au cluster Cassandra
cluster = Cluster(['127.0.0.1'])   # adapte l'adresse si nécessaire
session = cluster.connect('ads')

# Date du jour (export quotidien)
today = datetime.date.today().strftime("%Y-%m-%d")

# Exemple : campagne à exporter
campaign_id = "C1"

# Récupérer clics
clicks_rows = session.execute("""
    SELECT ad_id, clicks FROM clicks_by_campaign_ad
    WHERE campaign_id = %s
""", (campaign_id,))

# Récupérer impressions
impressions_rows = session.execute("""
    SELECT ad_id, impressions FROM impressions_by_campaign_ad
    WHERE campaign_id = %s
""", (campaign_id,))

# Récupérer coûts (sur la journée)
cost_rows = session.execute("""
    SELECT cost FROM events_by_campaign_day
    WHERE campaign_id = %s AND event_date = %s
""", (campaign_id, today))

total_cost = sum([row.cost for row in cost_rows])

# Transformer en dictionnaires pour accès rapide
clicks_dict = {row.ad_id: row.clicks for row in clicks_rows}
impressions_dict = {row.ad_id: row.impressions for row in impressions_rows}

ads_report = []
total_clicks = 0
total_impressions = 0

for ad_id in clicks_dict:
    c = clicks_dict.get(ad_id, 0)
    i = impressions_dict.get(ad_id, 0)
    ctr = c / i if i > 0 else 0
    cpc = total_cost / c if c > 0 else 0

    ads_report.append([campaign_id, ad_id, c, i, round(ctr, 4), round(cpc, 4), round(total_cost, 2)])
    total_clicks += c
    total_impressions += i

# Résumé global
global_ctr = total_clicks / total_impressions if total_impressions > 0 else 0
global_cpc = total_cost / total_clicks if total_clicks > 0 else 0

# Export en fichier CSV
filename = f"report_{campaign_id}_{today}.csv"
with open(filename, "w", newline="") as f:
    writer = csv.writer(f)
    # En-têtes
    writer.writerow(["campaign_id", "ad_id", "clicks", "impressions", "CTR", "CPC", "total_cost"])
    # Données par annonce
    writer.writerows(ads_report)
    # Ligne résumé global
    writer.writerow(["SUMMARY", "-", total_clicks, total_impressions, round(global_ctr, 4), round(global_cpc, 4), round(total_cost, 2)])

