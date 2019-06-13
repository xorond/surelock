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
        try:
            self.c.execute(f"""{cmd}""")
        except Exception as e:
            print("Error: {}".format(e))
    def get_cursor(self):
        return self.c
    def commit(self):
        self.conn.commit()
    def close(self):
        self.conn.close()

def create_table(db, table_name, filename=db_name):
    # db: database object
    db.run_cmd(f""" CREATE TABLE IF NOT EXISTS {table_name} (id INTEGER PRIMARY KEY AUTOINCREMENT, site TEXT, password TEXT, description TEXT, username TEXT) """)
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
    if ("sqlite_sequence",) in tables:
        tables.remove(("sqlite_sequence",))
    return tables

def retrieve_table(db, table_name='root', filename=db_name):
    db.run_cmd(f""" SELECT site, description, username FROM {table_name}""")
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

def insert_entry(db, pwd, entry_name, entry_password, description='', table_name='root', filename=db_name, username=''):
    #inserts an entry or replaces it if the name already exists
    entry_password = crypto_funcs.Algorithm(pwd).encrypt(entry_password).decode("ascii")
    a=retrieve_entries(db, table_name, filename)
    if (entry_name,) not in a:
        db.run_cmd(f""" INSERT INTO {table_name} (site, password, description, username) VALUES ('{entry_name}', '{entry_password}', '{description}', '{username}') """)
        db.commit()
    else:
        c=input("Do you want to replace username, password and description for this entry? y/n")
        if ask_confirmation(c):
            a=get_rowid(db, entry_name, table_name)
            delete_entry(db, entry_name, table_name)
            db.run_cmd(f""" INSERT INTO {table_name} (id, site, password, description, username) VALUES ('{a}', '{entry_name}', '{entry_password}', '{description}', '{username}') """)
            db.commit()
            
def insert_entry_gui(db, pwd, entry_name, entry_password, description='', table_name='root', filename=db_name, username=''):
    #inserts an entry or replaces it if the name already exists
    entry_password = crypto_funcs.Algorithm(pwd).encrypt(entry_password).decode("ascii")
    a=retrieve_entries(db, table_name, filename)
    if (entry_name,) not in a:
        db.run_cmd(f""" INSERT INTO {table_name} (site, password, description, username) VALUES ('{entry_name}', '{entry_password}', '{description}', '{username}') """)
        db.commit()
    else:
        a=get_rowid(db, entry_name, table_name)
        delete_entry(db, entry_name, table_name)
        db.run_cmd(f""" INSERT INTO {table_name} (id, site, password, description, username) VALUES ('{a}', '{entry_name}', '{entry_password}', '{description}', '{username}') """)
        db.commit()

def retrieve_entries(db, table_name='root', filename=db_name):
    db.run_cmd(f""" SELECT site FROM {table_name}""")
    entries = db.get_cursor().fetchall()
    db.commit()
    return entries

def get_rowid(db, site, table_name='root'):
    db.run_cmd(f""" SELECT rowid FROM {table_name} WHERE site='{site}' """)
    i = db.get_cursor().fetchall()
    rowid=i[0][0]
    db.commit()
    return rowid

def delete_table(db, table_name, filename=db_name):
    db.run_cmd(f""" DROP TABLE IF EXISTS {table_name} """)
    db.commit()

def ask_confirmation(answer):
    if answer in ['y','Y','j','J']:
        return True
    else:
        return False
