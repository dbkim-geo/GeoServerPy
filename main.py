from wms.wmsPublishGenerator import WMSPublishGenerator
from setting.configValue import ConfigValue
from custom.timer import Timer


def main():


    '''
    WMS publish generator
    '''
    wmsPublishGenerator = WMSPublishGenerator(
        ConfigValue.geoServerProjectInputPath
    )
    # wmsPublishGenerator.getWMSLayer()
    # wmsPublishGenerator.publishWMSToGeoserver()
    # wmsPublishGenerator.setDataStorePath()
    # wmsPublishGenerator.addDataStore()

    # wmsPublishGenerator.testDataStore()
    wmsPublishGenerator.getSeoulRtd()




if __name__ == '__main__':

    with Timer():
        main()