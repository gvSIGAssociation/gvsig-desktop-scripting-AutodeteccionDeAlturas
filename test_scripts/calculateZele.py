
from gvsig import *
import geom

def main(*args):

    # Create new example shape
    layer = currentLayer()
    #Filter features
    features = layer.features()

    layer.edit()
    for i in features:
        try:
            zground = i.get('Zground')
            elevation = i.get('Elevation')
            value = elevation - zground
            c = i.getEditable()
            c.set("Zele", value)
            features.update(c)
        except:
            pass
        
    layer.commit()