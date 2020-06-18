

from inti.MA.MAMagBase import MAMagBase
import logging

class MAMagLoader:
    def __init__(self,mag_dir,database_name,sep='\t', buffer_size=1024*1024, dburi='mongodb://localhost:27017/', hunabku_server = None, hunabku_apikey = None,
                 log_file='mamagloader.log', info_level=logging.DEBUG):
        """
        Class to load the different files from mag directory,
        the directory should have the next files
        mag/PaperAuthorAffiliations.txt
        mag/ConferenceSeries.txt
        mag/Affiliations.txt
        mag/PaperUrls.txt
        mag/Papers.txt
        mag/PaperResources.txt
        mag/ConferenceInstances.txt
        mag/Authors.txt
        mag/PaperReferences.txt
        mag/PaperExtendedAttributes.txt
        mag/Journals.txt

        by default the method run, execute the code to load all the files,
        you can to specify the file, given the argument to the methdo run, lets see run documentation for more details.
        """
        self.instances = {}

        self.authors_col_names = ['AuthorId', 'Rank', 'NormalizedName', 'DisplayName', 'LastKnownAffiliationId', 'PaperCount', 'PaperFamilyCount', 'CitationCount', 'CreatedDate']
        self.authors_col_indexes = ['AuthorId','LastKnownAffiliationId']
        self.instances['Authors'] = MAMagBase(mag_dir+'/Authors.txt',database_name,'Authors',self.authors_col_names,self.authors_col_indexes,sep, buffer_size, dburi, hunabku_server, hunabku_apikey,log_file, info_level)

        self.affiliations_col_names = ['AffiliationId', 'Rank', 'NormalizedName', 'DisplayName', 'GridId', 'OfficialPage', 'WikiPage', 'PaperCount', 'PaperFamilyCount', 'CitationCount', 'Latitude', 'Longitude', 'CreatedDate']
        self.affiliations_col_indexes = ['AffiliationId','GridId']
        self.instances['Affiliations'] = MAMagBase(mag_dir+'/Affiliations.txt',database_name,'Affiliations',self.affiliations_col_names,self.affiliations_col_indexes,sep, buffer_size, dburi, hunabku_server, hunabku_apikey,log_file, info_level)

        self.paper_author_affiliations_col_names = ['PaperId', 'AuthorId', 'AffiliationId', 'AuthorSequenceNumber', 'OriginalAuthor', 'OriginalAffiliation']
        self.paper_author_affiliations_col_indexes = ['PaperId','AuthorId','AffiliationId']
        self.instances['PaperAuthorAffiliations'] = MAMagBase(mag_dir+'/PaperAuthorAffiliations.txt',database_name,'PaperAuthorAffiliations',self.paper_author_affiliations_col_names,self.paper_author_affiliations_col_indexes,sep, buffer_size, dburi, hunabku_server, hunabku_apikey,log_file, info_level)

        self.papers_col_names = ['PaperId', 'Rank', 'Doi', 'DocType', 'PaperTitle', 'OriginalTitle', 'BookTitle', 'Year', 'Date', 'Publisher', 'JournalId', 'ConferenceSeriesId', 'ConferenceInstanceId', 'Volume', 'Issue', 'FirstPage', 'LastPage', 'ReferenceCount', 'CitationCount', 'EstimatedCitation', 'OriginalVenue', 'FamilyId', 'CreatedDate']
        self.papers_col_indexes = ['PaperId','JournalId','ConferenceSeriesId','ConferenceInstanceId','FamilyId']
        self.instances['Papers'] = MAMagBase(mag_dir+'/Papers.txt',database_name,'Papers',self.papers_col_names,self.papers_col_indexes,sep, buffer_size, dburi, hunabku_server, hunabku_apikey,log_file, info_level)

        self.paper_urls_col_names = ['PaperId', 'SourceType', 'SourceUrl', 'LanguageCode']
        self.paper_urls_col_indexes = ['PaperId']
        self.instances['PaperUrls'] = MAMagBase(mag_dir+'/PaperUrls.txt',database_name,'PaperUrls',self.paper_urls_col_names,self.paper_urls_col_indexes,sep, buffer_size, dburi, hunabku_server, hunabku_apikey,log_file, info_level)

        self.paper_resources_col_names = ['PaperId', 'ResourceType', 'ResourceUrl', 'SourceUrl', 'RelationshipType']
        self.paper_resources_col_indexes = ['PaperId']
        self.instances['PaperResources'] = MAMagBase(mag_dir+'/PaperResources.txt',database_name,'PaperResources',self.paper_resources_col_names,self.paper_resources_col_indexes,sep, buffer_size, dburi, hunabku_server, hunabku_apikey,log_file, info_level)

        self.paper_references_col_names = ['PaperId', 'PaperReferenceId']
        self.paper_references_col_indexes = ['PaperId', 'PaperReferenceId']
        self.instances['PaperReferences'] = MAMagBase(mag_dir+'/PaperReferences.txt',database_name,'PaperReferences',self.paper_references_col_names,self.paper_references_col_indexes,sep, buffer_size, dburi, hunabku_server, hunabku_apikey,log_file, info_level)
                
        self.paper_extended_attributes_col_names = ['PaperId', 'AttributeType', 'AttributeValue']
        self.paper_extended_attributes_col_indexes = ['PaperId']
        self.instances['PaperExtendedAttributes'] = MAMagBase(mag_dir+'/PaperExtendedAttributes.txt',database_name,'PaperExtendedAttributes',self.paper_extended_attributes_col_names,self.paper_extended_attributes_col_indexes,sep, buffer_size, dburi, hunabku_server, hunabku_apikey,log_file, info_level)

        self.journals_col_names = ['JournalId', 'Rank', 'NormalizedName', 'DisplayName', 'Issn', 'Publisher', 'Webpage', 'PaperCount', 'PaperFamilyCount', 'CitationCount', 'CreatedDate']
        self.journals_col_indexes = ['JournalId']
        self.instances['Journals'] = MAMagBase(mag_dir+'/Journals.txt',database_name,'Journals',self.journals_col_names,self.journals_col_indexes,sep, buffer_size, dburi, hunabku_server, hunabku_apikey,log_file, info_level)

        self.conference_series_col_names = ['ConferenceSeriesId', 'Rank', 'NormalizedName', 'DisplayName', 'PaperCount', 'PaperFamilyCount', 'CitationCount', 'CreatedDate']
        self.conference_series_col_indexes = ['ConferenceSeriesId']
        self.instances['ConferenceSeries'] = MAMagBase(mag_dir+'/ConferenceSeries.txt',database_name,'ConferenceSeries',self.conference_series_col_names,self.conference_series_col_indexes,sep, buffer_size, dburi, hunabku_server, hunabku_apikey,log_file, info_level)

        self.conference_instances_col_names = ['ConferenceInstanceId', 'NormalizedName', 'DisplayName', 'ConferenceSeriesId', 'Location', 'OfficialUrl', 'StartDate', 'EndDate', 'AbstractRegistrationDate', 'SubmissionDeadlineDate', 'NotificationDueDate', 'FinalVersionDueDate', 'PaperCount', 'PaperFamilyCount', 'CitationCount', 'Latitude', 'Longitude', 'CreatedDate']
        self.conference_instances_col_indexes = ['ConferenceInstanceId','ConferenceSeriesId']
        self.instances['ConferenceInstances'] = MAMagBase(mag_dir+'/ConferenceInstances.txt',database_name,'ConferenceInstances',self.conference_instances_col_names,self.conference_instances_col_indexes,sep, buffer_size, dburi, hunabku_server, hunabku_apikey,log_file, info_level)

    def get_instance_keys(self):
        """
        return the instance keys
        """
        return self.instances.keys()

    def run(self,max_threads=None,instace=None):
        if instace is None:
            for i in self.instances.keys():
                self.instances[i].run(max_threads=max_threads)
        else:
            if instace in self.instances.keys():
                self.instances[instace].run(max_threads=max_threads)
         