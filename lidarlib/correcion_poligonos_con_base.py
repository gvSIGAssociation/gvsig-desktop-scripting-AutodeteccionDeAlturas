
from gvsig import *
from gvsig.geom import *
from gvsig.libs.timeit import timeit

@timeit
def correccion_poligonos_con_base(lyrPol, lyrBase):
    print "====== CORRECCION POLIGONOS CON BASE ======= "
    """ Correccion poligonos con base """
    """
    param layer: layer Poligonos resultado
    param base: layer con bases con alturas corregidas
    resultado: capa layer con poligonos corregidos
    """
    featurespol = lyrPol.features()
    featuresbase = lyrBase.features()
    
    sch = createSchema()
    sch.append("Elevation","DOUBLE")
    sch.append("HBASE", "DOUBLE")
    sch.append("ZEND", "DOUBLE")
    sch.append("GEOMETRY", "GEOMETRY")
    sch.get("GEOMETRY").setGeometryType(POLYGON, D2)
    newshape = createShape(sch, prefixname="respol")
    for fpol in featurespol:
        for fbase in featuresbase:
            if fpol.geometry().intersects(fbase.geometry()):
                zend = fpol.Elevation - fbase.HEIGHT
                newshape.append(HBASE=fbase.HEIGHT,Elevation=fpol.Elevation,ZEND=zend,GEOMETRY=fpol.geometry())
                break

    newshape.commit()
    #currentView().addLayer(newshape)
    return newshape
                
                
    pass

def main(*args):
    lyrPol = currentView().getLayer("pol")
    lyrBase = currentView().getLayer("base")
    correccion_poligonos_con_base(lyrPol, lyrBase)