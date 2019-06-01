#!/usr/bin/env python

from libs import crypto_funcs
from libs import sql
import argparse
import pandas as pd
#pandas is used to copy the password to the clipboard (cross-platform support) 

def main():
    
    parser = argparse.ArgumentParser(prog='surelock')
    subparsers = parser.add_subparsers(dest='subparser_name')

    parser_add = subparsers.add_parser('add', help='add a new entry')
    parser_add.add_argument("entry", help="name of the new entry", type=str)
    parser_add.add_argument("entrypwd", help="password to be saved with this entry", type=str)
    parser_add.add_argument("-f","--file" , help="name of the database file", type=str, default="surelock.db")
    parser_add.add_argument("-t","--table" , help="name of the table", type=str, default="root")
    parser_add.add_argument("-u","--username" , help="username for the entry", type=str, default="")
    
    parser_view = subparsers.add_parser('view', help='view a password')
    parser_view.add_argument("entry", help="the entry for which you want to view  password", type=str)
    parser_view.add_argument("-f","--file" , help="name of the database file", type=str, default="surelock.db")
    parser_view.add_argument("-t","--table" , help="name of the table", type=str, default="root")

    parser_del = subparsers.add_parser('del', help='delete an entry')
    parser_del.add_argument("entry", help="name of the entry you want to delete", type=str)
    parser_del.add_argument("-f","--file" , help="name of the database file", type=str, default="surelock.db")
    parser_del.add_argument("-t","--table" , help="name of the table", type=str, default="root")

    parser_list = subparsers.add_parser('list', help='list tables from the database')
    parser_list.add_argument("-f","--file" , help="name of the database file", type=str, default="surelock.db")
    
    parser_init = subparsers.add_parser('init', help='initialize a database')
    parser_init.add_argument("-f","--file" , help="name of the database file", type=str, default="surelock.db")
    
    parser_show_table = subparsers.add_parser('show', help='show a table')
    parser_show_table.add_argument("-t","--table", help="the table you want to view", type=str, default="root")
    parser_show_table.add_argument("-f","--file" , help="name of the database file", type=str, default="surelock.db")
    
    parser_add_table = subparsers.add_parser('add_table', help='add a table')
    parser_add_table.add_argument("table", help="name of the new table", type=str)
    parser_add_table.add_argument("-f","--file" , help="name of the database file", type=str, default="surelock.db")

    parser_delete_table = subparsers.add_parser('delete_table', help='delete a table')
    parser_delete_table.add_argument("table", help="name of the table you want to delete", type=str, default="root")
    parser_delete_table.add_argument("-f","--file" , help="name of the database file", type=str, default="surelock.db")
    
    parser_show_all_entries = subparsers.add_parser('showall', help='shows all entries in the database')
    parser_show_all_entries.add_argument("-f","--file" , help="name of the database file", type=str, default="surelock.db")
    
    args = parser.parse_args()

    if args.subparser_name == 'init':
        db = sql.Database(filename=args.file)
        sql.init_database(db)

    if args.subparser_name == 'list':
        db = sql.Database(filename=args.file)
        tables = sql.list_tables(db)
        tables.remove(("sqlite_sequence",))
        for e in tables:
            print (str(e[0]))

    if args.subparser_name == 'add':
        pwd = crypto_funcs.get_pass_input()
        db = sql.Database(filename=args.file)
        sql.insert_entry2(db, pwd, args.entry, args.entrypwd, description=args.username, table_name=args.table, filename=args.file)
        
    if args.subparser_name == 'view':
        pwd = crypto_funcs.get_pass_input()
        db = sql.Database(filename=args.file)
        a = sql.retrieve_entry(db, pwd, args.entry, args.table, args.file)
        print(a)
        df=pd.DataFrame([str(a)])
        df.to_clipboard(index=False,header=False)

    if args.subparser_name == 'del':
        db = sql.Database(filename=args.file)
        sql.delete_entry(db, args.entry, args.table)

    if args.subparser_name == 'show':
        db = sql.Database(filename=args.file)
        b=sql.retrieve_table(db, args.table, args.file)
        print("Table: "+str(args.table))
        for e in b:
            print("  Seite: "+ str(e[0])+ "\t Username: ".expandtabs(15-len(e[0]))+ str(e[1]))
    
    if args.subparser_name == 'showall':
        db = sql.Database(filename=args.file)
        tables = sql.list_tables(db)
        tables.remove(("sqlite_sequence",))
        for c in tables:
            a=c[0]
            print("Table: "+str(a))
            b=sql.retrieve_table(db, a, args.file)
            for e in b:
                print("  Seite: "+ str(e[0])+ "\t Username: ".expandtabs(15-len(e[0]))+ str(e[1]))

    if args.subparser_name == 'add_table':
        db = sql.Database(filename=args.file)
        sql.create_table(db, args.table, args.file)
        
    if args.subparser_name == 'delete_table':
        db = sql.Database(filename=args.file)
        sql.delete_table(db, args.table, args.file)
    
if __name__ == '__main__':
    main()
