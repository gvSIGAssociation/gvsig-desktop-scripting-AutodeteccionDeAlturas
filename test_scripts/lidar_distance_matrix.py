
import gvsig
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
    
def main(*args):

    #Remove this lines and add here your code

    print "hola mundo"
    layer = gvsig.currentLayer()
    nx = 0
    table = []
    print table
    count = layer.features().getCount()
    table = [[0 for i in range(0, count)] for j in range(0, count)]
    print "Calculating distances"
    for x in layer.features():
        ny = 0
        for y in layer.features():
            d = x.geometry().distance(y.geometry())
            table[nx][ny] = d
            table[ny][nx] = d
            ny+=1
        nx +=1
        if nx % 1000 == 0:
            print "pass: ", nx
    pass
