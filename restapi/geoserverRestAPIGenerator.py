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


        '''
        Creating coveragestores
        -- publishing the raster data to the geoserver
        '''
        lyrNm = 'lst_sample_1'
        # # get coveragestore list
        # logger.writeLog(f'coveragestore : {geo.get_coveragestores()}')

        if not geo.get_layer(layer_name=f'{lyrNm}'):
            logger.writeLog(f'{lyrNm} layer is not exist.')
            geo.create_coveragestore(
                layer_name=f'{lyrNm}'
                , path=f'{geoserverFileBaseInputDir}/lst_sample_1.tif'
                , workspace=f'{workspaceNm}'
            )
            logger.writeLog(f'{lyrNm} layer is created.')
        else:
            logger.writeLog(f'{lyrNm} layer is already exist.')
        