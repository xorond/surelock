#!/usr/bin/env python

import sys
import argparse
import os
# import time

# handle our imports
try:
    from libs import crypto_funcs
    from libs import sql
    from libs import common
except Exception as e:
    print("Error: {}".format(e))
    sys.exit()

try:
    has_pandas = True
    import pandas as pd
except ImportError:
    has_pandas = False
    print("Warning: pandas library couldn't be imported")

is_posix = False
if os.name == 'posix':
    is_posix = True

def main():

    parser = argparse.ArgumentParser(prog='surelock')
    subparsers = parser.add_subparsers(dest='subparser_name')

    parser_add = subparsers.add_parser('add', help='add a new entry')
    parser_add.add_argument("-f","--file" , help="name of the database file", type=str, default="surelock.db")
    parser_add.add_argument("entry", help="name of the new entry", type=str)
    parser_add.add_argument("username" , help="username for the entry", default="", type=str)
    parser_add.add_argument("category", help="name of the category", default="root", type=str, nargs='?')
    parser_add.add_argument("-r","--random_password", help="store a random password with this entry", action='store_true')
    parser_add.add_argument("-l","--length" , help="number of characters in the random password", default=16, type=int)
    parser_add.add_argument("-s","--special_characters", help="includes special characters in the random password", action='store_true')
    parser_add.add_argument("-n","--numbers", help="includes numbers in the random password", action='store_true')
    parser_add.add_argument("-d","--description" , help="description of the entry", default="", type=str, nargs='*')

    parser_view = subparsers.add_parser('view', help='view a password')
    parser_view.add_argument("entry", help="the entry for which you want to view the password", type=str)
    parser_view.add_argument("category", help="name of the category", default="root", type=str, nargs='?')
    parser_view.add_argument("-s","--show_password", help="show the password in the console", action='store_true')
    parser_view.add_argument("-f","--file" , help="name of the database file", type=str, default="surelock.db")

    parser_del = subparsers.add_parser('del', help='delete an entry')
    parser_del.add_argument("entry", help="name of the entry you want to delete", type=str)
    parser_del.add_argument("category", help="name of the category", default="root", type=str, nargs='?')
    parser_del.add_argument("-f","--file" , help="name of the database file", type=str, default="surelock.db")

    parser_init = subparsers.add_parser('init', help='initialize a database')
    parser_init.add_argument("-f","--file" , help="name of the database file", type=str, default="surelock.db")

    parser_show_category = subparsers.add_parser('show', help='show a category')
    parser_show_category.add_argument("category", help="name of the category", type=str, nargs='?')
    parser_show_category.add_argument("-c","--list_categories", help="list all categories", action='store_true')
    parser_show_category.add_argument("-f","--file" , help="name of the database file", type=str, default="surelock.db")

    parser_add_category = subparsers.add_parser('add_category', help='add a category')
    parser_add_category.add_argument("category", help="name of the new category", type=str)
    parser_add_category.add_argument("-f","--file" , help="name of the database file", type=str, default="surelock.db")

    parser_delete_category = subparsers.add_parser('delete_category', help='delete a category')
    parser_delete_category.add_argument("category", help="name of the category you want to delete", type=str, default="root")
    parser_delete_category.add_argument("-f","--file" , help="name of the database file", type=str, default="surelock.db")

    parser_pwgen = subparsers.add_parser('pwgen', help='Generate a strong password based on a simple one')
    parser_pwgen.add_argument("simple_password", help="simple password", type=str)
    parser_pwgen.add_argument("length" , help="number of characters in the generated password", default=16, type=int, nargs='?')
    parser_pwgen.add_argument("-s","--special_characters", help="includes special characters in the generated password", action='store_true')
    parser_pwgen.add_argument("-n","--numbers", help="includes numbers in the generated password", action='store_true')

    args = parser.parse_args()

    if args.subparser_name == 'init':
        db = sql.Database(filename=args.file)
        sql.init_database_command_line(db)
        sql.add_root_table(db)

    if args.subparser_name == 'add':
        pwd = common.get_pass()
        db = sql.Database(filename=args.file)
        if sql.check_password(db, pwd):
            #join the rest of the arguments into description as a single string
            args.description = " ".join(args.description)
            if args.category == 'hashed_password_table' or args.category == "sqlite_sequence":
                print("This category cannot be created!")
            else:
                sql.create_table(db, args.category, args.file)
                if args.random_password:
                    entrypwd = crypto_funcs.pwd_gen("", args.special_characters, args.numbers, characters=args.length)
                else:
                    entrypwd = common.get_pass("Password for {}: ".format(args.entry))
                sql.insert_entry(db, pwd, args.entry, entrypwd, description=args.description, table_name=args.category, filename=args.file, username=args.username)
        else:
            print("This is the wrong password for the database!")

    if args.subparser_name == 'view':
        db = sql.Database(filename=args.file)
        a=sql.retrieve_entries(db, args.category, args.file)
        if (args.entry,) not in a:
            print('Error: No entry named {} in category {}'.format(args.entry, args.category))
        else:
            pwd = common.get_pass()
            a = sql.retrieve_entry(db, pwd, args.entry, args.category, args.file)
            if has_pandas:
                try:
                    df = pd.DataFrame([str(a)])
                    df.to_clipboard(index=False, header=False)
                    print("The password was copied to the clipboard!")
                    input("Press enter to clear the clipboard!")
                    df = pd.DataFrame([])
                    df.to_clipboard(index=False, header=False)
                except Exception:
                    print("Warning", "Failed to copy to clipboard!")
                    if not args.show_password:
                        print("The password is " + a)
                        input("Press enter to clear the command line!") #If preferred you can use time.sleep(10) instead of this line.
                        if is_posix:
                            os.system("reset")
                        else:
                            os.system("cls")
            else:
                print("Warning", "Can't to copy to clipboard! pandas library was not found!")
                if not args.show_password:
                    print("The password is " + a)
                    input("Press enter to clear the command line!") #If preferredyou can use time.sleep(10) instead of this line.
                    if is_posix:
                        os.system("reset")
                    else:
                        os.system("cls")
            if args.show_password:
                print("The password is " + a)
                input("Press enter to clear the command line!") #If preferred you can use time.sleep(10) instead of this line.
                if is_posix:
                    os.system("reset")
                else:
                    os.system("cls")

    if args.subparser_name == 'del':
        db = sql.Database(filename=args.file)
        sql.delete_entry(db, args.entry, args.category)

    if args.subparser_name == 'show':
        db = sql.Database(filename=args.file)
        tables = sql.list_tables(db)
        if args.list_categories:
            for e in sql.list_tables_with_number_of_entries(db):
                print (e)
            return
        if (str(args.category),) in tables:
            b=sql.retrieve_table(db, args.category, args.file)
            print("Category: "+str(args.category))
            for e in b:
                print("  Site: "+ str(e[0])+ "\t Username: ".expandtabs(15-len(e[0]))+ str(e[2]) + "\t Description: ".expandtabs(15-len(e[2]))+ str(e[1]))
        else:
            for c in tables:
                a=c[0]
                print("Category: "+str(a))
                b=sql.retrieve_table(db, a, args.file)
                for e in b:
                    print("  Site: "+ str(e[0])+ "\t Username: ".expandtabs(15-len(e[0]))+ str(e[2]) + "\t Description: ".expandtabs(15-len(e[2]))+ str(e[1]))

    if args.subparser_name == 'add_category':
        db = sql.Database(filename=args.file)
        if args.category == 'hashed_password_table' or args.category == "sqlite_sequence":
            print("This category cannot be created!")
        else:
            sql.create_table(db, args.category, args.file)

    if args.subparser_name == 'delete_category':
        db = sql.Database(filename=args.file)
        sql.delete_table(db, args.category, args.file)

    if args.subparser_name == 'pwgen':
        print(crypto_funcs.pwd_gen(args.simple_password, args.special_characters, args.numbers, characters=args.length))

    # handle no arguments
    if len(sys.argv[1:]) == 0:
        parser.print_help()
        sys.exit()

if __name__ == '__main__':
    main()
