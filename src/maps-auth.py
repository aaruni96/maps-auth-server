#!/usr/bin/env python3

import os
import csv
import time
import uuid
import argparse


# some constants

VERSION = '0.1'
TWODAYS = 48 * 60 * 60  # 48 hours in seconds



# define a CLI

def addCLI():
    parser = argparse.ArgumentParser(prog="maps-auth", description="maps auth service")
    subparser = parser.add_subparsers(help="Use --help with each of thec ommands for more help", dest="SubPars_NAME", required=True)

    # arguments for main path
    parser.add_argument("--version", action='version', version=VERSION)
    parser.add_argument("--db", dest="DB", action='store', default="authdb.csv", help="name of database file")

    # arguments for adding user to db
    parser_add = subparser.add_parser("add", help="Command for adding a dude to the db")
    parser_add.add_argument("-n", "--name", dest="NAME", action='store', default=False, help="Username of the dude to add", required=True)

    # arguemnts for pruning
    parser_prune = subparser.add_parser("prune", help="command for pruning the db")

    # arguments for auth
    parser_auth = subparser.add_parser("auth", help="command for auth")
    parser_auth.add_argument("-n", "--name", dest="NAME", action="store", default=False, help="Username of the dude to check")
    parser_auth.add_argument("-k", "--key", dest="KEY", action='store', default=False, help="dude's password")

    return parser


# helper function to get current unix time
def unix_time():
    return int(time.strftime("%s"))

# helper function to validate UUID
def is_valid_uuid(key: str):
    try:
        uuid.UUID(key, version=4)
        return True
    except:
        print("Invalid key!")
    return False

def add_key(name: str, dbfile: str):
    key = uuid.uuid4()
    with open(dbfile, 'a') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerow([unix_time(), name, key])
    return 0

def prune_db(dbfile: str):
    pass
    with open(dbfile) as readfile:
        reader = csv.reader(readfile, delimiter=',')
        csvheader = reader.__next__()
        csvcontents = [row for row in reader]

    with open("tmpdb.csv", 'w', newline='') as writefile:
        writer = csv.writer(writefile, delimiter=',')
        writer.writerow(csvheader)
        for row in csvcontents:
            #if row is newer than 48 hours
            if unix_time() - int(row[0]) < TWODAYS:
                writer.writerow(row)

    os.replace("tmpdb.csv", dbfile)
    return 0

def auth(username: str, key: str, dbfile: str):
    with open(dbfile) as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        csvheader = reader.__next__()
        csvcontents = {row[1]:row[2] for row in reader}

    if username in csvcontents.keys():
        #check valid key
        if is_valid_uuid(key):
            #check key equality
            if key == csvcontents[username]:
                print("Valid!")
            else:
                print("Key not registered or expired!")

def main():
    parser = addCLI()
    args = parser.parse_args()
    if args.SubPars_NAME == "add":
        print("adding....")
        add_key(args.NAME, args.DB)
        pass
    elif args.SubPars_NAME == "prune":
        print("pruning now...")
        prune_db(args.DB)
    elif args.SubPars_NAME == "auth":
        pass
    else:
        raise ValueError("Impossible Case")


if __name__ == "__main__":
    main()
