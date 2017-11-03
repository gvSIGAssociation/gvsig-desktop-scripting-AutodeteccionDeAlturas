
from gvsig import *
from gvsig.geom import *
from gvsig.libs.timeit import timeit

@timeit
def main(*args):
    lyrpol = currentView().getLayer("ResultPols")
    lyrpar = currentView().getLayer("constru_ayuntamiento_valencia")
    discrepancias(lyrpol, lyrpar, fieldZpar="HEIGHT", fieldZpol="Elevation")

def discrepancias(lyrpol, lyrpar, fieldZpar="HEIGHT", fieldZpol="Elevation", newFieldZdif="ZDIF"):
    """ 
    Ordenar los poligonos por altura, siendo las mas bajas primero analizadas
    De esta forma en la capa de poligonos final apareceran ordenadas y se podra 
    ver la forma del edificio
    """
    
    print "Iniciando analisis de discrepancias..."
    #lyrpar = currentView().getLayer("poli_parcelas")
    #lyrpol = currentView().getLayer("resultado_poligonal")

    fpar = lyrpar.features()
    fpol = lyrpol.features('ID>0',fieldZpol,asc=True)

    sch = createSchema(lyrpar.getSchema())
    sch.append(fieldZpol, "DOUBLE")
    sch.append(newFieldZdif, "DOUBLE")
    sch.get("GEOMETRY").setGeometryType(POLYGON, D2)
    newshape = createShape(sch, prefixname="inter")
    newshape.edit()
    n = 0
    total = fpol.getSize()
    for pol in fpol:
        n+=1
        for par in fpar:
            try:
                if par.get(fieldZpar) < pol.get(fieldZpol):
                    if par.geometry().intersects(pol.geometry()):
                        ngeom = par.geometry().intersection(pol.geometry())
                        values = par.getValues()
                        values[fieldZpar] = par.get(fieldZpar)
                        values[fieldZpol] = pol.get(fieldZpol)
                        values[newFieldZdif] = values[fieldZpol] - values[fieldZpar]
                        values["GEOMETRY"] = ngeom
                        newshape.append(values)
            except:
                    pass
          
                    
                    
    newshape.commit()
    currentView().addLayer(newshape)
    return newshape
    pass
