import gvsig
from gvsig import geom
from whitebox.geospatialfiles import LASReader
import os
import time                                                


def paginado(*args):
    pass
    
def main(*args):

    inputFile = "C:/gvdata-lidar/lidar_valencia.las"
    inputFile = r"C:/gvdata-lidar/LiDAR_2297952622768139636.las"
    print os.path.exists(inputFile)
    las = LASReader(inputFile)
    numPoints = las.getNumPointRecords()
    print las, type(las)
    print dir(las)
    print "X offset: ", las.getXOffset(), las.getXScale()
    xdif = las.getMaxX()-las.getMinX() #las.getMaxX(), las.getMinX(), 
    print "X: ", xdif
    ydif =  las.getMaxY()-las.getMinY() #las.getMaxY(), las.getMinY(),
    print "Y: ", ydif
    print "Total: ", las.getNumPointRecords()
    print "Area: ", xdif * ydif
    print "Densidad: ", las.getNumPointRecords() / ((las.getMaxX()-las.getMinX())*(las.getMaxY()-las.getMinY())), " por m2"

    pass
