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
    """
    WMS Publish Generator
    ##TODO: 변수명 정리, 프로세스 정리
    1. Add workspace
    2. Add data store
    3. Publish WMS to Geoserver
    """
    def __init__(self, geoServerProjectInputPath):
        self.inputPath = geoServerProjectInputPath

        # # GeoServer API Config
        self.geoServerApiConfig = {
            'baseUrl': "http://localhost:8080/geoserver"
            , 'auth': ('admin', 'geoserver')
            , 'workspace': 'dbkim'
            , 'dataStore': 'testDataStore'
        }


    def getWMSLayer(self):
        logger = Logger()
        logger.writeLog('Start get WMS Layer')

        geoServerApiConfig = self.geoServerApiConfig

        geoServerApiConfig['dataStore'] = 'geoserverWebInterfaceV1'
        geoServerApiConfig['layer'] = 'ctp_rvn'

        bbox = "746110.2599834986,1458754.0441563274,1387949.5927430664,2068443.9546290152" # minx, miny, maxx, maxy
        srs = 'EPSG:5179'
        width = 768 #256
        height = 729 #256
        
        url = f'''
            {geoServerApiConfig['baseUrl']}
            /{geoServerApiConfig['workspace']}
            /wms
            ?service=WMS
            &version=1.1.0
            &request=GetMap
            &layers={geoServerApiConfig['layer']}
            &bbox={bbox}
            &width={width}
            &height={height}
            &srs={srs}
            &styles=
            &format=image/png
        '''.replace('\n', '').replace(' ', '')
        
        # 용산역 히트맵 test api
        # url = f"https://data.seoul.go.kr/SeoulRtd/heatmap_api?hotspotNm=용산역&baseDate=20221230&timeCd=1735&minX=126.94672645688983&minY=37.524660454413855&maxX=126.9658276704073&maxY=37.534464967056806&width=847&height=577&format=image/png"

        # # Get WMS Layer and format is PNG
        logger.writeLog(url)
        response = requests.get(url)
        
        logger.writeLog(f'response status code : {response.status_code}')
        if response.status_code == 200:
            logger.writeLog('WMS Layer Get Success')

            image_data = response.content

            # Save the image data to a file
            with open("image2.png", "wb") as f:
                f.write(image_data)

    def getSeoulRtd(self):
        logger = Logger()
        hotsportNm = '용산역'
        baseDate = '20221230'
        # timeCd = '1740'
        # timeCd = '0000'

        # # time data list
        # # 00시 00분 ~ 23시 55분 (5분 단위)
        timeCdList = []
        for i in range(0, 24):
            for j in range(0, 60, 5):
                timeCd = f'{str(i).zfill(2)}{str(j).zfill(2)}'
                timeCdList.append(timeCd)

        # timeCdList = ['0000', '0005']

        for timeCd in timeCdList:
            url = f'''
                https://data.seoul.go.kr/SeoulRtd/heatmap_api
                ?hotspotNm={hotsportNm}
                &baseDate={baseDate}
                &timeCd={timeCd}
                &minX=126.94672645688983
                &minY=37.524660454413855
                &maxX=126.9658276704073
                &maxY=37.534464967056806
                &width=847
                &height=577
                &format=image/png
            '''.replace('\n', '').replace(' ', '')

            # # Get WMS Layer and format is PNG
            # logger.writeLog(url)
            response = requests.get(url)
            
            # logger.writeLog(f'response status code : {response.status_code}')
            if response.status_code == 200:
                # logger.writeLog('WMS Layer Get Success')

                image_data = response.content
                
                # # 사진 left-bottom 에 heatmap_{hotsportNm}_{baseDate}_{timeCd}  표시 # 인코딩은 utf-8로
                image = Image.open(BytesIO(image_data))
                draw = ImageDraw.Draw(image)
                font = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 20)
                draw.text(
                    (0, 0) # x, y
                    # , f'heatmap_{hotsportNm}_{baseDate}_{timeCd}' # text
                    , f'heatmap_yongsan_{baseDate}_{timeCd}' # text # FIXME: 한글명이 깨짐
                    , (255, 255, 255) # color
                    , font=font # font
                )
                image_data = BytesIO()
                image.save(image_data, format='PNG')
                image_data = image_data.getvalue()

                # Save the image data to a file
                with open(f"figure/heatmap_fig_v4/heatmap_{hotsportNm}_{baseDate}_{timeCd}.png", "wb") as f:
                    f.write(image_data)

        # # Save the image data to a gif file
        with imageio.get_writer(f'figure/heatmap_fig_v4/heatmap_{hotsportNm}_{baseDate}.gif', mode='I') as writer:
            for timeCd in timeCdList:
                image = imageio.imread(f'figure/heatmap_fig_v4/heatmap_{hotsportNm}_{baseDate}_{timeCd}.png')
                writer.append_data(image)




    # def publishWMSToGeoserver(self):
    #     """
    #     Publish WMS To Geoserver
    #     GeoServer REST API
    #     """
    #     logger = Logger()
    #     logger.writeLog('Start publish WMS to Geoserver')

    #     dataInputPath = self.inputPath

    #     base_url = "http://localhost:8080/geoserver/rest"
    #     # # Define the authentication credentials for the GeoServer REST API
    #     auth = ("admin", "geoserver")
    #     # # Define the name of the workspace where you want to publish the WMS layer
    #     workspace = "dbkim"
    #     # # Define the name of the WMS layer you want to publish
    #     wms_layer_name = "testlayer"
    #     # # Define the data store that contains the WMS layer
    #     data_store_name = "testDataStore"
    #     # # Define the name of the style you want to apply to the WMS layer
    #     style_name = "my_style"
    #     # # Create a JSON payload with the details of the WMS layer
    #     payload = {
    #         "layer": {
    #             "name": wms_layer_name,
    #             "nativeName": wms_layer_name,
    #             "type": "VECTOR",
    #             "enabled": "true",
    #             "defaultStyle": {
    #                 "name": style_name
    #             },
    #             "store": {
    #                 "name": data_store_name,
    #                 "workspace": workspace
    #             }
    #         }
    #     }
    #     # # Send a POST request to the GeoServer REST API to create the WMS layer
    #     url = f"{base_url}/workspaces/{workspace}/datastores/{data_store_name}/featuretypes"

    #     response = requests.post(url, auth=auth, json=payload)

    #     if response.status_code == 201:
    #         print("WMS layer successfully published")
    #     else:
    #         print("Error publishing WMS layer")


    #     # # This should publish the WMS layer to GeoServer. You can then access the WMS layer using the following URL:
    #     '''
    #     http://localhost:8080/geoserver/wms
    #     ?service=WMS
    #     &version=1.1.0
    #     &request=GetMap
    #     &layers=my_workspace:my_wms_layer
    #     &styles=my_style
    #     &bbox=-180,-90,180,90
    #     &width=768
    #     &height=385
    #     &srs=EPSG:4326
    #     &format=application/openlayers
    #     '''


    # def setDataStorePath(self):
    #     logger = Logger()
    #     logger.writeLog('Start set data store path')

    #     dataInputPath = self.inputPath

    #     base_url = "http://localhost:8080/geoserver/rest"
    #     # # Define the authentication credentials for the GeoServer REST API
    #     auth = ("admin", "geoserver")
    #     # # Define the name of the workspace where you want to publish the WMS layer
    #     workspace = "dbkim"
    #     # # Define the data store that contains the WMS layer
    #     data_store_name = "test_data_store"
    #     data_store_path = f"{dataInputPath}/ctp_rvn.shp"
    #     url = f"{base_url}/workspaces/{workspace}/datastores/{data_store_name}.json"

    #     response = requests.get(url, auth=auth)

    #     if response.status_code == 200:
    #         data_store = response.json()
    #         logger.writeLog(data_store)
    #     else:
    #         logger.writeLog(response.status_code)
    #         logger.writeLog("Error retrieving data store")

    #     data_store["dataStore"]["connectionParameters"]["path"] = data_store_path

    #     url = f"{base_url}/workspaces/{workspace}/datastores/{data_store_name}"

    #     response = requests.put(url, auth=auth, json=data_store)

    #     if response.status_code == 200:
    #         print("Data store path successfully set")
    #     else:
    #         print("Error setting data store path")


    # def addDataStore(self):
    #     logger = Logger()
    #     logger.writeLog('Start add data store')
    #     dataPath  = self.inputPath

    
    #     baseUrl = "http://localhost:8080/geoserver/rest"
    #     auth = ("admin", "geoserver")
    #     workspace = "dbkim"
    #     dataStoreName = "test_data_store"
    #     dataStoreType = "shapefile"
    #     connectionParameters = {
    #         "url": f"file:{dataPath}",
    #         "namespace": "http://example.com/namespace"
    #     }

    #     payload = {
    #         "dataStore": {
    #             "name": dataStoreName,
    #             "type": dataStoreType,
    #             "enabled": True,
    #             "workspace": {
    #                 "name": workspace
    #             },
    #             "connectionParameters": connectionParameters
    #         }
    #     }

    #     url = f"{baseUrl}/workspaces/{workspace}/datastores"

    #     # # FIXME: 예외 처리 및 케이스 정리. dataStore가 있을 경우, 없을 경우
    #     response = requests.post(url, auth=auth, json=payload)

    #     if response.status_code == 201:
    #         logger.writeLog("Data store successfully added")
    #     else:
    #         logger.writeLog("Error adding data store")

    #     response = requests.get(url, auth=auth)
    #     if response.status_code == 200:
    #         data_store = response.json()
    #         logger.writeLog(data_store)

        
    #     ##TODO: 코드 분석. openGPT 소스 예시 -- 시작
    #     # To create a Python code that checks if a datastore exists in GeoServer and adds it if it does not, you can use the GeoServer REST API and the requests library in Python.

    #     # Here is an example of how you could do this:
    #     import requests

    #     # Set the base URL for the GeoServer REST API
    #     base_url = "http://localhost:8080/geoserver/rest"

    #     # Set the name of the datastore you want to check for and add
    #     datastore_name = "my_datastore"

    #     # Set the user name and password for your GeoServer instance
    #     username = "admin"
    #     password = "geoserver"

    #     # Check if the datastore exists by sending a GET request to the datastore resource
    #     url = f"{base_url}/workspaces/my_workspace/datastores/{datastore_name}.json"
    #     response = requests.get(url, auth=(username, password))

    #     # If the datastore does not exist, add it by sending a POST request to the datastores resource
    #     if response.status_code == 404:
    #         # Set the payload for the POST request
    #         data = """
    #         <dataStore>
    #         <name>{}</name>
    #         <connectionParameters>
    #             <entry key="ConnectionURL">file:data/{}</entry>
    #             <entry key="create">true</entry>
    #         </connectionParameters>
    #         </dataStore>
    #         """.format(datastore_name, datastore_name)
    #         headers = {"Content-Type": "text/xml"}
    #         url = f"{base_url}/workspaces/my_workspace/datastores"
    #         response = requests.post(url, data=data, headers=headers, auth=(username, password))

    #     # Check the response status code to see if the request was successful
    #     if response.status_code == 201:
    #         print("Datastore added successfully")
    #     else:
    #         print("Error adding datastore")

    #     # In this example, the code sends a GET request to the datastore resource for the specified datastore name to check if it exists. 
    #     # If the datastore does not exist (i.e. if the response status code is 404), the code sends a POST request to the datastores resource to add the datastore. 
    #     # The payload for the POST request specifies the name of the datastore and the connection parameters for the datastore.

    #     # You can customize this code to fit your specific needs by changing the base URL, the datastore name, the user name and password, and the connection parameters for the datastore. 
    #     # You may also need to modify the code to handle other response status codes and handle errors appropriately.
    #     ##TODO: 코드 분석. openGPT 소스 예시 -- 끝




