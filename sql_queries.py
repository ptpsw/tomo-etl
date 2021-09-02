# Drop tables
station_table_drop = "DROP TABLE IF EXISTS stations;"
station_link_table_drop = "DROP TABLE IF EXISTS station_links;"
max_snr_table_drop = "DROP TABLE IF EXISTS max_snr;"
temp_table_drop = "DROP TABLE IF EXISTS temperature;"
current_table_drop = "DROP TABLE IF EXISTS current;"

# Create tables
station_table_create = """
CREATE TABLE IF NOT EXISTS stations (
    station_id VARCHAR(10) PRIMARY KEY,
    name VARCHAR(50),
    lat FLOAT,
    lon FLOAT,
    l2_folder VARCHAR(50),
    l3_folder VARCHAR(50)
);
"""
station_link_table_create = """
CREATE TABLE IF NOT EXISTS station_links (
    link_id INT PRIMARY KEY AUTO_INCREMENT,
    link_name VARCHAR(50),
    source_station_id VARCHAR(10),
    dest_station_id VARCHAR(10),
    FOREIGN KEY (source_station_id) REFERENCES stations(station_id) ON DELETE CASCADE,
    FOREIGN KEY (dest_station_id) REFERENCES stations(station_id) ON DELETE CASCADE
);
"""
max_snr_table_create = """
CREATE TABLE max_snr (
    station_id VARCHAR(10) NOT NULL, 
    timestamp TIMESTAMP NOT NULL,
    value FLOAT,
    PRIMARY KEY(station_id, timestamp),
    FOREIGN KEY (station_id) REFERENCES stations(station_id) ON DELETE CASCADE
); 
"""
temp_table_create = """
CREATE TABLE temperature (
    station_link_id INT,
    timestamp TIMESTAMP,
    value FLOAT,
    PRIMARY KEY(station_link_id, timestamp),
    FOREIGN KEY (station_link_id) REFERENCES station_links(link_id) ON DELETE CASCADE
);
"""
current_table_create = """
CREATE TABLE IF NOT EXISTS current (
    station_link_id INT,
    timestamp TIMESTAMP,
    value FLOAT,
    direction FLOAT,
    PRIMARY KEY(station_link_id, timestamp),
    FOREIGN KEY (station_link_id) REFERENCES station_links(link_id) ON DELETE CASCADE
);
"""

# Insert queries
stations_table_insert = """
INSERT INTO stations (station_id, name, lat, lon, l2_folder, l3_folder)
VALUES (%s, %s, %s, %s, %s, %s) 
ON DUPLICATE KEY UPDATE name=VALUES(name), lat=VALUES(lat), lon=VALUES(lon),
    l2_folder=VALUES(l2_folder), l3_folder=VALUES(l3_folder);
"""

station_link_id_insert = """
INSERT INTO station_links (link_name, source_station_id, dest_station_id)
VALUES (%s, %s, %s)
ON DUPLICATE KEY UPDATE 
    link_name=VALUES(link_name), 
    source_station_id=VALUES(source_station_id),
    dest_station_id=VALUES(dest_station_id)
"""

max_snr_table_insert = """
INSERT INTO max_snr (station_id, timestamp, value)
VALUES (%s, %s, %s)
ON DUPLICATE KEY UPDATE value=VALUES(value);
"""

temp_table_insert = """
INSERT INTO temperature (station_link_id, timestamp, value)
VALUES (%s, %s, %s)
ON DUPLICATE KEY UPDATE station_link_id=station_link_id
"""

current_table_insert = """
"""

# Select queries
get_station_id_l2_sql = """
SELECT station_id FROM stations WHERE l2_folder=%s;
"""

get_station_id_l3_sql = """
SELECT station_id FROM stations WHERE l3_folder=%s;
"""

get_station_link_sql = """
SELECT link_id, link_name, source_station_id, dest_station_id
FROM station_links
WHERE 
    (source_station_id=%s AND dest_station_id=%s) OR
    (source_station_id=%s AND dest_station_id=%s);
"""

# Create tables with tables referenced by foreign key first
create_table_queries = [
    station_table_create,
    station_link_table_create, 
    max_snr_table_create, temp_table_create, current_table_create
]

# Drop tables with tables with foreign key first
drop_table_queries = [
    max_snr_table_drop, temp_table_drop, current_table_drop,
    station_link_table_drop, 
    station_table_drop
]