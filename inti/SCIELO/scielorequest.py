"""Coded by: Victor Moreno Marin."""

from pymongo import MongoClient
from articlemeta.client import RestfulClient


class ScieloRequest:
    """Requests class to build a SciELO database."""

    def __init__(self, db='scielo-test', host=None,):
        """
        Build a database with three collections.

        'collections' (mainly countries), 'journals' and 'stage' that
        contains articles data.
        The class methods use the SciELO API to get database documents.
        """
        self.client = MongoClient(host)
        self.db = self.client[db]
        self.scielo_client = RestfulClient()

    def get_collections(self):
        """Get collections from SciELO database."""
        collections = self.scielo_client.collections()
        for collection in collections:
            self.db['collections'].insert_one(collection)

    def list_collections(self):
        """
        List database SciELO collections.

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
        """
        Get raw data of journals from SciELO.

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
        """
        List database SciELO collections.

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
        """
        Check downloaded journals.

        This method verifies which journals have been downloaded
        before continues downloading SciELO articles.

        If all journal articles have been downloaded,
        this method avoid includes this journal in downloadable
        journals and avoid repeated documents in articles collection.
        """
        data = []
        cursor = self.db['cache'].find({'downloaded': 0})
        for cache_item in cursor:
            jrl_list = cache_item['id_journal']
            data.append(jrl_list)
        return data

    def update_cache(self, id_journal):
        """
        Update downloaded status.

        This method updates download status key to one when a
        journal has been completelly downloaded.

        args:
            id_journal: ObjectId for not downloaded journal.
        """
        cursor = self.db['cache'].find({'id_journal': id_journal})
        for cache_item in cursor:
            _id = cache_item['_id']
        new_data = {'id_journal': id_journal, 'downloaded': 1}
        self.db['cache'].update_one({'_id': _id}, {"$set": new_data})

    def delete_articles(self, id_journal):
        """
        Delete articles from an imcomplete downloaded journal.

        The articles are delete in stage collection.

        args:
            id_journal: ObjectId for not downloaded journal.
        """
        cursor = self.db['stage'].find({'id_journal': id_journal})
        if cursor:
            for article in cursor:
                article_id = article['_id']
                self.db['stage'].delete_one({'_id': article_id})
        else:
            pass

    def fix_cache(self):
        """
        Re-build cache collecion.

        If there are downloaded articles and cache collection
        all journals appear as not-downloaded, this method updates
        the cache with the correct values.
        """
        journal_id_list = []
        cursor = self.db['cache'].find()
        for article in cursor:
            journal_id_list.append(article['journal_id'])
        unique_jrl = set(journal_id_list)
        for jrl in unique_jrl:
            self.update_cache(jrl)

    def get_articles(self):
        """
        Get raw data of articles from Scielo.

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
                self.update_cache(id_journal)
            else:
                continue
