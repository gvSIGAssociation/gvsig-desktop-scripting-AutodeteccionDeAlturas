
from gvsig import *
from gvsig.geom import *
from gvsig.libs.timeit import timeit

@timeit
def alternativa_correccion_puntos(lyrBase, lyrPoints):
    print "====== CORRECCION DE PUNTOS ======= "
    sch = createSchema()
    sch.append("ID", "INTEGER", 10)
    sch.append("Z", "DOUBLE", 10)
    sch.append("ZBASE", "DOUBLE", 10)
    sch.append("ZELEV", "DOUBLE", 10)
    sch.append("GEOMETRY", "GEOMETRY")
    sch.get("GEOMETRY").setGeometryType(POINT, D2)
    newshape = createShape(sch)
    newshape.edit()
    fbase = lyrBase.features()
    fpoints = lyrPoints.features()
    for fb in fbase:
        for fp in fpoints:
            try:
              zelev = fp.Z-fb.HEIGHT
              if zelev < 0:
                  continue
              if fp.geometry().intersects(fb.geometry()):
                    newshape.append(ID=fb.ID,
                                    Z=fp.Z,
                                    ZBASE=fb.HEIGHT,
                                    ZELEV=zelev,
                                    GEOMETRY=fp.geometry()
                                    )
            except:
                print "Geometry error", fb, fp
                pass
    newshape.commit()
    #currentView().addLayer(newshape)
    return newshape

    
def main(*args):
    print "Calculating.."
    #basecorregida = currentView().getLayer("bases")
    basecorregida = currentLayer()
    lyrPointsForCorrection = currentView().getLayer("mestalla_buildings")
    
    puntos_corregidos = alternativa_correccion_puntos(basecorregida, lyrPointsForCorrection)
    pass