import sys, os
from geo.Geoserver import Geoserver

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from log.logger import Logger

class GeoserverRestAPIGenerator():
    def __init__(
            self
            , geoserverAuth
            , geoserverFileBaseInputDir
        ):
        self.geoserverAuth = geoserverAuth
        self.geoserverFileBaseInputDir = geoserverFileBaseInputDir
        pass

    def test(self):
        '''
        Tutorial for geoserver-rest library
        
        ref: https://geoserver-rest.readthedocs.io/en/latest/how_to_use.html
        '''
        
        logger = Logger()
        
        geoserverAuth = self.geoserverAuth
        geoserverFileBaseInputDir = self.geoserverFileBaseInputDir


        '''
        Getting started with geoserver-rest
        '''
        geo = Geoserver(
            geoserverAuth['geoserverUrl']
            , geoserverAuth['geoserverUser']
            , geoserverAuth['geoserverPassword']
        )


        '''
        Creating workspaces
        '''
        workspaceNm = 'demo'
        
        # # get workspace list
        # logger.writeLog(f'workspace : {geo.get_workspaces()}')

        # # Check if the workspace already exists
        if not geo.get_workspace(f'{workspaceNm}'):
            logger.writeLog(f'{workspaceNm} workspace is not exist.')
            geo.create_workspace(f'{workspaceNm}')
            logger.writeLog(f'{workspaceNm} workspace is created.')
        else:
            logger.writeLog(f'{workspaceNm} workspace is already exist.')
        # logger.writeLog(f'workspace : {geo.get_workspace("demo")}')




        dataStoreNm = 'lst_sample_1'

        # # get all the datastores
        # logger.writeLog(f'datastore : {geo.get_datastores()}')

        # # get dataStoreNm datastore
        dataStore = geo.get_datastores(workspace= workspaceNm)
        # logger.writeLog(dataStore['dataStores'])

        # # # Check if the datastore already exists (dataStore var is blank)
        if not dataStore['dataStores']:
            logger.writeLog(f'{dataStoreNm} datastore is not exist.')
            geo.create_datastore(
                workspace= workspaceNm
                , name= dataStoreNm
                , path= f'{geoserverFileBaseInputDir}lst_sample_1/'
            )
            logger.writeLog(f'{dataStoreNm} datastore is created.')
        else:
            logger.writeLog(f'{dataStoreNm} datastore is already exist.')



