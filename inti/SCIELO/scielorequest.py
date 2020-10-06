"""Created by: Victor Moreno Marin."""

from pymongo import MongoClient
from articlemeta.client import RestfulClient
import json


class ScieloRequest:
    """Requests class to build a SciELO database."""

    def __init__(self, database_name='scielo-test', host=None):
        """
        Build a database with three collections.

        'collections' (mainly countries), 'journals' and 'stage' that
        contains articles data.
        The class methods use the SciELO API to get database documents.
        """
        self.client = MongoClient(host)
        self.db = self.client[database_name]
        self.scielo_client = RestfulClient()

    def get_collections(self):
        """Get collections from SciELO database."""
        collections = self.scielo_client.collections()
        for collection in collections:
            self.db['collections'].insert_one(collection)

    def list_collections(self):
        """List database SciELO collections.

        Displays its name and alpha-3 code.
        """
        list_collections = []
        cursor = self.db["collections"].find()
        for collection in cursor:
            collection_code = collection['code']
            name = collection['name']['en']
            list_collections.append({name: collection_code})
        return list_collections

    def get_journals(self):
        """Get raw data of journals from SciELO.

        A collection identification id is added in data
        to relate journals belong from each collection.
        """
        cursor = self.db['collections'].find()
        for collection in cursor:
            collection_code = collection['code']
            for journal in self.scielo_client.journals(collection_code):
                journal.data['collection_id'] = collection['_id']
                self.db['journals'].insert_one(journal.data)

    def list_jornals_in_collection(self, collection_code):
        """List database SciELO collections.

        Returns a tuple with a dictionary
        that has ISSN code and journal name;
        the another object tuple's is the total journals number.

        args:
            collection_code: code from a specific SciELO collections.
        """
        journals_in_collection = {}
        for journal in self.db['journals'].find():
            if collection_code in journal['collection']:
                journal_name = journal['v100'][0]['_']
                journal_issn = journal['issns'][0]
                journals_in_collection[journal_issn] = journal_name
        return journals_in_collection, len(journals_in_collection.keys())

    def create_cache(self):
        """
        Create a cache.

        This method builds a collection to verifies full downloaded
        journals. If journal articles as not been downloaded or are
        incomplete, download status key has zero value.
        """
        cursor = self.db['journals'].find()
        data = {}
        for journal in cursor:
            id_journal = journal['_id']
            data = {'id_journal': id_journal, 'downloaded': 0}
            self.db['cache'].insert_one(data)

    def check_cache(self):
        """Check downloaded journals.

        This method verifies which journals have been downloaded
        before continues downloading SciELO articles.

        If all journal articles have been downloaded,
        this method avoid includes this journal in downloadable
        journals and avoid repeated documents in articles collection.
        """
        data = []
        list_id = []
        cursor = self.db['cache'].find()
        for cache_item in cursor:
            list_id.append(cache_item['_id'])
        for id_cache in list_id:
            for dl_jrl in self.db['cache'].find({'_id': id_cache},
                                                {'downloaded': 0}):
                jrl_list = dl_jrl['id_journal']
                data.append(jrl_list)
        return data

    def update_cache(self, id_journal, new_data):
        """Update downloaded status.

        This method updates download status key to one when a
        journal has been completelly downloaded.

        args:
            id_journal: ObjectId for not downloaded journal.
            new_data: new key value to 1 if journal has been downloaded.
        """
        cursor = self.db['cache'].find({'id_journal': id_journal})
        for cache_item in cursor:
            _id = cache_item['_id']
        self.db['cache'].update_one({'_id': _id}, {"$set": new_data})

    def delete_articles(self, id_journal):
        """Delete articles from an imcomplete downloaded journal.

        The articles are delete in stage collection.

        args:
            id_journal: ObjectId for not downloaded journal.
        """
        cursor = self.db['stage'].find()
        for article in cursor:
            if id_journal != article.data['id_journal']:
                continue
            else:
                article_id = article['_id']
                self.db['stage'].delete_one({'_id': article_id})

    def get_articles(self):
        """Get raw data of articles from Scielo.

        A journal identification is added in data to
        relate articles belong from each journal.
        """
        cursor = self.db['journals'].find(no_cursor_timeout=True)
        data = self.check_cache()
        for journal in cursor:
            id_journal = journal['_id']
            if id_journal in data:
                issn = journal['issns'][0]
                code_collection = journal['collection']
                self.delete_articles(id_journal)
                documents = self.scielo_client.documents(code_collection, issn)
                for article in documents:
                    article.data['id_journal'] = journal['_id']
                    self.db['stage'].insert_one(article.data)
                new_data = {'id_journal': id_journal, 'downloaded': 1}
                self.update_cache(id_journal, new_data)
            else:
                continue
