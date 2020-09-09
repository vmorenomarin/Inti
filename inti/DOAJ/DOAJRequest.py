#!/usr/bin/env python3

#author: Victor Moreno Marin, Gerardo Gutierrez
# #email: vmorenomarin@gmail.com, muzgash@gmail.com

from pymongo import MongoClient
from forex_python.converter import CurrencyRates
import requests
import numpy as np

class DOAJRequest:   
"""Create a DOAJ object to request and save data from DOAJ site using its API."""
    def __init__(self,database_name,collection):
        """
        Class to get requested data from DOAJ API.
        Requiere database name and inner collection to get the ISSN codes list.
        """
        self.client = MongoClient()
        self.db = self.client[database_name]
        self.collection = self.db[collection]

    def getIssnLists(self):
        """Returns print and electronic ISSN from Lens collection."""
        pissn_list = []
        eissn_list = []
        for register in self.collection.find():
            if "source" in register.keys():
                if register["source"]:
                    if not "issn" in register["source"]:
                        continue
                    for issn in register["source"]["issn"]:
                        if issn["type"] == "print":
                            pissn_list.append(issn["value"])
                        elif issn["type"] == "electronic":
                            eissn_list.append(issn["value"])

        return pissn_list, eissn_list

    def getAPC(self,issn_list):
        """
        Returns whole data requested from DOAJ. Data is storage as a dictionary.
        Also returns a dictionary only with hata that has APC values.
        """
        self.issn_list=issn_list
        apc_dict = {}
        data_request = {}
        for issn in self.issn_list:
            issn_formated = issn[:4]+'-'+issn[4:]
            url_request = 'https://doaj.org/api/v1/search/journals/{0}'.format(issn_formated)
            response = requests.get(url_request)
            data = response.json()
            data_request = data
            if len(data['results']) > 0:
                if not 'apc' in data['results'][0]['bibjson']:
                    continue
                if 'apc' in data['results'][0]['bibjson']:
                    apc = data['results'][0]['bibjson']['apc']
                    apc_dict[issn_formated] = apc

        return apc_dict, data_request

    def convert_apc2usd(self,dictionary):
        """
        Converts APC average price to USD currency. Needs dictionary
        with ISSN with APC data.
        """

        self.dictionary=dictionary

        c = CurrencyRates()
        for issn in self.dictionary.keys():
            if  self.dictionary[issn]['currency'] != 'USD':
                currency_foreign = self.dictionary[issn]['currency']
                avr_price_foreign = self.dictionary[issn]['average_price']
                usd_currency = c.convert(currency_foreign,'USD',avr_price_foreign)

                # Update dictionaty with APC in USD currency.
                usd_currency_aprox = int(np.floor(usd_currency))
                self.dictionary[issn] = {'currency':'USD','average_price':usd_currency_aprox}

        return self.dictionary