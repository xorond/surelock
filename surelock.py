#!/usr/bin/env python

from libs import rsa
from libs import sql
import argparse

def main():
    
    parser = argparse.ArgumentParser(prog='Surelock')
    subparsers = parser.add_subparsers(dest='subparser_name')

    parser_enc = subparsers.add_parser('enc', help='enc help')
    parser_enc.add_argument("-o","--outfile" , help="name of the encrypted file", type=str)
    parser_enc.add_argument("-i","--infile" , help="name of the input file", type=str)
    parser_enc.add_argument("-k","--keyfile" , help="name of the keyfile", type=str)
    parser_enc.add_argument("-b","--bytes" , help="number of random bytes used for encryption", type=int)

    parser_dec = subparsers.add_parser('dec', help='dec help')
    parser_dec.add_argument("-o","--outfile" , help="name of the decrypted output file", type=str)
    parser_dec.add_argument("-i","--infile" , help="name of the encrypted input file", type=str)
    parser_dec.add_argument("-k","--keyfile" , help="name of the keyfile", type=str)
    parser_dec.add_argument("-b","--bytes" , help="number of random bytes used for encryption", type=int)

    parser_add = subparsers.add_parser('add', help='add help')
    parser_add.add_argument("entry", help="add an entry to the database", type=str)

    parser_ret= subparsers.add_parser('ret', help='ret help')
    parser_ret.add_argument("entry", help="retrieve an entry from the database", type=str)

    parser_rem = subparsers.add_parser('del', help='del help')
    parser_rem.add_argument("entry", help="delete an entry from the database", type=str)
    
#    parser_init = subparsers.add_parser('init')

    args = parser.parse_args()

    if args.subparser_name == 'enc':
        encrypt_file(args.infile, args.outfile, args.keyfile, args.bytes)
        print(args.infile)
    if args.subparser_name == 'dec':
        decrypt_file(args.infile, args.outfile, args.keyfile, args.bytes)
#    if args.subparser_name == 'add':
        
#    if args.subparser_name == 'ret':
        
#    if args.subparser_name == 'del':
        
#    if args.subparser_name == 'init':

if __name__ == '__main__':
    main()
    
    