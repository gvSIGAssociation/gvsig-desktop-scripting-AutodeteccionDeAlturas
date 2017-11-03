
from gvsig import *
from org.gvsig.raster.impl.datastruct import DefaultNoData

def main(*args):

    #Remove this lines and add here your code

    print "Raster"
    
    raster = currentLayer()
    print "Extent X: ", raster.getMaxX(), raster.getMinX()
    print "Extent Y: ", raster.getMaxY(), raster.getMinY()
    print "CellSize: ", raster.getCellSize()
    print raster, type(raster)
    store = raster.getDataStore()
    print store
    print "Bandas: ", store.getBands()
    print "BandaDefault: ", store.getDefaultBandList()
    print "BandCoundyProvider: ", store.getBandCountByProvider()
    print "Ancho: ", store.getWidthByProvider()
    print "Alto: ", store.getHeightByProvider()

    print "Point 10, 10: ", store.getData(10, 10, 0)
    print "Point 0, 0: ", store.getData(0, 0, 0)

    """
        from org.gvsig.fmap.dal import DALLocator
        from org.gvsig.fmap.mapcontext import MapContextLocator
        from java.io import File
              dalManager = gvsig.DALLocator.getDataManager()
          mapContextManager = gvsig.MapContextLocator.getMapContextManager()
          params = dalManager.createStoreParameters("Gdal Store")
          params.setFile(File(value.getFilename()))
          dataStore = dalManager.createStore(params)
          layer = mapContextManager.createLayer(value.getName(), dataStore)
    """
    #newraster = raster.cloneLayer()
    #currentView().addLayer(newraster)

    nodata2 = DefaultNoData()
    nodata2.setValue(0.0)
    print nodata2, type(nodata2), type(raster)
    print "--- tesing: new nodata: ", nodata2.getValue()
    print "--- testing: nodata: ", raster.getNoDataValue().getValue()
    raster.setNoDataValue(nodata2)
    raster.setNoDataTransparent(True)
    mpx = currentView().getMapContext()
    print type(mpx), dir(mpx)
    
    return
    #update viewcontext
    mctx = currentView().getMapContext()
    print mctx, type(mctx)