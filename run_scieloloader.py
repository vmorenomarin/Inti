#!/usr/bin/env python3
"""Created by: Victor Moreno Marin."""

from scielo.scielorequest import ScieloRequest

import argparse
import logging

parser = argparse.ArgumentParser(description='Download Scielo collections,'
                                 'journals and articles and.')
parser.add_argument('--db', required=True, type=str,
                    help='Database name (example: scielo_db)')
parser.add_argument('--host', required=True, type=str, default=None,
                    help='IP Address to associated host.')

args = parser.parse_args()

requester = ScieloRequest(db=args.db, host=args.host)

logging.warning("--------------------------------------------------------\n")
logging.warning("Starting Scielo Request ")
requester.get_collections()
requester.get_journals()
requester.create_cache()
requester.get_articles()
logging.warning("Scielo articles downloaded. ")
logging.warning("--------------------------------------------------------\n")
