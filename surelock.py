#!/usr/bin/env python

from libs import crypto_funcs
from libs import sql
import argparse

def main():
    
    parser = argparse.ArgumentParser(prog='surelock')
    subparsers = parser.add_subparsers(dest='subparser_name')

    parser_add = subparsers.add_parser('add', help='add a new entry')
    parser_add.add_argument("entry", help="add an entry to the database", type=str, default="surelock.db")

    parser_ret= subparsers.add_parser('view', help='view an entry')
    parser_ret.add_argument("entry", help="view an entry from the database", type=str, default="surelock.db")

    parser_rem = subparsers.add_parser('del', help='delete an entry')
    parser_rem.add_argument("entry", help="delete an entry from the database", type=str, default="surelock.db")

    parser_list = subparsers.add_parser('list', help='list categories from the database')
    parser_list.add_argument("-f","--file" , help="name of the database file", type=str, default="surelock.db")
    
    parser_init = subparsers.add_parser('init', help='initialize the database')
    parser_init.add_argument("-f","--file" , help="name of the database file", type=str, default="surelock.db")

    args = parser.parse_args()

    if args.subparser_name == 'init':
        db = sql.Database(filename=args.file)
        sql.init_database(db)

    if args.subparser_name == 'list':
        db = sql.Database(filename=args.file)
        tables = sql.list_tables(db)
        print(tables)

# TODO: all of these

#    if args.subparser_name == 'add':
#        db = sql.Database(filename=args.file)
        
#    if args.subparser_name == 'ret':
#        db = sql.Database(filename=args.file)

#    if args.subparser_name == 'del':
#        db = sql.Database(filename=args.file)
        
#    if args.subparser_name == 'init':
#        db = sql.Database(filename=args.file)

if __name__ == '__main__':
    main()
