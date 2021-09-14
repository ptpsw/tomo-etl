from datetime import datetime, timedelta
import os
import re
import sys
import pymysql.cursors
import pandas as pd
from sql_queries import *
from dotenv import load_dotenv

load_dotenv()

SDE_PRODUCT = "sde"
SDR_PRODUCT = "sdr"

def get_db_conn():
    conn = pymysql.connect(
        host=os.getenv("MYSQL_HOST"),
        port=int(os.getenv("MYSQL_PORT")),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASS"),
        database=os.getenv("MYSQL_DB")
    )
    cur = conn.cursor()
    return conn, cur

def close_db_conn(conn, cur):
    cur.close()
    conn.close()

def get_std_datetime(filename):
    return datetime.strptime(filename[1:16], '%y%m%d_%H_%M_%S')

def get_std_station_folder(filepath):
    return os.path.basename(os.path.dirname(filepath))

def day_decimal_to_timestamp(datetime, day_decimal_ser):
    timestamp_ser = pd.to_datetime(datetime.date()).value + day_decimal_ser%1*86400*1e9
    return pd.to_datetime(timestamp_ser, format='%Y-%m-%d %H:%M:%S')

def parse_date_by_os(str, format):
    if sys.platform == "win32":
        std_date = datetime.strptime(str, format.replace(':', '_'))
    else:
        std_date = datetime.strptime(str, format)
    return std_date

def process_sdr_file(conn, cur, filepath):
    head, tail = os.path.split(filepath)

    # eg: "0210906_01:00:26to0210906_00:50:25_SDR.csv"
    regex_date = '(?P<{}>[0-9]{{6}}_[0-9]{{2}}(:|_)[0-9]{{2}}(:|_)[0-9]{{2}})?'
    regex_sdr = re.compile('(?P<st1>[0-9])?' + regex_date.format("date_start") + 'to' +
                       '(?P<st2>[0-9])?' + regex_date.format("date_end") + '_SDR.csv')
    m = regex_sdr.match(tail)

    if(m.group("date_start") is None):
        raise ValueError("Can't get SDR product date")
        
    sdr_date = parse_date_by_os(m.group("date_start"), '%y%m%d_%H:%M:%S')
    sdr_folder = get_std_station_folder(filepath)

    result = cur.execute(get_station_id_l2_sql, (sdr_folder))
    if (result == 0):
        raise ValueError("Cannot get station_id from station folder:{}".format(sdr_folder))
    sdr_station, = cur.fetchone()

    sdr_data_df = pd.read_csv(filepath, sep=' ')
    sdr_data_df['date'] = str(sdr_date.date())
    sdr_data_df['timestamp'] = pd.to_datetime(sdr_data_df['date'] + ' ' + sdr_data_df['Time_day'])
    sdr_data_df['station'] = sdr_station

    for index, row in sdr_data_df[['station', 'timestamp', 'Max_SNR']].iterrows():
        cur.execute(sdr_table_insert, list(row))
        conn.commit()

def process_sde_file(conn, cur, filepath):
    head, tail = os.path.split(filepath)

    # eg: USL02 2210913_13:50:23 to 2210913_18:20:23 _SDE.csv
    regex_date = '(?P<{}>[0-9]{{6}}_[0-9]{{2}}(:|_)[0-9]{{2}}(:|_)[0-9]{{2}})?'
    regex_std = re.compile('(?P<stname>[A-Za-z0-9]{2,5})?( )?' + 
                           '(?P<st1>[0-9])?' + regex_date.format("date_start") + '( to )?' +
                           '(?P<st2>[0-9])?' + regex_date.format("date_end") + '( )?_SDE.csv')
    m = regex_std.match(tail)

    if(m.group("date_start") is None):
        raise ValueError("Can't get SDE product date")
        
    std_date = parse_date_by_os(m.group("date_start"), '%y%m%d_%H:%M:%S')
    std_folder = get_std_station_folder(filepath)

    result = cur.execute(get_station_id_l2_sql, (std_folder))
    if (result == 0):
        raise ValueError("Cannot get station_id from station folder:{}".format(std_folder))
    std_station, = cur.fetchone()

    std_data_df = pd.read_csv(filepath, sep=',')
    std_data_df['date'] = str(std_date.date())
    std_data_df['timestamp'] = pd.to_datetime(std_data_df['date'] + ' ' + std_data_df['df.Time_day'])
    std_data_df['station'] = std_station

    for index, row in std_data_df[['station', 'timestamp', 'df.std.esn']].iterrows():
        cur.execute(max_snr_table_insert, list(row))
        conn.commit()

def get_data_product(filepath):
    regex_std = re.compile('.*(_SDE|std).csv')
    regex_sdr = re.compile('.*(_SDR).csv')
    head, tail = os.path.split(filepath)

    if(regex_std.match(tail)):
        data_product = SDE_PRODUCT
    if(regex_sdr.match(tail)):
        data_product = SDR_PRODUCT

    return data_product

def process_file(filepath):
    conn, cur = get_db_conn()
    try:
        data_product = get_data_product(filepath)
        {
            SDE_PRODUCT: process_sde_file,
            SDR_PRODUCT: process_sdr_file
        }[data_product](conn, cur, filepath)
    finally:
        close_db_conn(conn, cur)
    
def main ():
    if len(sys.argv) > 1:
        filepath = sys.argv[1] 
    else:
        raise ValueError("Please enter file path to be processed")
    process_file(filepath)

if __name__ == "__main__":
    main()