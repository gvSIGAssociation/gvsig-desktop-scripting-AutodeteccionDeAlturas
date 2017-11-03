
import gvsig
from gvsig import geom

from gvsig.uselib import use_jar
import os.path


import os
import time                                                
from gvsig.libs.timeit import timeit


def insertShape(prefixname):
    schema = gvsig.createSchema()
    schema.append("GEOMETRY", "GEOMETRY")
    schema.append("Z", "DOUBLE")
    schema.append("Class", "INTEGER")
    schema.append("Intensity", "INTEGER")
    schema.get('GEOMETRY').setGeometryType(geom.POINT, geom.D2)

    new = gvsig.createShape(schema, CRS=gvsig.currentView().getProjectionCode(), prefixname=prefixname)#, CRS=crs)#, geometryType=geom.SURFACE)
    #gvsig.currentView().addLayer(new)
    return new

@timeit
def lidar_to_shape(inputFile):
    import sys
    use_jar(os.path.join(os.path.dirname(__file__),"..","jars","WhiteboxAPI.jar"))
    from whitebox.geospatialfiles import LASReader

    #print inputFile
    #print os.path.exists(inputFile)
    las = LASReader(inputFile)
    numPoints = las.getNumPointRecords()
    #print numPoints
    from sets import Set
    tipos = Set()
    newshape_ground = insertShape("ground")
    newshape_building = insertShape("building")
    
    newshape_ground.getFeatureStore().edit()
    newshape_building.getFeatureStore().edit()
    n = 0
    for a in xrange(0, numPoints):
        n+=1
        #if 7000000 < n < 7300000:
        #if 7200000 < n < 7500000:
        point = las.getPointRecord(a)
        entry = [point.getY(), point.getX()]
        """
        print "\nID: ", a
        print "Classification: ", point.getClassification()
        print "ScanAngle: ", point.getScanAngle()
        print "NumberOfReturns: ", point.getNumberOfReturns()
        print "Intensity: ", point.getIntensity()
        print "PointSourceID: ", point.getPointSourceID()
        print "UserData: ", point.getUserData()
        print "X, Y, Z: ", point.getX(), point.getY(), point.getZ()
        print "GPS Time: ", point.getGPSTime()
        """
        tipos.add(point.getClassification())
        if point.getClassification()==6:
            newshape_building.append({'Class': point.getClassification(),'Intensity': point.getIntensity(),'Z':point.getZ(),'GEOMETRY':geom.createPoint2D(point.getX(), point.getY())})
        else:
            newshape_ground.append({'Class': point.getClassification(),'Intensity': point.getIntensity(),'Z':point.getZ(),'GEOMETRY':geom.createPoint2D(point.getX(), point.getY())})
        #print point.getX(), point.getY()

        
        #if n > 100000:
        #    break
            
    newshape_building.commit()
    newshape_ground.commit()
    #print "Tipos: ", tipos
    return newshape_building, newshape_ground # RETURN LAYERBUILDING, LAYERGROUND

def main(*args):
    #inputFile = r"C:/gvdata-lidar/lidar_rustica_1.las"
    #inputFile = r"C:/gvdata-lidar/LiDAR_6397680901258476999.las"
    #inputFile = r"C:/gvdata-lidar/lidar_valencia.las"
    #inputFile = r"C:\gvdata-lidar\ejemplo_rustica\lidar_rustica.las"
    #inputFile = r"C:\gvdata-lidar\lidar_rustica_test1\loriguilla.las"
    #inputFile = r"C:\gvdata-lidar\test\LIDAR-LAZ-2014-SP08\280.las"
    inputFile = os.path.join(os.path.dirname(__file__),"..","datos","loriguilla.las")
    lyrPointsBuildings, lyrPointsGround = lidar_to_shape(inputFile)  
    pass