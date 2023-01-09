from osgeo import gdal, osr, ogr
import numpy as np
from numpy import log as ln
from sklearn.cluster import DBSCAN
import pandas as pd
import os, sys
import math
import matplotlib.pyplot as plt
from tqdm import tqdm
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import json
import requests
import imageio
from datetime import datetime
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
    def __init__(self, geoServerProjectInputPath, geoServerProjectFigurePath):
        self.inputPath = geoServerProjectInputPath
        self.figurePath = geoServerProjectFigurePath

        # # GeoServer API Config
        self.geoServerApiConfig = {
            'baseUrl': "http://localhost:8080/geoserver"
            , 'auth': ('admin', 'geoserver')
            , 'workspace': 'dbkim'
            , 'dataStore': 'testDataStore'
        }


    def getWMSLayer(self):
        '''
        Get WMS Layer

        GeoServer REST API
        png format으로 다운로드 받아줌
        # TODO: javascript로 렌더링 해서 보여주기
        '''
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
        ##TODO: heatmap api로 받아온 데이터를 geoserver에 올리기
        ##TODO: heatmap 말고 추가로 베이스맵도 뒤에다가 깔기
        logger = Logger()
        # timeStamp = datetime.now().strftime('%Y%m%d%H%M%S')
        # if not os.path.exists(f'{self.figurePath}/{timeStamp}'):
        #     os.makedirs(f'{self.figurePath}/{timeStamp}')



        # hotsportNm = '용산역'
        # baseDate = '20221230'
        # # timeCd = '1740'
        # # timeCd = '0000'

        # # # time data list
        # # # 00시 00분 ~ 23시 55분 (5분 단위)
        # # timeCdList = []
        # # for i in range(0, 24):
        # #     for j in range(0, 60, 5):
        # #         timeCd = f'{str(i).zfill(2)}{str(j).zfill(2)}'
        # #         timeCdList.append(timeCd)

        # timeCdList = ['0000', '0005']
        # timeCdList = ['0000']

        # for timeCd in timeCdList:
        #     url = f'''
        #         https://data.seoul.go.kr/SeoulRtd/heatmap_api
        #         ?hotspotNm={hotsportNm}
        #         &baseDate={baseDate}
        #         &timeCd={timeCd}
        #         &minX=126.94672645688983
        #         &minY=37.524660454413855
        #         &maxX=126.9658276704073
        #         &maxY=37.534464967056806
        #         &width=847
        #         &height=577
        #         &format=image/png
        #     '''.replace('\n', '').replace(' ', '')

        #     # # Get WMS Layer and format is PNG
        #     # logger.writeLog(url)
        #     response = requests.get(url)
            
        #     # logger.writeLog(f'response status code : {response.status_code}')
        #     if response.status_code == 200:
        #         # logger.writeLog('WMS Layer Get Success')

        #         image_data = response.content
                
                # # 사진 left-bottom 에 heatmap_{hotsportNm}_{baseDate}_{timeCd}  표시 # 인코딩은 utf-8로
                # image = Image.open(BytesIO(image_data))
                # draw = ImageDraw.Draw(image)
                # font = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 20)
                # draw.text(
                #     (0, 0) # x, y
                #     # , f'heatmap_{hotsportNm}_{baseDate}_{timeCd}' # text
                #     , f'heatmap_yongsan_{baseDate}_{timeCd}' # text # FIXME: 한글명이 깨짐
                #     , (255, 255, 255) # color
                #     , font=font # font
                # )
                # image_data = BytesIO()
                # image.save(image_data, format='PNG')
                # image_data = image_data.getvalue()

                # # 배경에는 vworld base layer를 깔기
                # # vworld base layer



                # # Save the image data to a file
                # with open(f"{self.figurePath}/{timeStamp}/heatmap_{hotsportNm}_{baseDate}_{timeCd}.png", "wb") as f:
                #     f.write(image_data)

        # # # Save the image data to a gif file
        # with imageio.get_writer(f'{self.figurePath}/{timeStamp}/heatmap_{hotsportNm}_{baseDate}.gif', mode='I') as writer:
        #     for timeCd in timeCdList:
        #         image = imageio.imread(f'{self.figurePath}/{timeStamp}/heatmap_{hotsportNm}_{baseDate}_{timeCd}.png')
        #         writer.append_data(image)


        # # Convert PNG to getTiff (EPSG:4326)
        # Open the PNG file using GDAL
        # png_ds = gdal.Open(f'{self.figurePath}/{timeStamp}/20230103105341/heatmap_용산역_20221230_0000.png')
        png_ds = gdal.Open(f'C:/Users/dongb/Desktop/dbkim/workspace/asset/dataset/GeoServerPy/figure/20230103111903/heatmap_용산역_20221230_0000.png')

        # Get the raster data from the PNG file
        raster_data = png_ds.ReadAsArray()

        # Get the geo-referencing information from the PNG file
        origin_x, pixel_width, _, origin_y, _, pixel_height = png_ds.GetGeoTransform()
        origin_x = 126.94672645688983
        origin_y = 37.534464967056806
        # # FIXME: lat lon to pixel....
        
        max_x = origin_x + png_ds.RasterXSize * pixel_width
        max_y = origin_y + png_ds.RasterYSize * pixel_height
        logger.writeLog(f'max_x : {max_x}')

        logger.writeLog(f'png_ds.GetGeoTransform() : {png_ds.GetGeoTransform()}')
        logger.writeLog(f'ds.GetProjectionRef() : {png_ds.GetProjectionRef()}')

        # # # Create a new GeoTiff file using GDAL
        # drv = gdal.GetDriverByName('GTiff')
        # geotiff_ds = drv.Create(
        #     # f'{self.figurePath}/{timeStamp}/20230103105341/test2.tif'
        #     f'C:/Users/dongb/Desktop/dbkim/workspace/asset/dataset/GeoServerPy/figure/20230103111903/test_b4.tif'
        #     , png_ds.RasterXSize
        #     , png_ds.RasterYSize
        #     , 1
        #     , gdal.GDT_Float32
        # )
        # logger.writeLog(f'geotiff_ds : {geotiff_ds}')

        # # # Set the geo-referencing information for the GeoTiff file
        # geotiff_ds.SetGeoTransform((
        #     origin_x, pixel_width, 0, origin_y, 0, pixel_height
        # ))

        # # # Set the projection for the GeoTiff file to EPSG:4326
        # srs = osr.SpatialReference()
        # srs.ImportFromEPSG(4326)
        # geotiff_ds.SetProjection(srs.ExportToWkt())

        # # # Write the raster data to the GeoTiff file
        # geotiff_ds.GetRasterBand(1).WriteArray(raster_data[3])

        # # # Close the GeoTiff file
        # geotiff_ds = None

        


    def getVworldWMS(self):
        # # TODO: vworld base layer를 png로 저장
        logger = Logger()
        logger.writeLog('Start get Vworld WMS Layer')
        
        privateKey = '7EC9ECCD-9F15-3466-8B72-E4A4653E51AD'

        url = f'''
            http://api.vworld.kr/req/wms
            ?service=WMS
            &request=GetMap
            &version=1.1.1
            &layers=LT_C_BAS
            &styles=
            &bbox=126.94672645688983,37.524660454413855,126.9658276704073,37.534464967056806
            &width=847
            &height=577
            &srs=EPSG:4326
            &format=image/png
            &transparent=true
            &key={privateKey}
        '''.replace('\n', '').replace(' ', '')

        logger.writeLog(url)
        response = requests.get(url)
        logger.writeLog(f'response status code : {response.status_code}')
        # if response.status_code == 200:

        #     image_data = response.content
        #     # Save the image data to a file
        #     with open("figure/vworld_wms.png", "wb") as f:
        #         f.write(image_data)




    def publishWMSToGeoserver(self):
        """
        Publish WMS To Geoserver
        GeoServer REST API
        """
        logger = Logger()
        logger.writeLog('Start publish WMS to Geoserver')

        dataInputPath = self.inputPath
        geoServerApiConfig = self.geoServerApiConfig

        geoServerApiConfig['dataStore'] = 'geoserverWebInterfaceV1'
        geoServerApiConfig['layer'] = 'ctp_rvn'

        base_url = "http://localhost:8080/geoserver/rest"
        # # Define the authentication credentials for the GeoServer REST API
        auth = ("admin", "geoserver")
        # # Define the name of the workspace where you want to publish the WMS layer
        workspace = "dbkim"
        # # Define the name of the WMS layer you want to publish
        wms_layer_name = "ctp_rvn"
        # # Define the data store that contains the WMS layer
        data_store_name = "geoserverWebInterfaceV1"
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
        url = f'''
            {geoServerApiConfig['baseUrl']}
            /workspaces
            /{geoServerApiConfig['workspace']}
            /datastores
            /{geoServerApiConfig['dataStore']}
            /featuretypes
        '''.replace('\n', '').replace(' ', '')

        logger.writeLog(url)

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


    def addDataStore(self):
        logger = Logger()
        logger.writeLog('Start add data store')
        dataPath  = self.inputPath

    
        baseUrl = "http://localhost:8080/geoserver/rest"
        auth = ("admin", "geoserver")
        workspace = "dbkim"
        dataStoreName = "test_data_store"
        dataStoreType = "shapefile"
        connectionParameters = {
            "url": f"file:{dataPath}",
            "namespace": "http://example.com/namespace"
        }

        payload = {
            "dataStore": {
                "name": dataStoreName,
                "type": dataStoreType,
                "enabled": True,
                "workspace": {
                    "name": workspace
                },
                "connectionParameters": connectionParameters
            }
        }

        url = f"{baseUrl}/workspaces/{workspace}/datastores"

        # # FIXME: 예외 처리 및 케이스 정리. dataStore가 있을 경우, 없을 경우
        response = requests.post(url, auth=auth, json=payload)

        if response.status_code == 201:
            logger.writeLog("Data store successfully added")
        else:
            logger.writeLog("Error adding data store")

        response = requests.get(url, auth=auth)
        if response.status_code == 200:
            data_store = response.json()
            logger.writeLog(data_store)

    def testDataStore(self):
        '''
        TODO:
        1. Add data store
        2. Add layer
        3. Publish layer
        '''


        logger = Logger()
        ##TODO: 코드 분석. openGPT 소스 예시 -- 시작
        # To create a Python code that checks if a datastore exists in GeoServer and adds it if it does not, you can use the GeoServer REST API and the requests library in Python.

        # Here is an example of how you could do this:
        # Set the base URL for the GeoServer REST API
        base_url = "http://localhost:8080/geoserver/rest"
        workspace = "dbkim"
        dataPath  = self.inputPath

        # Set the name of the datastore you want to check for and add
        datastore_name = "test_data_store_v1"

        # Set the user name and password for your GeoServer instance
        username = "admin"
        password = "geoserver"

        # Check if the datastore exists by sending a GET request to the datastore resource
        url = f"{base_url}/workspaces/{workspace}/datastores/{datastore_name}.json"
        response = requests.get(url, auth=(username, password))

        logger.writeLog(f'Check if the datastore exists by sending a GET request to the datastore resource: {response.status_code}')

        # If the datastore does not exist, add it by sending a POST request to the datastores resource
        if response.status_code == 404:
            # Set the payload for the POST request
            payload = {
                "dataStore": {
                    "name": datastore_name,
                    "type": "shapefile",
                    "enabled": True,
                    "workspace": {
                        "name": workspace
                    },
                    "connectionParameters": {
                        "url": f"file:{dataPath}ctp_rvn2.shp",
                        "namespace": "http://example.com/namespace"
                    }
                }
            }

            # Send the POST request to add the datastore
            url = f"{base_url}/workspaces/{workspace}/datastores"
            response = requests.post(url, auth=(username, password), json=payload)

        # Check the response status code to see if the request was successful
        if response.status_code == 201:
            logger.writeLog("Datastore added successfully")
        else:
            logger.writeLog(f"Error adding datastore : {response.status_code}")



        # Set the base URL of the GeoServer instance
        geoserver_url = "http://localhost:8080/geoserver"

        # Set the name of the workspace and datastore
        workspace_name = workspace

        # Set the name of the new layer
        layer_name = "ctp_rvn2"

        # Construct the URL for the POST request to add the layer
        url = f"{geoserver_url}/rest/workspaces/{workspace_name}/datastores/{datastore_name}/featuretypes"

        # Set the headers for the POST request
        headers = {
            "Content-Type": "application/json"
            , "Accept": "application/json"
        }

        # Set the payload for the POST request
        payload = {
            "layer": {
                "name": layer_name,
            }
        }
        # payload = {
        #     "featureType": {
        #         "name": layer_name,
        #     }
        # }


        # Make the POST request to add the layer
        response = requests.post(url, data=json.dumps(payload), headers=headers)
        logger.writeLog(f"Make the POST request to add the layer: {response.status_code}")

        # Check the response status code to make sure the request was successful
        if response.status_code == 201:
            print("Layer added successfully")
        else:
            print("Error adding layer")

        # Construct the URL for the PUT request to publish the layer
        url = f"{geoserver_url}/rest/layers/{workspace_name}:{layer_name}"

        # Set the payload for the PUT request
        payload = {
            "layer": {
                "enabled": True
            }
        }

        # Make the PUT request to publish the layer
        response = requests.put(url, data=json.dumps(payload), headers=headers)

        # Check the response status code to make sure the request was successful
        if response.status_code == 200:
            print("Layer published successfully")
        else:
            print("Error publishing layer")



        # In this example, the code sends a GET request to the datastore resource for the specified datastore name to check if it exists. 
        # If the datastore does not exist (i.e. if the response status code is 404), the code sends a POST request to the datastores resource to add the datastore. 
        # The payload for the POST request specifies the name of the datastore and the connection parameters for the datastore.

        # You can customize this code to fit your specific needs by changing the base URL, the datastore name, the user name and password, and the connection parameters for the datastore. 
        # You may also need to modify the code to handle other response status codes and handle errors appropriately.
        ##TODO: 코드 분석. openGPT 소스 예시 -- 끝




