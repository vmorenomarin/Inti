from pymongo import MongoClient
from articlemeta.client import RestfulClient
import json

class ScieloRequest:
    """
    Requests class to build a SciELO database with three central collections: 
    'collections' (mainly countries), 'journals' and 'articles'. 
    The class methods use the SciELO API to get database documents.
    """
    def __init__(self, database_name='scielo-test',dbserver_url="localhost",port=27017):
        """
        """
        self.client=MongoClient(dbserver_url,port)
        self.db=self.client[database_name]
        self.scielo_client = RestfulClient()

    def get_collections(self):
        """
        Gets collections from SciELO database.
        """
        collections=self.scielo_client.collections()
        for collection in collections:
            self.db['collections'].insert_one(collection)

    def list_collections(self):
        """
        Lists database SciELO collections. Displays its name and alpha-3 code.
        """
        list_collections=[]
        cursor=self.db["collections"].find()
        for collection in cursor:
            collection_code=collection['code']
            name=collection['name']['en']
            list_collections.append({name: collection_code})
        return list_collections

    def get_journals(self):
        """
        Gets raw data of journals from SciELO. A collection identification id 
        is added in data to relate journals belong from each collection.
        """
        cursor=self.db['collections'].find()
        for collection in cursor:
            collection_code=collection['code']
            for journal in self.scielo_client.journals(collection_code):
                journal['collection_id']=collection['_id']
                self.db['journals'].insert_one(journal.data)

    def list_jornals_in_collection(self, collection_code):
        """
        Lists database SciELO collections. Returns a tuple with a dictionary 
        that has ISSN code and journal name; the another object tuple's is the total journals number.
        """
        journals_in_collection = {}
        for journal in self.db['journals'].find():
            if collection_code in journal['collection']:
                journal_name=journal['v100'][0]['_']
                journal_issn=journal['issns'][0]
                journals_in_collection[journal_issn]=journal_name
        return journals_in_collection, len(journals_in_collection.keys())

    def update_status(self,code_article,dl_articles):
        """
        This method updates articles downloaded status list for a specific collection.
        The list is saved as text file.
        """
        dl_articles.append(code_article)
        with open('status-bk2.txt', 'w') as f:
            f.write(json.dumps(dl_articles))

    def check_status(self):
        """
        This method checks the status for downloaded articles for a specific collection
        to avoid repeats objects in the collection; if the collection is empty,
        creates a list to save the downloaded article code id.
        """
        documents_count=self.db['stage'].count_documents({})
        if documents_count==0:
            dl_articles=[]
            print("Empty collection.")
            return dl_articles
        else:
            with open('status-bk2.txt', 'r') as f:
                dl_articles=json.loads(f.read())
                if len(dl_articles) < documents_count:
                    dl_articles=[]
                    print("Incomplete downloaded list. Building downloaded status for articles in collection.")
                    for article in self.db['stage'].find():
                        code_article=article['code']
                        dl_articles.append(code_article)
                    print("Number of documents: {}").format(documents_count)
                    return dl_articles
                else:
                    print("No empty collection. Number of documents: {}".format(documents_count))
                    return dl_articles

    def get_articles(self):
        """
        Gets raw data of articles from Scielo. A journal identification is added in data to
        relate articles belong from each journal.
        """
        cursor = self.db['journals'].find(no_cursor_timeout=True)
        for journal in cursor:
            if journal['dl_status']==1:
                continue
            else:
                issn=journal['issns'][0]
                code_collection=journal['collection']
                documents=self.scielo_client.documents(code_collection,issn)
                dl_articles=self.check_status()
                for article in documents:
                    code_article=article.data['code']
                    if code_article in dl_articles:
                        continue
                    else:
                        article.data['journal_id']=journal['_id']
                        self.db['stage'].insert_one(article.data)
                        self.update_status(code_article,dl_articles)
            journal['dl_status']=1
