CREATE KEYSPACE ads
WITH replication = {
	’class’: ’SimpleStrategy’,
	’replication_factor’: 1
};
