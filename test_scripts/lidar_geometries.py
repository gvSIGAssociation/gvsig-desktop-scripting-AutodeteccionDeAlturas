
import gvsig
import geom


# https://docs.python.org/2/library/os.path.html
import tempfile
# https://docs.python.org/2/library/tempfile.html
import os
# https://docs.python.org/2/library/time.html
import time

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
    lpoints = []
    clpoints = []
    for p in layer.features():
        lpoints.append(p.geometry())
        clpoints.append(p.geometry())

    #Check distance between all points
    lenPoints = len(lpoints)
    dB = {}
    idb = 0 #id building
    lenbuffer = 2.8
    for i in lpoints: #genp(lpoints):
        idb += 1
        if idb % 500 == 0:
            print "+500"
        dB[idb] = [0,list(),i.buffer(lenbuffer)] # num ents, geoms, buffer            
        for n in range(0, len(clpoints)):
            j = clpoints[n]
            if j == None:
                continue
            if dB[idb][2].intersects(j):
                
                if dB[idb][0]==0:
                    dB[idb][0] += 1
                    dB[idb][1].append(i)
                    dB[idb][2] = i.buffer(lenbuffer)
                dB[idb][0] += 1
                dB[idb][1].append(j)
                dB[idb][2] = dB[idb][2].union(j.buffer(lenbuffer))
                clpoints[n] = None
                
                
    #for n in range(0, lenPoints):
    #    for lpoints[n]
    pol.edit()
    store = pol.getFeatureStore()
    for i in dB.keys():
        x = dB[i]
        if x[0] < 3:
            continue
        print "B: ", i, " POLY: ", x[0]
        newfeature = store.createNewFeature()
        newfeature.set("GEOMETRY", x[2].buffer(-lenbuffer+0.5))

        store.insert(newfeature)
    #pol.commit()
    
    print "end"
    pass
    
def genp(lpoints):
    print len(lpoints)
    yield lpoints.pop(0)
    
