#!/usr/bin/env python3

import sqlite3
from libs import crypto_funcs

db_name = "surelock.db"

class Database:
    def __init__(self, filename=db_name):
        self.filename = filename
        self.conn = sqlite3.connect(self.filename)
        self.c = self.conn.cursor()
    def run_cmd(self, cmd, filename=db_name):
        self.filename = filename
        self.c.execute(f"""{cmd}""")
    def get_cursor(self):
        return self.c
    def commit(self):
        self.conn.commit()
    def close(self):
        self.conn.close()

db = Database()

def create_table(table_name, filename=db_name):
    db.run_cmd(f""" CREATE TABLE IF NOT EXISTS {table_name} (id INTEGER PRIMARY KEY AUTOINCREMENT, site TEXT, password TEXT, description TEXT) """)
    db.commit()

def insert_entry(entry_name, entry, description='', rowid='', table_name='root', filename=db_name):
    # use REPLACE if a rowid is given, INSERT if not
    # TODO: implement encrypt_text and decrypt_text in this function
    if rowid == '':
        db.run_cmd(f""" INSERT INTO {table_name} (site, password, description) VALUES ('{entry_name}', '{entry}', '{description}') """)
        db.commit()
    else:
        db.run_cmd(f""" REPLACE INTO {table_name} (id, site, password, description) VALUES ('{rowid}', '{entry_name}', '{entry}', '{description}') """)
        db.commit()

def delete_entry(rowid, table_name='root'):
    db.run_cmd(f""" DELETE FROM {table_name} WHERE id = {rowid}""")
    db.commit()

def init_database(filename=db_name):
    create_table('root', filename)
    db.commit()

def list_tables(filename=db_name):
    db.run_cmd("SELECT name FROM sqlite_master WHERE type='table'")
    tables = db.get_cursor().fetchall()
    db.commit()
    return tables

def retrieve_table(table_name, filename=db_name):
    # TODO: like in list_tables
    db.run_cmd(f""" SELECT * FROM {table_name}""")
    db.commit()
    
def retrieve_entry(site, table_name, filename=db_name):
    # TODO: like in list_tables
    db.run_cmd(f""" SELECT * FROM {table_name} where site={site}""")
    db.commit()
