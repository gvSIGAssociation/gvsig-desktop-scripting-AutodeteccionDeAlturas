
import gvsig
from com.vividsolutions.jts.index.quadtree import Quadtree
from com.vividsolutions.jts.geom import Envelope
from com.vividsolutions.jts.geom import Coordinate

def main(*args):

    #Remove this lines and add here your code

    print "Quadtree"
    qt = Quadtree()
    layer = gvsig.currentLayer()
    for f in layer.features():
        env = f.geometry().buffer(30).getEnvelope()
        x1 = Coordinate(env.getLowerCorner().getX(), env.getLowerCorner().getY())
        x2 = Coordinate(env.getUpperCorner().getX(), env.getUpperCorner().getY())
        envelope = Envelope(x1, x2)
        qt.insert(envelope, f.getCopy())
        last = envelope
        #break
    qr = qt.query(last)
    print type(qr), len(qr)
    #print qr
    print qr[0]
    pass
