

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

def timeit(method):
    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()
        print '%r (%r, %r) %2.2f sec' % \
              (method.__name__, args, kw, te-ts)
        return result
    return timed

class lpoint:
    def __init__(self, arg):
        self.values = arg
        
    def setUsed(self):
        self.values['used']=True
        
    def getValues(self):
        return self.values
        
class lidarPoints:
    all = None
    qt = Quadtree()
    bufferValue = 5
    fullpoints = []
    idbpointworking = 0
    def __init__(self):
        pass
        
    def loadLidar(self, layer):
        n = 0
        flayer = layer.features()
        for f in flayer:
            env = f.geometry().buffer(self.bufferValue).getEnvelope()
            x1 = Coordinate(env.getLowerCorner().getX(), env.getLowerCorner().getY())
            x2 = Coordinate(env.getUpperCorner().getX(), env.getUpperCorner().getY())
            envelopef = Envelope(x1, x2)
            self.fullpoints.append(lpoint({'idb':n, 'env':envelopef, 'point':f.geometry(), 'used':False}))
            self.qt.insert(envelopef, n)
            n += 1
            
    def getPointByIDB(self, idb):
        return self.fullpoints[idb]

    def setPointUsed(self, idb):
        self.fullpoints[idb].setUsed()

    def popNextPoint(self):
        pop = self.fullpoints[self.idbpointworking]
        self.setPointUsed(self.idbpointworking)
        self.idbpointworking += 1
        return pop

    def getQuery(self, lpoint):
        env = fg.buffer(10).getEnvelope() #
        x1 = Coordinate(env.getLowerCorner().getX(), env.getLowerCorner().getY())#
        x2 = Coordinate(env.getUpperCorner().getX(), env.getUpperCorner().getY())#
        envelopef = Envelope(x1, x2)#
        qt.remove(envelopef, fg)
        
        
    
@timeit
def main(*args):
    print "Lidar: Identify shape"
    
    layer = gvsig.currentLayer()
    lp = lidarPoints()
    lp.loadLidar(layer)
    print lp.fullpoints[0].getValues()
    print lp.getPointByIDB(1408).getValues()
    print lp.fullpoints[1408].getValues()
    lp.setPointUsed(1408)
    print lp.getPointByIDB(1408).getValues()
    
    while True:
        fg = lp.popNextPoint()
        print "FG: ", fg.getValues()
        break
    """
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
    """
    pass