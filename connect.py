import psycopg2
import os
from glob import glob

def connect():
    """ Connect to the PostgreSQL database server """
    try:
        # Connecting to the PostgreSQL server
        conn = psycopg2.connect(
            host=os.getenv('DATABASE_HOSTNAME'),
            database=os.getenv('DATABASE_NAME'),
            user=os.getenv('DATABASE_USER'),
            password=os.getenv('DATABASE_PASSWORD'),
            port=os.getenv('DATABASE_PORT')
        )
        print('Connected to the PostgreSQL server.')
        return conn
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)

def init_tables(conn):
    try:
        cur = conn.cursor()
        # Find all .sql files in the scripts/sql directory
        entities = glob('scripts/create_tables/*.sql')
        linking_tables = glob('scripts/create_linking_Tables/*.sql')
        sql_files = entities + [item for item in linking_tables]

        # Execute each table creation file
        for sql_file in sql_files:
          with open(sql_file, 'r') as file:
            sql = file.read()
            ex = cur.execute(f"""{sql}""")
            print(ex)
            conn.commit()
    except psycopg2.DatabaseError as error:
        print(error)
        conn.rollback()  # Rollback changes on error

if __name__ == '__main__':
    conn = connect()
    init_tables(conn)