import pymysql.cursors
from sql_queries import *

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
        host='localhost',
        user='root',
        password='mypassword',
        database='tomo'
    )
    cur = conn.cursor()

    drop_tables(cur, conn)
    create_tables(cur, conn)

    conn.close()

if __name__ == "__main__":
    main()