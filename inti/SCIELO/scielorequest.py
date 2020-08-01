from pymongo import MongoClient
from bson.objectid import ObjectId

from articlemeta.client import RestfulClient
from xylose.scielodocument import Article, Journal, Issue

class ScieloRequest:
    """
    Request class to build a SciELO database with three central collections:
    collections, journals and documents.
    The class methods use the Scielo API to get database documents.
    """
    def __init__(self, database_name='scielo'):
        
        self.client = MongoClient()
        self.db = self.client[database_name]
        #self.collection = self.db[collection]

    # Client to get Scielo information
    scielo_client = RestfulClient()
            
    def get_collections(self, scielo_client):
        """
        Gets collections from Scielo servers. 
        """
        collections=scielo_client.collections()
        for collection in collections:
            self.db['collections'].insert_one(collection)
    
    def list_collections(self):
        """
        List dababse SciELo colections. Displays its name and alpha-3
        code.
        """
        list_collections = []
        for collection in self.db["collection"]:
            code=collection[code]
            name=collection['code']['name']['en']
            list_collections.append({name: code})

        return list_collections

    def get_journals(self, scielo_client):
        """
        Gets raw data of journals from Scielo servers.
        A collection identification id is added in data to
        relate journals belong from each collection. 
        """
        for collection in self.db['collections'].find():
            collection_code=collection['code']
            for journal in scielo_client.journals(collection_code):
                journal.data['collection_id']=collection['_id']
                self.db['journals'].insert_one(journal.data)

    def list_jornals_in_collection(self,collection_code):
        """
        List dababse SciELo colections. Displays its name and alpha-3
        code.
        """
        journals_in_collection = {}
        for collection in self.db['collections']:
            if collection[collection_code]:
                for journal in self.db['journals']:
                    journal_name=journal['data']['v100']
                    journal_issn=journal['issns'][0]
                journals_in_collection[journal_issn]=journal_name

        return journals_in_collection

    def get_articles(self, scielo_client):
        """
        Gets raw data of articles from Scielo servers.
        A journal database identification id is added in data to
        relate articles belong from each journal. 
        """
        for collection in self.db['collections'].find():
            collection_code=collection['code']
            for journal in self.db['journals'].find():
                try:
                    journal_issn=journal['issns'][0]
                    docs=scielo_client.documents(collection_code,journal_issn)
                    for article in docs:
                        article.data['journal_id']=journal['_id']
                        self.db['stage'].insert_one(article.data)

                except:
                    continue