
from gvsig import *
from org.gvsig.fmap.dal.feature.impl.featureset import DefaultFeatureSet
from org.gvsig.fmap.dal.feature.impl import DefaultFeatureQuery
import re
from gvsig.libs.timeit import timeit

#Define digit mapping

#Define exceptions
class RomanError(Exception): pass
class OutOfRangeError(RomanError): pass
class NotIntegerError(RomanError): pass
class InvalidRomanNumeralError(RomanError): pass

romanNumeralMap = (('M',  1000),
                   ('CM', 900),
                   ('D',  500),
                   ('CD', 400),
                   ('C',  100),
                   ('XC', 90),
                   ('L',  50),
                   ('XL', 40),
                   ('X',  10),
                   ('IX', 9),
                   ('V',  5),
                   ('IV', 4),
                   ('I',  1))
                   
romanNumeralPattern = re.compile("""
    ^                   # beginning of string
    M{0,4}              # thousands - 0 to 4 M's
    (CM|CD|D?C{0,3})    # hundreds - 900 (CM), 400 (CD), 0-300 (0 to 3 C's),
                        #            or 500-800 (D, followed by 0 to 3 C's)
    (XC|XL|L?X{0,3})    # tens - 90 (XC), 40 (XL), 0-30 (0 to 3 X's),
                        #        or 50-80 (L, followed by 0 to 3 X's)
    (IX|IV|V?I{0,3})    # ones - 9 (IX), 4 (IV), 0-3 (0 to 3 I's),
                        #        or 5-8 (V, followed by 0 to 3 I's)
    $                   # end of string
    """ ,re.VERBOSE)

def fromRoman(s):
    """convert Roman numeral to integer"""
    if not s:
        raise InvalidRomanNumeralError, 'Input can not be blank'
    if not romanNumeralPattern.search(s):
        raise InvalidRomanNumeralError, 'Invalid Roman numeral: %s' % s

    result = 0
    index = 0
    for numeral, integer in romanNumeralMap:
        while s[index:index+len(numeral)] == numeral:
            result += integer
            index += len(numeral)
    return result

@timeit
def field_constru2metros(layer, field, ratio = 3, newfield="HEIGHT"):
    print "====== ALTURA BASE ======= "
    try:
        sch = createSchema(layer.getSchema())
        sch.append(newfield, "DOUBLE", 10)
        layer.updateSchema(sch)
        layer.commit()
    except:
        pass
    #store = layer.getFeatureStore()
    #query = DefaultFeatureQuery([field])
    #featureSet = DefaultFeatureSet(store, query)

    n = 0
    layer.edit()
    featureSet = layer.features()
    for f in featureSet:
        constru = f.get(field)
        listconstru = str(constru).split("+")
        try:
            if listconstru[-1] == 'TZA':
                fromroman = fromRoman(listconstru[-2])
            else:
                fromroman = fromRoman(listconstru[-1])
            #print "Lista: ", listconstru, "\t\tValue: ", listconstru[-1], " Number: ", fromroman
        except:
            if listconstru[-1] not in ["?","SUELO","-I", "-II", "-III", "-IV", "P", "JD"]:
                print "***** Error in:", listconstru, " Value: ", listconstru
            fromroman = 0
        c = f.getEditable()
        c.set(newfield, fromroman * ratio)
        featureSet.update(c)
    layer.commit()
        
def main(*args):

    #Field CONSTRU 2 METROS

    field_constru2metros(currentLayer(),field="CONSTRU_co", ratio=3) #ratio = metros * altura
    pass
