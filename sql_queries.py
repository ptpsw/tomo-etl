# Drop tables
station_table_drop = "DROP TABLE IF EXISTS stations;"
station_link_table_drop = "DROP TABLE IF EXISTS station_links;"
max_snr_table_drop = "DROP TABLE IF EXISTS max_snr;"
temp_table_drop = "DROP TABLE IF EXISTS temperature;"
current_table_drop = "DROP TABLE IF EXISTS current;"

# Create tables
station_table_create = """
CREATE TABLE IF NOT EXISTS stations (
    station_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(50),
    lat FLOAT,
    lon FLOAT
);
"""
station_link_table_create = """
CREATE TABLE IF NOT EXISTS station_links (
    link_id INT PRIMARY KEY AUTO_INCREMENT,
    link_name VARCHAR(50),
    source_station_id INT,
    dest_station_id INT,
    FOREIGN KEY (source_station_id) REFERENCES stations(station_id) ON DELETE CASCADE,
    FOREIGN KEY (dest_station_id) REFERENCES stations(station_id) ON DELETE CASCADE
);
"""
max_snr_table_create = """
CREATE TABLE max_snr (
    station_id INT NOT NULL, 
    timestamp DATETIME NOT NULL,
    value FLOAT,
    FOREIGN KEY (station_id) REFERENCES stations(station_id) ON DELETE CASCADE
); 
"""
temp_table_create = """
CREATE TABLE temperature (
    station_link_id INT,
    timestamp DATETIME,
    value FLOAT,
    FOREIGN KEY (station_link_id) REFERENCES station_links(link_id) ON DELETE CASCADE
);
"""
current_table_create = """
CREATE TABLE IF NOT EXISTS current (
    station_link_id INT,
    timestamp DATETIME,
    value FLOAT,
    direction FLOAT,
    FOREIGN KEY (station_link_id) REFERENCES station_links(link_id) ON DELETE CASCADE
)
"""

# Insert queries
max_snr_table_insert = """
"""
temp_table_insert = """
"""
current_table_insert = """
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