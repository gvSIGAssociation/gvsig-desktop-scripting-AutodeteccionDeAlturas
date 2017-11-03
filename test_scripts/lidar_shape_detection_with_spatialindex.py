
import gvsig
import geom


# https://docs.python.org/2/library/os.path.html
import tempfile
# https://docs.python.org/2/library/tempfile.html
import os
# https://docs.python.org/2/library/time.html
import time
from com.vividsolutions.jts.index.quadtree import Quadtree
from com.vividsolutions.jts.geom import Envelope
from com.vividsolutions.jts.geom import Coordinate

def getTempFile(name, ext):
    tempdir = os.path.join(tempfile.gettempdir(),"lidar")
    if not os.path.isdir(tempdir):
      os.makedirs(tempdir)
    f = os.path.join(
      tempdir,
      "%s-%x%s" % (name,time.time(),ext)
    )
    return f
    
def insertShape():
    schema = gvsig.createSchema()
    schema.append("GEOMETRY", "GEOMETRY")
    schema.append("Z", "DOUBLE")
    schema.get('GEOMETRY').setGeometryType(geom.POLYGON, geom.D2)

    new = gvsig.createShape(schema, CRS=gvsig.currentView().getProjectionCode())#, CRS=crs)#, geometryType=geom.SURFACE)
    gvsig.currentView().addLayer(new)
    return new

def createGeometryFrom(g):
        #scripting-help-v2/help/javadocs/html/org/gvsig/fmap/geom/GeometryManager.html
        from org.gvsig.fmap.geom import GeometryLocator
        geometryManager = GeometryLocator.getGeometryManager()
        geometry = geometryManager.createFrom(g)
        return geometry
        
def main(*args):
    print "Lidar: Identify shape"
    
    layer = gvsig.currentLayer() #gvsig.currentView().getLayer("tepoints")
    pol = insertShape() #gvsig.currentView().getLayer("tepol")

    flayer = layer.features()
    """
    newgeom = geom.createGeometry(3)
    print type(newgeom), newgeom
    initvertex = None
    for fl in flayer:
        if initvertex==None:
            initvertex = fl.geometry()
            
        npoint = fl.geometry()
        newgeom.addVertex(npoint)
    newgeom.addVertex(initvertex)
    

    store = pol.getFeatureStore()

    newfeature = store.createNewFeature()
    newfeature.set("GEOMETRY", newgeom)
    
    pol.edit()
    store.insert(newfeature)
    pol.commit()
    """
    qt = Quadtree()
    for f in flayer:
        env = f.geometry().buffer(10).getEnvelope()
        x1 = Coordinate(env.getLowerCorner().getX(), env.getLowerCorner().getY())
        x2 = Coordinate(env.getUpperCorner().getX(), env.getUpperCorner().getY())
        envelopef = Envelope(x1, x2)
        qt.insert(envelopef, f.getCopy())

    #Check distance between all points
    dB = {}
    idb = 0 #id building
    
    for f in flayer: #genp(lpoints):
        idb += 1
        if idb % 500 == 0:
            print "+500"
        ng = geom.createGeometry(3)
        dB[idb] = [0,0,list(),ng] # num ents, geoms, buffer            
        fgeom = f.geometry()
        env = fgeom.buffer(5).getEnvelope()
        x1 = Coordinate(env.getLowerCorner().getX(), env.getLowerCorner().getY())
        x2 = Coordinate(env.getUpperCorner().getX(), env.getUpperCorner().getY())
        envelope = Envelope(x1, x2)
        qr = qt.query(envelope)
        for n in range(0, len(qr)):
            j = qr[n]
            if j == None:
                continue
            dB[idb][1] += 1
            dB[idb][2].append(f.geometry())
            dB[idb][3].union(fgeom.buffer(5))
                
                
    #for n in range(0, lenPoints):
    #    for lpoints[n]
    pol.edit()
    store = pol.getFeatureStore()
    print "Creating polygons from points"
    print len(dB.keys())
    for idb in dB.keys():
        x = dB[idb]
        print len(x[2]),x[1],x[0]
        points = x[3]
        #if len(points) < 30:
        #    continue
        newfeature = store.createNewFeature()
        #newpol = geom.createGeometry(3)
        #for i in points:
        #    #p = createGeometryFrom(str(i)).buffer(2)
        #    newpol.addVertex(i)
        newpol = points
        newfeature.set("GEOMETRY", newpol)

        store.insert(newfeature)
    pol.commit()
    
    print "end"
    pass
    