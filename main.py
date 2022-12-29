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
    # wmsPublishGenerator.publishWMSToGeoserver()
    wmsPublishGenerator.setDataStorePath()
    # wmsPublishGenerator.addDataStore()






if __name__ == '__main__':

    with Timer():
        main()