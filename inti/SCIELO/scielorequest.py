from pymongo import MongoClient
from articlemeta.client import RestfulClient
import json

class ScieloRequest:
    """
    Request class to build a SciELO database with three central collections:
    collections, journals and documents.
    The class methods use the Scielo API to get database documents.
    """
    def __init__(self, database_name='scielo'):
        """
        """
        self.client=MongoClient()
        self.db=self.client[database_name]
        #self.collection = self.db[collection]
        self.scielo_client = RestfulClient()

    # Client to get Scielo information
    
            
    def get_collections(self):
        """
        Gets collections from Scielo servers.
        """
        collections=self.scielo_client.collections()
        for collection in collections:
            self.db['collections'].insert_one(collection)
    
    def list_collections(self):
        """
        List dababse SciELo colections. Displays its name and alpha-3
        code.
        """
        list_collections = []
        for collection in self.db["collection"]:
            collection_code=collection[code]
            name=collection['code']['name']['en']
            list_collections.append({name: collection_code})

        return list_collections

    def get_journals(self):
        """
        Gets raw data of journals from Scielo servers.
        A collection identification id is added in data to
        relate journals belong from each collection.
        """
        for collection in self.db['collections'].find():
            collection_code=collection['code']
            for journal in self.scielo_client.journals(collection_code):
                journal.data['collection_id']=collection['_id']
                self.db['journals'].insert_one(journal.data)

    def list_jornals_in_collection(self, collection_code):
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

    '''def get_articles(self, scielo_client):
        """
        Gets raw data of articles from Scielo servers.
        A journal database identification id is added in data to
        relate articles belong from each journal. 
        """
        for collection in self.db['collections'].find():
            collection_code=collection['code']
            with self.db['journals'].find(no_cursor_timeout=True) as cursor:
                for journal in cursor:
                    journal_issn=journal['issns'][0]
                    docs=scielo_client.documents(collection_code,journal_issn)
                    for article in docs:
                        article.data['journal_id']=journal['_id']
                        self.db['stage'].insert_one(article.data)
            """ try:    
                for journal in self.db['journals'].find():
                    journal_issn=journal['issns'][0]
                    docs=scielo_client.documents(collection_code,journal_issn)
                    for article in docs:
                        article.data['journal_id']=journal['_id']
                        self.db['stage'].insert_one(article.data)
            except Exception():
                parse_Exception
            finally:
                cursor.close() """'''

    def create_status(journal_list):
        """
        This method builds artciles downloaded status list for a specific collection. 
        The list is saved as text file.
        """
        cursor=self.db['stage'].find({'downloaded':1})
        dl_articles=[] 
        for i in cursor:
            code=i.data['code']
            dl_articles.append(code)
        
        with open('status.txt', 'w') as f:
            f.write(json.dumps(dl_articles))
        

    def check_status(journal_list):
        """
        This method checks the status for downloaded articles for a specific collection. 
        Loads the text file createrd by create_status method.
        """
        cursor=self.db['stage'].find({'downloaded':1})
        dl_articles=[] 
        for i in cursor:
            code=i.data['code']
            dl_articles.append(code)
        
        with open('status.txt', 'w') as f:
            f.write(json.dumps(dl_articles))
  


    def get_articles(self):
        """
        Gets raw data of articles from Scielo servers.
        A journal database identification id is added in data to
        relate articles belong from each journal. 
        """
        cursor = self.db['journals'].find(no_cursor_timeout=True)
        for journal in cursor:
            issn=journal['issns'][0]
            code_collection=journal['collection']
            docs=self.scielo_client.documents(code_collection,issn)
            for article in docs:
                article.data['journal_id']=journal['_id']
                article.data['downloaded']=1
                result=self.db['stage'].insert_one(article.data)
            '''
            checked_journals.append(issn)
            saved_docs[code_collection]=checked_journals
            date_string=time.strftime('%Y%m%d_%H%M%S')
            checkpoint[date_string]=saved_docs
            '''