
import gvsig, geom
from whitebox.geospatialfiles import LASReader
import os
import time                                                

def timeit(method):

    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()

        print '%r (%r, %r) %2.2f sec' % \
              (method.__name__, args, kw, te-ts)
        return result

    return timed

def insertShape():
    schema = gvsig.createSchema()
    schema.append("GEOMETRY", "GEOMETRY")
    schema.append("Z", "DOUBLE")
    schema.append("Class", "INTEGER")
    schema.append("Intensity", "INTEGER")
    schema.get('GEOMETRY').setGeometryType(geom.POINT, geom.D2)

    new = gvsig.createShape(schema, CRS=gvsig.currentView().getProjectionCode())#, CRS=crs)#, geometryType=geom.SURFACE)
    gvsig.currentView().addLayer(new)
    return new

@timeit
def main(*args):

    #Remove this lines and add here your code

    print "LiDAR 2 Shape"
    inputFile = "C:/gvdata-lidar/lidar_mestalla.las"
    print os.path.exists(inputFile)
    las = LASReader(inputFile)
    numPoints = las.getNumPointRecords()
    print numPoints
    from sets import Set
    tipos = Set()
    newshape = insertShape()
    newshape.getFeatureStore().edit()
    n = 0
    for a in xrange(0, numPoints):
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
            continue
            #pass
        newshape.append({'Class': point.getClassification(),'Intensity': point.getIntensity(),'Z':point.getZ(),'GEOMETRY':geom.createPoint(point.getX(), point.getY())})
        n+=1
        if n > 200000:
            break
            
    newshape.commit()
    print "Tipos: ", tipos
    pass
