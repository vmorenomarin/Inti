from moai.MA.MAMagBase import MAMagBase
import logging



class MAMagAffiliations(MAMagBase):
    def __init__(self,file_name,database_name,col_names,col_indexes,sep='\t', buffer_size=1024*1024, dburi='mongodb://localhost:27017/', hunabku_server = None, hunabku_apikey = None,
                 log_file='gsma.log', info_level=logging.DEBUG):
        super().__init__(file_name=file_name,database_name=database_name,col_names=col_names,col_indexes=col_indexes,sep=sep,buffer_size=buffer_size,dburi=dburi,hunabku_server=hunabku_server,hunabku_apikey=hunabku_apikey,log_file=log_file,info_level=info_level)
        self.collection = self.db['Affiliations']



    