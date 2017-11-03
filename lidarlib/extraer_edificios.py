from gvsig import *

import gvsig.libs.gvpy
reload(gvsig.libs.gvpy)
from gvsig.libs import gvpy as g

from org.gvsig.raster.impl.datastruct import DefaultNoData
from gvsig.libs.timeit import timeit
import time

def expand_extend(layer, metros):
    env = layer.getFullEnvelope()
    x1,y1 = env.getLowerCorner().getX()-metros, env.getLowerCorner().getY()-metros
    x2,y2 = env.getUpperCorner().getX()+metros, env.getUpperCorner().getY()+metros
    return [x1, y1, 0, x2, y2, 0]
    
def extraer_edificios_kriging_2(lyrPointsBuilding, fieldElev):
    print "====== EXTRAER EDIFICIOS KRIGING ======= "
    positionField = lyrPointsBuilding.getSchema().getAttrNames().index(fieldElev)
    print "positiondField: ", positionField

    x = lyrPointsBuilding.getFullEnvelope()
    x1 = x.getLowerCorner()
    x2 = x.getUpperCorner()
    new1x = x1.getX() - 100
    new1y = x1.getY() - 100
    new2x = x2.getX() + 100
    new2y = x2.getY() + 100
    proc1 = g.runalg("kriging", lyrPointsBuilding, positionField, "5.0", "3", "5", "0", "0.0", "100.0", "2.0", ADDLAYER=False, OUTPUT_FILTER="interpolado", EXTENT=expand_extend(lyrPointsBuilding,50), TOCNAME="Krig", CELLSIZE=0.5, CELLSIZEZ=0.5)
    #proc1 = g.runalg("kriging", lyrPointsBuilding, positionField, "3.0", "3", "5", "0", "0.0", "1.0", "10.0", OUTPUT_FILTER="interpolado", EXTENT=expand_extend(lyrPointsBuilding,50))
    #proc1 = g.runalg("universalkriging", "cutbuildings", "0", "4.0", [], "4", "25", "0", "0.0", "10.0", "100.0",EXTENT=lyrPointsBuilding)

    nodata = proc1[0].getNoDataValue() #DefaultNoData()
    nodata.setValue(-99999)
    print nodata, type(nodata)
    proc1[0].setNoDataValue(nodata)
    proc1[0].setNoDataTransparent(True)
    #proc1[1].setVisible(False)
    return proc1[0] #Kriging
    
def extraer_edificios_kriging(lyrPointsBuilding, fieldElev, cellsize=2):
    print "====== EXTRAER EDIFICIOS RASTERIZAR ======= "
    positionField = lyrPointsBuilding.getSchema().getAttrNames().index(fieldElev)
    print "positiondField: ", positionField

    x = lyrPointsBuilding.getFullEnvelope()
    x1 = x.getLowerCorner()
    x2 = x.getUpperCorner()
    new1x = x1.getX() - 100
    new1y = x1.getY() - 100
    new2x = x2.getX() + 100
    new2y = x2.getY() + 100
    proc1 = g.runalg("rasterizevectorlayer", lyrPointsBuilding, positionField, ADDLAYER=False, EXTENT=expand_extend(lyrPointsBuilding,50), TOCNAME="Rasterizar", CELLSIZE=cellsize, CELLSIZEZ=cellsize)
    #proc1 = g.runalg("kriging", lyrPointsBuilding, positionField, "3.0", "3", "5", "0", "0.0", "1.0", "10.0", OUTPUT_FILTER="interpolado", EXTENT=expand_extend(lyrPointsBuilding,50))
    #proc1 = g.runalg("universalkriging", "cutbuildings", "0", "4.0", [], "4", "25", "0", "0.0", "10.0", "100.0",EXTENT=lyrPointsBuilding)

    nodata = proc1.getNoDataValue() #DefaultNoData()
    nodata.setValue(-99999)
    print nodata, type(nodata)
    proc1.setNoDataValue(nodata)
    proc1.setNoDataTransparent(True)
    #proc1[1].setVisible(False)
    return proc1 #Kriging

    
def extraer_edificios_poligonos(lyrKrig):
    print "====== EXTRAER EDIFICIOS POLIGONOS ======= "
    proc2 = g.runalg("contourlines", lyrKrig, "0.5", "0.0", "10000.0", ADDLAYER=False, EXTENT=lyrKrig, NAME="contour")
    proc3 = g.runalg("polylinestopolygons", proc2, EXTENT=lyrKrig, ADDLAYER=True, NAME="ResultPols")
    return proc3 # Poligonos de edificios


def extraer_edificios_bases(lyrKrig):
    print "====== EXTRAER EDIFICIOS BASES ======= "
    proc4 = g.runalg("combinemasks", [lyrKrig], EXTENT=lyrKrig, ADDLAYER=False)
    time.sleep(5)#15
    nodata = proc4.getNoDataValue() #DefaultNoData()
    nodata.setValue(0)

    proc4.setNoDataValue(nodata)
    proc4.setNoDataTransparent(True)
    print "testing: after nodata: ", proc4.getNoDataValue().getValue()
    time.sleep(5)#15

    currentView().centerView(proc4.getFullEnvelope())
    proc5 = g.runalg("vectorize", proc4, ADDLAYER=False)
    print "PROC5: ", proc5
    proc5features = proc5.features()
    selection = proc5.getSelection()
    for f in proc5features:
        if f.get(1)==1.0:
            selection.select(f)
    proc6 = g.runalg("geometricproperties", proc5, ADDLAYER=False)
    return proc6 # Bases de edifcios 

@timeit
def main(*args):
    # 1191 secs. 20 min
    pass