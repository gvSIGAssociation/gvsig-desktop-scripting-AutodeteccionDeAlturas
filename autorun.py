
from gvsig import *
import plugin_lidar
reload(plugin_lidar)

def main(*args):
    plugin_lidar.selfRegister()
