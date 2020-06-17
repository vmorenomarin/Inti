

from moai.MA.MAMagBase import MAMagBase
import logging

class MaMagLoader:
    def __init__(self,mag_dir,database_name,sep='\t', buffer_size=1024*1024, dburi='mongodb://localhost:27017/', hunabku_server = None, hunabku_apikey = None,
                 log_file='gsma.log', info_level=logging.DEBUG):

        self.AffiliationsColNames = ['AffiliationId', 'Rank', 'NormalizedName', 'DisplayName', 'GridId', 'OfficialPage', 'WikiPage', 'PaperCount', 'PaperFamilyCount', 'CitationCount', 'Latitude', 'Longitude', 'CreatedDate']
        self.AffiliationsColIndexes = ['AffiliationId','GridId']
        self.Affiliations = MAMagBase(mag_dir+'/Affiliations.txt',database_name,self.AffiliationsColNames,self.AffiliationsColIndexes,sep, buffer_size, dburi, hunabku_server, hunabku_apikey,log_file, info_level)

