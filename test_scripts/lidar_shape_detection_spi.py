
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
    schema.append("IDB", "INTEGER")
    schema.get('GEOMETRY').setGeometryType(geom.POINT, geom.D2)

    new = gvsig.createShape(schema, CRS=gvsig.currentView().getProjectionCode())#, CRS=crs)#, geometryType=geom.SURFACE)
    gvsig.currentView().addLayer(new)
    return new

def createGeometryFrom(g):
        #scripting-help-v2/help/javadocs/html/org/gvsig/fmap/geom/GeometryManager.html
        from org.gvsig.fmap.geom import GeometryLocator
        geometryManager = GeometryLocator.getGeometryManager()
        geometry = geometryManager.createFrom(g)
        return geometry
        
def recCall(fg, x, fullpoints, qt):
    """
    qr = spPoints(fg, qt)
    env = fg.buffer(10).getEnvelope()
    x1 = Coordinate(env.getLowerCorner().getX(), env.getLowerCorner().getY())
    x2 = Coordinate(env.getUpperCorner().getX(), env.getUpperCorner().getY())
    envelopef = Envelope(x1, x2)
    qt.remove(envelopef, fg)
    
    for jg in qr:
    """
    distanceWithPoints = 5
    listapuntos = []

    print "VALUE: ", fg, qt
    qr = spPoints(fg, qt) #
    env = fg.buffer(10).getEnvelope() #
    x1 = Coordinate(env.getLowerCorner().getX(), env.getLowerCorner().getY())#
    x2 = Coordinate(env.getUpperCorner().getX(), env.getUpperCorner().getY())#
    envelopef = Envelope(x1, x2)#
    qt.remove(envelopef, fg)#
    
    for n in qr:
        enve = n[1]#
        n = n[0] #
    #for n in range(0, len(fullpoints)):
        

        jg = fullpoints[n] #n
        if jg==False or fg==False:
            continue
        if fg.distance(jg) < distanceWithPoints:
            listapuntos.append(jg)
            fullpoints[n]=False
            qt.remove(enve, n)#
            
    for jg in listapuntos:
            x.append(jg)
            recCall(jg, x, fullpoints, qt)


def insertValues(dB):
    pol = insertShape()
    pol.edit()
    store = pol.getFeatureStore()
    print "Creating polygons from points"
    print len(dB.keys())
    for idb in dB.keys():
        points = dB[idb]
        for i in points:
            newfeature = store.createNewFeature()
            newfeature.set("IDB", int(idb))
            if i==False or i==True: continue
            newfeature.set("GEOMETRY", i)
            store.insert(newfeature)
    pol.commit()


def spPoints(f, qt):
        env = f.buffer(5).getEnvelope()
        x1 = Coordinate(env.getLowerCorner().getX(), env.getLowerCorner().getY())
        x2 = Coordinate(env.getUpperCorner().getX(), env.getUpperCorner().getY())
        envelope = Envelope(x1, x2)
        qr = qt.query(envelope)
        return qr


### MAIN METHOD
### MAIN METHOD
### MAIN METHOD

@timeit
def main(*args):
    print "Lidar: Identify shape"
    
    layer = gvsig.currentLayer() #gvsig.currentView().getLayer("tepoints")
    #pol = insertShape() #gvsig.currentView().getLayer("tepol")

    flayer = layer.features()
    
    qt = Quadtree()
    n = 0
    indexList = [True] * flayer.getCount()
    for f in flayer:
        env = f.geometry().buffer(10).getEnvelope()
        x1 = Coordinate(env.getLowerCorner().getX(), env.getLowerCorner().getY())
        x2 = Coordinate(env.getUpperCorner().getX(), env.getUpperCorner().getY())
        envelopef = Envelope(x1, x2)
        qt.insert(envelopef, [n,envelopef])
        n += 1

    sp = {}
    print dir(flayer)
    nn = 0
    fullpoints = [i.geometry() for i in flayer]
    print len(fullpoints)
    while True:
        fg = fullpoints.pop()
        if str(nn).endswith("00"):
            print "Len: ", nn, fg
        #indexList[nn] = False
        sp[nn] = [fg]
        recCall(fg, sp[nn], fullpoints, qt)
        nn += 1
        top = False
        for i in fullpoints:
            if i!=False:
                top = True
        if top==False:
            break
            
    for i in sp.keys():
        if len(sp[i]) > 3:
            print "Buildings: ", len(sp[i])
            
    insertValues(sp)
    