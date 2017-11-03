
from gvsig import *
from whitebox.geospatialfiles import LASReader
from whitebox.structures import BoundingBox
from whitebox.structures import KdTree
from whitebox.geospatialfiles.LASReader import PointRecord
from whitebox.geospatialfiles.LASReader import PointRecColours

def main(*args):
    """ LAS Reader"""
    gvLASReader("/home/osc/gvdata/s1795725.las")

    print "end"


def gvLASReader(inputFile):
    weight = 2
    maxDist = 10
    resolution = 10
    maxSlope = 30
    noData = -32768 #Arbitrario

    outputHeader = "/home/osc/gvdata/newmodel2.dep"
    
    las = LASReader(inputFile)
    numPoints = las.getNumPointRecords()
    testing = 0
    bb = BoundingBox(las.getMinX(), las.getMinY(), las.getMaxX(), las.getMaxY());
    
    print bb
    print "- BB: ", bb.getMinX(), bb.getMaxX(), bb.getMinY(), bb.getMaxY()
    print "- BB Weight: ", bb.getMaxX() - bb.getMinX()
    print "- BB Height: ", bb.getMaxY() - bb.getMinY()

    bbexpanded = BoundingBox(bb.getMinX()-resolution, bb.getMinY() - resolution
                 ,bb.getMaxX()+resolution, bb.getMaxY() + resolution)

    print bbexpanded
    print "- BB: ", bbexpanded.getMinX(), bbexpanded.getMaxX(), bbexpanded.getMinY(), bbexpanded.getMaxY()
    print "- BB Weight: ", bbexpanded.getMaxX() - bbexpanded.getMinX()
    print "- BB Height: ", bbexpanded.getMaxY() - bbexpanded.getMinY()

    from whitebox.structures import BooleanBitArray1D
    pointsTree = KdTree.SqrEuclid(2, int(numPoints))
    nongroundBitArray = BooleanBitArray1D(numPoints)
    print nongroundBitArray

    i = 0
    for a in xrange(0, numPoints):
        point = las.getPointRecord(a)
        entry = [point.getY(), point.getX()]
        pointsTree.addPoint(entry,  #Interpolation record is a class created in this script
                            InterpolationRecord(point.getX(), point.getY(), point.getZ(),
                            point.getScanAngle(),
                            i))
        i+= 1

    print pointsTree
    #Outputheader

    from java.io import File
    outputHeaderFile = File(outputHeader)
    if outputHeaderFile.exists():
        outputHeaderFile.delete()
        File(outputHeader.replace(".dep", ".tas")).delete()

    # Getting rows and cols
    # What are noth, south, east and west and how many rows and columns
    # should there be?
    west = bb.getMinX() - 0.5 * resolution
    north = bb.getMaxY() + 0.5 * resolution
    nrows = int((north - bb.getMinY()) / resolution)
    ncols = int((bb.getMaxX() - west) / resolution)
    south = north - nrows * resolution
    east = west + ncols * resolution
    print west, north, south, east, nrows, ncols
    from whitebox.geospatialfiles import WhiteboxRaster
    from whitebox.geospatialfiles import WhiteboxRasterBase
    from whitebox.geospatialfiles.WhiteboxRasterBase import DataType
    from whitebox.geospatialfiles.WhiteboxRasterBase import DataScale

    image = WhiteboxRaster(outputHeader, 
                  north, south, east, west, nrows, ncols, 
                  WhiteboxRasterBase.DataScale.CONTINUOUS,
                    WhiteboxRasterBase.DataType.FLOAT, noData, noData)
    import math
    radToDeg = 180.0 / math.pi
    #maxslope
    slopeThreshold = maxSlope / radToDeg
    halfResolution = resolution / 2
    print halfResolution, slopeThreshold
    # double maxDist = Math.sqrt(2) * resolution / 2.0d;
    #   double maxDistSqr = maxDist * maxDist;
    #maxDist
    maxScanAngleDeviation = 10
    for row in xrange(0, nrows):
        for col in xrange(0, ncols):
            easting = image.getXCoordinateFromColumn(col)
            northing = image.getYCoordinateFromRow(row)
            entry = [northing, easting]
            #print entry
            results = pointsTree.neighborsWithinRange(entry, maxDist)
            if results.size() > 1:
                #print "Tak PointsTree Neighbors: ", results.size()
                minScanAngle = 99999999999 #positive infinity
                maxScanAngle = 0  #negative infinity
                for i in xrange(0, results.size()):
                    value = results.get(i).value
                    scanAngle = value.scanAngle
                    #print value.getValue(), value.getX(), value.getY()
                    #print scanAngle
                    #if scanAngle != 0: print scanAngle
                    if scanAngle > maxScanAngle: maxScanAngle = scanAngle
                    if scanAngle < minScanAngle: minScanAngle = scanAngle
                for i in xrange(0, results.size()):
                    value = results.get(i).value
                    scanAngle = value.scanAngle
                    if ((scanAngle - minScanAngle) > maxScanAngleDeviation):
                        nongroundBitArray.setValue(value.getIndex(), True)
                #print maxScanAngle, minScanAngle
                #break
                n = results.size()
                for i in xrange(0, n):
                  try:
                    rec1 = results.get(i).value
                    if nongroundBitArray.getValue(rec1.getIndex()) == False:
                        for j in xrange(0, n):
                            rec2 = results.get(j).value
                            if rec1.getIndex()==rec2.getIndex():
                               continue
                            if nongroundBitArray.getValue(rec2.getIndex()) == False:
                                r1x, r1y = rec1.getX(), rec1.getY()
                                r2x, r2y = rec2.getX(), rec2.getY()
                                dist = math.sqrt((r1x-r2x)*(r1x-r2x)+(r1y-r2y)*(r1y-r2y))
                                #print dist
                                if (rec1.getValue() > rec2.getValue()):
                                  higherVal = rec1.getValue()
                                  lowerVal = rec2.getValue()
                                  higherPoint = i
                                  higherPointIndex = rec1.getIndex()
                                else:
                                  higherVal = rec2.getValue()
                                  lowerVal = rec1.getValue()
                                  higherPoint = j
                                  higherPointIndex = rec2.getIndex()
                                
                                slope = math.atan((higherVal - lowerVal) / dist)
                                if (slope > slopeThreshold):
                                  nongroundBitArray.setValue(higherPointIndex, True)
                  except:
                      print "Error"
                z = noData
                n = 0
                sumWeights = 0
                weights = []
                vals = []
                for i in xrange(0, results.size()):
                    rec1 = results.get(i).value
                    if nongroundBitArray.getValue(rec1.getIndex())==False:
                        if results.get(i).distance > 0:
                            dist = 1 / math.pow(math.sqrt(results.get(i).distance),weight)
                            weights.append(dist)
                            sumWeights += dist
                            vals.append(rec1.value)
                            n += 1
                        else:
                            weights = []
                            vals = []
                            weights.append(1.0)
                            sumWeights = 1.0
                            vals.append(rec1.value)
                            n = 1
                            break
                if n>0:
                    z = 0
                    for s in xrange(0, n):
                        z += (weights[s] * vals[s])/sumWeights       
                image.setValue(row, col, z)
                     
        #break
    image.close()
    return
    for a in xrange(0, numPoints):
        point = las.getPointRecord(a)
        print point, dir(point)
        print "\nID: ", a
        print "Classification: ", point.getClassification()
        print "ScanAngle: ", point.getScanAngle()
        print "NumberOfReturns: ", point.getNumberOfReturns()
        print "Intensity: ", point.getIntensity()
        print "PointSourceID: ", point.getPointSourceID()
        print "UserData: ", point.getUserData()
        print "X, Y, Z: ", point.getX(), point.getY(), point.getZ()
        print "GPS Time: ", point.getGPSTime()
        testing += 1
        if testing == 30:
            break
    
class InterpolationRecord:
        value = 0.0
        scanAngle = 0 #byte
        x = float()
        y = float()
        index = int()
        
        def __init__(self, x,  y,  value, scanAngle, index):
            self.value = value
            self.scanAngle = scanAngle #(byte)Math.abs(scanAngle);
            self.x = x
            self.y = y
            self.index = index
        
        def getValue(self):
            return float(self.value)
     
        def getScanAngle(self):
            return scanAngle #byte
        def getX(self):
          return float(self.x)

        def getY(self):
          return float(self.y)   

        def getIndex(self):
          return int(self.index)
