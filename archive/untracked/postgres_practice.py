
# Working with PostgreSQL
# Installing in Python: hhttps://www.psycopg.org/psycopg3/docs/basic/install.html
import psycopg
from psycopg import sql

import sys
import pathlib

# Set base path
try:
    base_path = pathlib.Path(__file__).absolute().parents[2]
except:
    base_path = pathlib.Path.cwd().absolute()

# Add utils folder if not already in system path
if str(base_path) not in sys.path:
    print('adding path')
    sys.path.append(base_path)

# Import SQL Functions
from utils import sql_functions as sf

# * Create the connection
# -------------------------------------------------------
# Had to create this admin account via terminal
# https://www.sqlshack.com/setting-up-a-postgresql-database-on-mac/
# Psycopg3 connectionv
try:
    connection = psycopg.connect("dbname=mlb_project user=admin password=password host=localhost", autocommit=True)
except psycopg.OperationalError as e:
    print(e)

# * Create Cursor Object
# -------------------------------------------------------
cur = connection.cursor()


# * Create Player Info Table
# TODO: A way to dynamically create the table?\
schema, table_name = 'players', 'player_info'
if sf.table_exists(connection, schema, table_name):
    print('table exits, dont create')
    col_names = sf.get_table_col_names(connection, schema+'.'+table_name) # Get column names
    print(f"Columns: {col_names}")
else:
    try:
        cur.execute(sql.SQL("""CREATE TABLE {}.{} (
                                "mlbamid" int PRIMARY KEY,
                                "bbref_id" int,
                                "last_name" varchar,
                                "first_name" varchar,
                                "year_start" int,
                                "year_end" int,
                                "position" varchar
                                );""").format(sql.Identifier('players'),
                                              sql.Identifier('player_info'))
                    )
    except psycopg.Error as e:
        print(e)

# Close the connection
connection.close()