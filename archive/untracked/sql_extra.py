
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


##### Extra
# ---------------------------------------------------------------
# Psycopg2 connection
connection = psycopg.connect(database="postgres", user="admin", password="password", host="127.0.0.1", port="5432")

# * What Connection do people prefer?
# Psycopg3 connection
with psycopg.connect("dbname=postgres user=admin password=password") as conn:
    with conn.cursor() as cur:
        print('hello v2')