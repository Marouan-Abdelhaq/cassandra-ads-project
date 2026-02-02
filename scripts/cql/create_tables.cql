CREATE TABLE events_by_campaign_day (
	campaign_id text,
	event_date date,
	event_time timestamp,
	ad_id text,
	placement text,
	event_type text,
	cost decimal,
	PRIMARY KEY (campaign_id, event_date, event_time, ad_id)
) WITH CLUSTERING ORDER BY (
	event_date DESC,
	event_time DESC
);

CREATE TABLE clicks_by_campaign_ad (
	 campaign_id text,
	ad_id text,
	clicks counter,
	PRIMARY KEY (campaign_id, ad_id)
);

CREATE TABLE impressions_by_campaign_ad (
	campaign_id text,
	ad_id text,
	impressions counter,
	PRIMARY KEY (campaign_id, ad_id)
);
