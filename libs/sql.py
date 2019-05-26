#!/usr/bin/env python3

import sqlite3
from libs import crypto_funcs

db_name = "surelock.db"

def run_sql_cmd(cmd, filename=db_name):
    # wrapper function for running sql commands on a database.
    # note: sqlite3.connect() will create a database file if it doesn't exist
    conn = sqlite3.connect(filename)

    c = conn.cursor()

    c.execute(f"""{cmd}""")

    # save changes and close connection
    conn.commit()
    conn.close()

def create_table(table_name, filename=db_name):
    run_sql_cmd(f""" CREATE TABLE IF NOT EXISTS {table_name} (id INTEGER PRIMARY KEY AUTOINCREMENT, site TEXT, password TEXT, description TEXT) """)

def insert_entry(entry_name, entry, description='', rowid='', table_name='root', filename=db_name):
    # use REPLACE if a rowid is given, INSERT if not
    if rowid == '':
        run_sql_cmd(f""" INSERT INTO {table_name} (site, password, description) VALUES ('{entry_name}', '{entry}', '{description}') """)
    else:
        run_sql_cmd(f""" REPLACE INTO {table_name} (id, site, password, description) VALUES ('{rowid}', '{entry_name}', '{entry}', '{description}') """)

def delete_entry(rowid, table_name='root'):
    run_sql_cmd(f""" DELETE FROM {table_name} WHERE id = {rowid}""")

def init_database(filename=db_name):
    # TODO: implement encrypt_database and decrypt_database in this function
    create_table('root')
    
def list_tables(filename=db_name):
    run_sql_cmd("SELECT name FROM root WHERE type='table'")
        
def retrieve_table(table_name, filename=db_name):
    run_sql_cmd(f""" SELECT * FROM {table_name}""")
    
def retrieve_entry(site, table_name, filename=db_name):
    run_sql_cmd(f""" SELECT * FROM {table_name} where site={site}""")


