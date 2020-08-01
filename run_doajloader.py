#!/usr/bin/env python3

from inti.DOAJ.DOAJRequest import DOAJRequest

import argparse
import logging

parser = argparse.ArgumentParser(description='DOAJ request using APi.')
parser.add_argument('--db',required=True, type=str, help='Database name to read the data collection (example: doaj)')
parser.add_argument('--collection',required=True, type=str, help='Collection from DOAJ database (example lens')
parser.add_argument('--debug', action='store_true', help='Produces a lot of output messages for debug')

args = parser.parse_args()


loader=DOAJRequest(database_name=args.db, collection=args.collection)


logging.warning("--------------------------------------------------------\n")
logging.warning("Starting DOAJ Request ")
pisssn, eissn = loader.getIssnLists()
logging.warning("DOAJ request finished! ")
logging.warning("--------------------------------------------------------\n")
