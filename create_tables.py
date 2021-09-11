import os
import pymysql.cursors
from sql_queries import *
from dotenv import load_dotenv

load_dotenv()

def create_tables (cur, conn):
    for query in create_table_queries:
        cur.execute(query)
        conn.commit()

def drop_tables(cur, conn):
    for query in drop_table_queries:
        cur.execute(query)
        conn.commit()
    
def main ():
    conn = pymysql.connect(
        host=os.getenv("MYSQL_HOST"),
        port=int(os.getenv("MYSQL_PORT")),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASS"),
        database=os.getenv("MYSQL_DB")
    )
    cur = conn.cursor()

    try:
        drop_tables(cur, conn)
        create_tables(cur, conn)
    finally:
        cur.close()
        conn.close()

if __name__ == "__main__":
    main()