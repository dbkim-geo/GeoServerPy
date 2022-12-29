from osgeo import gdal, osr, ogr
import numpy as np
from numpy import log as ln
from sklearn.cluster import DBSCAN
import pandas as pd
import os, sys
import math
import matplotlib.pyplot as plt
from tqdm import tqdm
import json
import requests
from contextlib import contextmanager

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from log.logger import Logger

class WMSPublishGenerator():
    def __init__(self, geoServerProjectInputPath):
        self.inputPath = geoServerProjectInputPath


    def publishWMSToGeoserver(self):
        """
        Publish WMS To Geoserver
        GeoServer REST API
        """
        logger = Logger()
        logger.writeLog('Start publish WMS to Geoserver')

        dataInputPath = self.inputPath

        base_url = "http://localhost:8080/geoserver/rest"
        # # Define the authentication credentials for the GeoServer REST API
        auth = ("admin", "geoserver")
        # # Define the name of the workspace where you want to publish the WMS layer
        workspace = "dbkim"
        # # Define the name of the WMS layer you want to publish
        wms_layer_name = "testlayer"
        # # Define the data store that contains the WMS layer
        data_store_name = "testDataStore"
        # # Define the name of the style you want to apply to the WMS layer
        style_name = "my_style"
        # # Create a JSON payload with the details of the WMS layer
        payload = {
            "layer": {
                "name": wms_layer_name,
                "nativeName": wms_layer_name,
                "type": "VECTOR",
                "enabled": "true",
                "defaultStyle": {
                    "name": style_name
                },
                "store": {
                    "name": data_store_name,
                    "workspace": workspace
                }
            }
        }
        # # Send a POST request to the GeoServer REST API to create the WMS layer
        url = f"{base_url}/workspaces/{workspace}/datastores/{data_store_name}/featuretypes"

        response = requests.post(url, auth=auth, json=payload)

        if response.status_code == 201:
            print("WMS layer successfully published")
        else:
            print("Error publishing WMS layer")


        # # This should publish the WMS layer to GeoServer. You can then access the WMS layer using the following URL:
        '''
        http://localhost:8080/geoserver/wms
        ?service=WMS
        &version=1.1.0
        &request=GetMap
        &layers=my_workspace:my_wms_layer
        &styles=my_style
        &bbox=-180,-90,180,90
        &width=768
        &height=385
        &srs=EPSG:4326
        &format=application/openlayers
        '''


    def setDataStorePath(self):
        logger = Logger()
        logger.writeLog('Start set data store path')

        dataInputPath = self.inputPath

        base_url = "http://localhost:8080/geoserver/rest"
        # # Define the authentication credentials for the GeoServer REST API
        auth = ("admin", "geoserver")
        # # Define the name of the workspace where you want to publish the WMS layer
        workspace = "dbkim"
        # # Define the data store that contains the WMS layer
        data_store_name = "testDataStore"
        data_store_path = f"{dataInputPath}/testDataStore.shp"
        # url = f"{base_url}/workspaces/{workspace}/datastores/{data_store_name}.json"
        url = f"{base_url}/workspaces/{workspace}.json"

        # # Add shp datastore
        payload = {
            "dataStore": {
                "name": data_store_name,
                "type": "Shapefile",
                "enabled": "true",
                "workspace": {
                    "name": workspace
                },
                "connectionParameters": {
                    "entry": [
                        {
                            "@key": "create spatial index",
                            "$": "true"
                        },
                        {
                            "@key": "charset",
                            "$": "UTF-8"
                        },
                        {
                            "@key": "url",
                            "$": f"file:{data_store_path}"
                        }
                    ]
                }
            }
        }


        response = requests.post(url, auth=auth, json=payload)


        # response = requests.get(url, auth=auth)

        if response.status_code == 200:
            data_store = response.json()
            logger.writeLog(data_store)
        else:
            logger.writeLog(response.status_code)
            logger.writeLog("Error retrieving data store")

        # data_store["dataStore"]["connectionParameters"]["path"] = data_store_path

        # url = f"{base_url}/workspaces/{workspace}/datastores/{data_store_name}"

        # response = requests.put(url, auth=auth, json=data_store)

        # if response.status_code == 200:
        #     print("Data store path successfully set")
        # else:
        #     print("Error setting data store path")


    def addDataStore(self):
        logger = Logger()
        logger.writeLog('Start add data store')
        dataPath  = self.inputPath

    
        base_url = "http://localhost:8080/geoserver/rest"
        auth = ("admin", "geoserver")
        workspace = "dbkim"
        data_store_name = "test_data_store"
        data_store_type = "shapefile"
        connection_parameters = {
            "url": f"file:{dataPath}",
            "namespace": "http://example.com/namespace"
        }

        payload = {
            "dataStore": {
                "name": data_store_name,
                "type": data_store_type,
                "enabled": True,
                "workspace": {
                    "name": workspace
                },
                "connectionParameters": connection_parameters
            }
        }

        url = f"{base_url}/workspaces/{workspace}/datastores"

        response = requests.post(url, auth=auth, json=payload)

        if response.status_code == 201:
            logger.writeLog("Data store successfully added")
        else:
            logger.writeLog("Error adding data store")

        response = requests.get(url, auth=auth)
        if response.status_code == 200:
            data_store = response.json()
            logger.writeLog(data_store)
        # # FIXME: 변수 명 리팩터링
