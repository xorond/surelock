#!/usr/bin/env python

import sys
import argparse

# handle our imports
try:
    from libs import crypto_funcs
    from libs import sql
    from libs import common
    import pandas as pd
except Exception as e:
    print("Error: {}".format(e))
    sys.exit()

def main():
    
    parser = argparse.ArgumentParser(prog='surelock')
    subparsers = parser.add_subparsers(dest='subparser_name')

    parser_add = subparsers.add_parser('add', help='add a new entry')
    parser_add.add_argument("entry", help="name of the new entry", type=str)
    parser_add.add_argument("-f","--file" , help="name of the database file", type=str, default="surelock.db")
    parser_add.add_argument("-c","--category" , help="name of the category", type=str, default="root")
    parser_add.add_argument("-u","--username" , help="username for the entry", type=str, default="")
    parser_add.add_argument("-d","--description" , help="description of the entry", type=str, default="")
    
    parser_view = subparsers.add_parser('view', help='view a password')
    parser_view.add_argument("entry", help="the entry for which you want to view  password", type=str)
    parser_view.add_argument("-f","--file" , help="name of the database file", type=str, default="surelock.db")
    parser_view.add_argument("-c","--category" , help="name of the category", type=str, default="root")

    parser_del = subparsers.add_parser('del', help='delete an entry')
    parser_del.add_argument("entry", help="name of the entry you want to delete", type=str)
    parser_del.add_argument("-f","--file" , help="name of the database file", type=str, default="surelock.db")
    parser_del.add_argument("-c","--category" , help="name of the category", type=str, default="root")

    parser_list = subparsers.add_parser('list', help='list categories from the database')
    parser_list.add_argument("-f","--file" , help="name of the database file", type=str, default="surelock.db")
    
    parser_init = subparsers.add_parser('init', help='initialize a database')
    parser_init.add_argument("-f","--file" , help="name of the database file", type=str, default="surelock.db")
    
    parser_show_category = subparsers.add_parser('show', help='show a category')
    parser_show_category.add_argument("-c","--category", help="the category you want to view", type=str, default="root")
    parser_show_category.add_argument("-f","--file" , help="name of the database file", type=str, default="surelock.db")
    
    parser_add_category = subparsers.add_parser('add_category', help='add a category')
    parser_add_category.add_argument("category", help="name of the new category", type=str)
    parser_add_category.add_argument("-f","--file" , help="name of the database file", type=str, default="surelock.db")

    parser_delete_category = subparsers.add_parser('delete_category', help='delete a category')
    parser_delete_category.add_argument("category", help="name of the category you want to delete", type=str, default="root")
    parser_delete_category.add_argument("-f","--file" , help="name of the database file", type=str, default="surelock.db")
    
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
        pwd = common.get_pass_input()
        db = sql.Database(filename=args.file)
        sql.create_table(db, args.category, args.file)
        entrypwd = common.get_pass("Password for {}: ".format(args.entry))
        sql.insert_entry(db, pwd, args.entry, entrypwd, description=args.description, table_name=args.category, filename=args.file, username=args.username)
        
    if args.subparser_name == 'view':
        db = sql.Database(filename=args.file)
        a=sql.retrieve_entries(db, args.category, args.file)
        if (args.entry,) not in a:
            print('Error: No entry named {} in category {}'.format(args.entry, args.category))
        else:
            pwd = common.get_pass()
            a = sql.retrieve_entry(db, pwd, args.entry, args.category, args.file)
            print(a)
            df=pd.DataFrame([str(a)])
            df.to_clipboard(index=False,header=False)

    if args.subparser_name == 'del':
        db = sql.Database(filename=args.file)
        sql.delete_entry(db, args.entry, args.category)

    if args.subparser_name == 'show':
        db = sql.Database(filename=args.file)
        b=sql.retrieve_table(db, args.category, args.file)
        print("Category: "+str(args.category))
        for e in b:
            print("  Site: "+ str(e[0])+ "\t Username: ".expandtabs(15-len(e[0]))+ str(e[2]) + "\t Description: ".expandtabs(15-len(e[2]))+ str(e[1]))
    
    if args.subparser_name == 'showall':
        db = sql.Database(filename=args.file)
        tables = sql.list_tables(db)
        tables.remove(("sqlite_sequence",))
        for c in tables:
            a=c[0]
            print("Category: "+str(a))
            b=sql.retrieve_table(db, a, args.file)
            for e in b:
                print("  Site: "+ str(e[0])+ "\t Username: ".expandtabs(15-len(e[0]))+ str(e[2]) + "\t Description: ".expandtabs(15-len(e[2]))+ str(e[1]))

    if args.subparser_name == 'add_category':
        db = sql.Database(filename=args.file)
        sql.create_table(db, args.category, args.file)
        
    if args.subparser_name == 'delete_category':
        db = sql.Database(filename=args.file)
        sql.delete_table(db, args.category, args.file)

    # handle no arguments
    if len(sys.argv[1:]) == 0:
        parser.print_help()
        sys.exit()
    
if __name__ == '__main__':
    main()
