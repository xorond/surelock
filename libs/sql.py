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

def create_table(db, table_name, filename=db_name):
    # db: database object
    db.run_cmd(f""" CREATE TABLE IF NOT EXISTS {table_name} (id INTEGER PRIMARY KEY AUTOINCREMENT, site TEXT, password TEXT, description TEXT) """)
    db.commit()

def insert_entry(db, pwd, entry_name, entry, description='', rowid='', table_name='root', filename=db_name):
    # db: database object
    # pwd: result from get_pass_input

    entry = crypto_funcs.Algorithm(pwd).encrypt(entry).decode("ascii")

    if rowid == '':
        db.run_cmd(f""" INSERT INTO {table_name} (site, password, description) VALUES ('{entry_name}', '{entry}', '{description}') """)
        db.commit()
    else:
        db.run_cmd(f""" REPLACE INTO {table_name} (id, site, password, description) VALUES ('{rowid}', '{entry_name}', '{entry}', '{description}') """)
        # we use REPLACE if a rowid is given, INSERT if not
        db.commit()
     
def delete_entry(db, site, table_name='root'):
    db.run_cmd(f""" DELETE FROM {table_name} WHERE site='{site}' """)
    db.commit()

def init_database(db, filename=db_name):
    create_table(db, 'root', filename)
    db.commit()

def list_tables(db, filename=db_name):
    db.run_cmd("SELECT name FROM sqlite_master WHERE type='table'")
    tables = db.get_cursor().fetchall()
    db.commit()
    return tables

def retrieve_table(db, table_name='root', filename=db_name):
    db.run_cmd(f""" SELECT site, description FROM {table_name}""")
    table = db.get_cursor().fetchall()
    db.commit()
    return table
        
def retrieve_entry(db, pwd, site, table_name='root', filename=db_name):
    db.run_cmd(f""" SELECT password FROM {table_name} WHERE site='{site}' """)
    entrypwd = db.get_cursor().fetchall()
    a=entrypwd[0][0]
    decpwd = crypto_funcs.Algorithm(pwd).decrypt(a)
    db.commit()
    return decpwd

def insert_entry2(db, pwd, entry_name, entry, description='', table_name='root', filename=db_name):
    #inserts an entry or replaces it if the name already exists
    entry = crypto_funcs.Algorithm(pwd).encrypt(entry).decode("ascii")
    a=retrieve_entries(db, table_name, filename)
    if (entry_name,) not in a:
        db.run_cmd(f""" INSERT INTO {table_name} (site, password, description) VALUES ('{entry_name}', '{entry}', '{description}') """)
        db.commit()
    else:
        c=input("Do you want to replace the username and password for this entry? y/n")
        if c == "y":
            a=get_rowid(db, entry_name, table_name)
            delete_entry(db, entry_name, table_name)
            db.run_cmd(f""" INSERT INTO {table_name} (id, site, password, description) VALUES ('{a}', '{entry_name}', '{entry}', '{description}') """)
            db.commit()

def retrieve_entries(db, table_name='root', filename=db_name):
    #lists all entries, used in insert_entry2 to check if an entry already exists 
    db.run_cmd(f""" SELECT site FROM {table_name}""")
    entries = db.get_cursor().fetchall()
    db.commit()
    return entries

def get_rowid(db, site, table_name='root'):
    # This function is used to avoid non-consecutive rowids when replacing an entry with insert_entry2, however deleting a single entry still leads to non-consecutive rowids
    db.run_cmd(f""" SELECT rowid FROM {table_name} WHERE site='{site}' """)
    i = db.get_cursor().fetchall()
    rowid=i[0][0]
    db.commit()
    return rowid

def delete_table(db, table_name, filename=db_name):
    db.run_cmd(f""" DROP TABLE IF EXISTS {table_name} """)
    db.commit()
