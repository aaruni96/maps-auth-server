#!/usr/bin/env python3

import os
import csv
import sys
import json
import time
import uuid
import argparse


# some constants

VERSION = '0.1'
TWODAYS = 48 * 60 * 60  # 48 hours in seconds

# helper function prints to stderr
def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

# define a CLI

def addCLI():
    parser = argparse.ArgumentParser(prog="maps-auth", description="maps auth service")
    subparser = parser.add_subparsers(help="Use --help with each of thec ommands for more help", dest="SubPars_NAME")

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
    # assert that we don't already know the user
    with open(dbfile, 'r') as indb:
        for line in indb:
            assert name not in line, f"Cannot add {name} as it already exists and must be unique!\n"
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
        csvcontents = [row for row in reader if row != []]

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
        csvcontents = {row[1]:row[-1] for row in reader}

    if username in csvcontents.keys():
        #check valid key
        if is_valid_uuid(key):
            #check key equality
            if key == csvcontents[username]:
                eprint("Valid!")
                return True
            else:
               eprint("Key not registered or expired!")
    return False

def tusdauth(args, authstr):
    assert authstr[0] == "Basic"
    # call auth with the rest
    if auth(authstr[1].split(':')[0], authstr[1].split(':')[-1], args.DB):
        eprint("Authenticated!")
        return True

    # build a reject output
    rejdict = {"RejectUpload": True, "HTTPResponse":{"StatusCode": 401, "Body": "Authentication failed"}}
    print(json.dumps(rejdict))
    return False

def check_db(dbfile):
    if not os.path.isfile(dbfile):
        # db doesn't already exist
        # add just the header line to it
        with open(dbfile, 'w') as writefile:
            writefile.write("timestamp,username,key\n")
    else:
        # db already exists
        pass

def main():
    parser = addCLI()
    args = parser.parse_args()
    check_db(args.DB)
    if args.SubPars_NAME == "add":
        print("adding....")
        add_key(args.NAME, args.DB)
        pass
    elif args.SubPars_NAME == "prune":
        print("pruning now...")
        prune_db(args.DB)
    elif args.SubPars_NAME == "auth":
        print("checking auth...")
        return auth(args.NAME, args.KEY, args.DB)
    else:
        # being called from tusd, grab stuff from STDIN
        instring = sys.stdin.read()
        authstr = json.loads(instring)["Event"]["HTTPRequest"]["Header"]["Authentication"][0].split()
        tusdauth(args, authstr)



if __name__ == "__main__":
    main()
