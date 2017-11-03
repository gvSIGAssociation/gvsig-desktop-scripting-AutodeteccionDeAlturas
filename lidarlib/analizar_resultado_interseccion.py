
from gvsig import *

def analizar_resultado_interseccion(layer, areamin=6, difaltura=10, fieldZDif="ZDIF"):
    """
    param layer: shpe, resultado interseccion entre pols y constru
    param areamin: int, area minima para tenerla en cuenta
    param difaltura: int, diferencia minima para exportar a la capa
    """
    sch = createSchema(layer.getSchema())
    shp = createShape(sch,prefixname="dif-alt"+str(difaltura)+"ar"+str(areamin))
    shp.edit()
    for i in layer.features():
        #Area_constru depende de la capa poligonal inf constru.
        if i.geometry().area() < areamin:
            continue

        dif = i.get(fieldZDif)
        if dif > difaltura: # Gran diferencia
            values = i.getValues()
            shp.append(values)
        
    shp.commit()
    currentView().addLayer(shp)

def main(*args):
    analizar_resultado_interseccion(currentLayer(),6, 10)
