from wms.wmsPublishGenerator import WMSPublishGenerator
from restapi.geoserverRestAPIGenerator import GeoserverRestAPIGenerator
from setting.configValue import ConfigValue
from custom.timer import Timer


def main():


    '''
    WMS publish generator
    '''
    # wmsPublishGenerator = WMSPublishGenerator(
    #     ConfigValue.geoServerProjectInputPath
    #     , ConfigValue.geoServerProjectFigurePath
    # )
    # wmsPublishGenerator.getWMSLayer()
    # wmsPublishGenerator.publishWMSToGeoserver()
    # wmsPublishGenerator.setDataStorePath()
    # wmsPublishGenerator.addDataStore()

    # wmsPublishGenerator.testDataStore()

    # wmsPublishGenerator.getSeoulRtd()
    # wmsPublishGenerator.getVworldWMS()

    '''
    GeoServer REST API generator
    '''
    geoserverRestAPIGenerator = GeoserverRestAPIGenerator(
        ConfigValue.geoserverAuth
        , ConfigValue.geoserverFileBaseInputDir
    )
    geoserverRestAPIGenerator.test()





if __name__ == '__main__':

    with Timer():
        main()