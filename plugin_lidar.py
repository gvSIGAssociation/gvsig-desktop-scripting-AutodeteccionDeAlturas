
from gvsig import *
from gvsig.libs.formpanel import FormPanel
from gvsig import commonsdialog
from java.io import File
import java.lang.Throwable
from StringIO import StringIO

import lidarlib.lidar_to_shape
reload(lidarlib.lidar_to_shape)
from lidarlib.lidar_to_shape import lidar_to_shape

import gvsig.libs.gvpy
reload(gvsig.libs.gvpy)
from gvsig.libs import gvpy as g

from org.gvsig.raster.impl.datastruct import DefaultNoData
import lidarlib
reload(lidarlib)
from lidarlib.altura_base import altura_base
reload(lidarlib.altura_base)

from lidarlib.alternativa_correcion_puntos import alternativa_correccion_puntos

import lidarlib.extraer_edificios
reload(lidarlib.extraer_edificios)
from lidarlib.extraer_edificios import extraer_edificios_kriging, extraer_edificios_bases, extraer_edificios_poligonos
from lidarlib.correcion_poligonos_con_base import correccion_poligonos_con_base
from lidarlib.field_constru2metros import field_constru2metros
reload(lidarlib.field_constru2metros)

import lidarlib.discrepancias 
reload(lidarlib.discrepancias)
from lidarlib.discrepancias import discrepancias

import lidarlib.analizar_resultado_interseccion
reload(lidarlib.analizar_resultado_interseccion)
from lidarlib.analizar_resultado_interseccion import analizar_resultado_interseccion

from gvsig.libs.timeit import timeit
import time
import thread, threading
import os.path
from org.gvsig.andami import PluginsLocator
from org.gvsig.scripting.app.extension import ScriptingExtension
from org.gvsig.tools.swing.api import ToolsSwingLocator
import traceback
import java.lang.Exception
import sys

class Panel(FormPanel):
    def __init__(self):
        FormPanel.__init__(self, getResource(__file__, "plugin_lidar2.xml"))
        self.btnUpdateCmb_click()

    def message(self, msg, mode=LOGGER_INFO, ex=None):
      logger(msg,mode,ex)
      self.txtField.setText(msg)

    def btnPath_click(self, *args):
        laspath = commonsdialog.openFileDialog("Abrir fichero", initialPath=getResource(__file__))[0]
        self.txtPath.setText(laspath)

    def btnCalcularAlturas_click(self, *args):
        if currentView()==None:
          self.message("Es necesario que haya una vista activa.")
          return
        threading.Thread(target=self.calcularAlturas, name="CalcularAlturas", args=tuple()).start()

    def calcularAlturas(self):
       try:
            self.message("Calculando...")
            self.btnClose.setEnabled(False)
            self.btnCalcularAlturas.setEnabled(False)
            #Pedir path fichero las
            laspath = self.txtPath.getText()
            
            if laspath == "":
                self.message("Indique una ruta correcta.")
                commonsdialog.msgbox("Debe introducir una ruta correcta","Error", commonsdialog.FORBIDEN )
                return

            self.message("Calculando... creando capa de puntos...")
            #Calcular capas de puntos
            lyrPointsBuildings, lyrPointsGround = lidar_to_shape(laspath) 
    
            #Crear base de edificios
            self.message("Calculando... base de las construcciones...")
            lyrKri =  extraer_edificios_kriging(lyrPointsBuildings,"Z")
            
            #lyrPoligonos = extraer_edificios_poligonos(lyrKri) #Final sin corregir
            self.message("Calculando... construcciones...")
            lyrBase = extraer_edificios_bases(lyrKri)
            
            # Base de edificios corregida de altura
            self.message("Calculando... alturas...")
            basecorregida = altura_base(lyrBase, lyrPointsGround)

            # Alternativa 1:
            self.message("Calculando... realizando correcciones...")
            puntos_corregidos = alternativa_correccion_puntos(basecorregida, lyrPointsBuildings)
        
            #Nuew base
            self.message("Calculando... correcciones de las construcciones...")
            lyrNewKrig = extraer_edificios_kriging(puntos_corregidos, "ZELEV")

            self.message("Calculando... poligonos de las construcciones...")
            lyrNewPoligonos = extraer_edificios_poligonos(lyrNewKrig)
            
            self.message("Completado")
            
       except Exception, ex:
            self.message("Se ha producido errores", mode=LOGGER_WARN, ex=ex)
            commonsdialog.msgbox("Se produjo un error durante el proceso", "Error", commonsdialog.FORBIDEN)
       finally:
            self.btnCalcularAlturas.setEnabled(True)
            self.btnClose.setEnabled(True)
      
    def btnDiscrepancias_click(self, *args):
        if currentView()==None:
          self.message("Es necesario que haya una vista activa.")
          return
        threading.Thread(target=self.analisisDiscrepancias, name="Analisis de discrepancias", args=tuple()).start()
        
    def analisisDiscrepancias(self):
        try:
            self.message("Calculando...")
            self.btnClose.setEnabled(False)
            self.btnDiscrepancias.setEnabled(False)
            lyrPol = currentView().getLayer(str(self.cmbPol.getSelectedItem()))
            lyrBase = currentView().getLayer(str(self.cmbPar.getSelectedItem()))
            
            self.message("Calculando... normalizando alturas...")
            field_constru2metros(lyrBase,field="CONSTRU", ratio=3) 
            
            self.message("Calculando... discrepancias...")
            resultdis = discrepancias(lyrPol, lyrBase)
            
            self.message("Calculando... filtrado de discrepancias...")
            analizar_resultado_interseccion(resultdis, areamin=4, difaltura=2)
            
            self.message("Completado")
       
        except Exception, ex:
            self.message("Se ha producido errores",mode=LOGGER_WARN, ex=ex)
            commonsdialog.msgbox("Se produjo un error durante el proceso", "Error", commonsdialog.FORBIDEN)
        finally:
            self.btnDiscrepancias.setEnabled(True)
            self.btnClose.setEnabled(True)
            
    
    def btnUpdateCmb_click(self, *args):
      if currentView()==None:
        return
      self.cmbPol.removeAllItems()
      self.cmbPar.removeAllItems()
      for lyr in currentView().getLayers():
          self.cmbPol.addItem(lyr.name)
          self.cmbPar.addItem(lyr.name)
        
    def btnClose_click(self,*args):
        self.hide()


def warn(msg, ex):
  tb = sys.exc_info()[2]
  f = StringIO()
  f.write("%s\n" % msg)
  f.write("Traceback (most recent call last):\n")
  while tb!=None:
    code = tb.tb_frame.f_code
    f.write("  File %r, line %d, %s\n" % (code.co_filename,tb.tb_frame.f_lineno,code.co_name))
    tb = tb.tb_next
  f.write("%s\n" % str(ex))
  f.getvalue()
  print f.getValue()
  ScriptingExtension.log(ScriptingExtension.WARN,f.getvalue(),None)


class DeteccionDeAlturasExtension(ScriptingExtension):
  def __init__(self):
    pass

  def canQueryByAction(self):
    return True

  def isEnabled(self,action):
    return currentView()!=None

  def isVisible(self,action):
    return currentView()!=None
    
  def execute(self,actionCommand, *args):
    l = Panel()
    l.showTool("Autodeteccion de alturas")

def selfRegister():
  application = ApplicationLocator.getManager()

  icon_show = File(getResource(__file__,"deteccion-alturas.png")).toURI().toURL()
  
  iconTheme = ToolsSwingLocator.getIconThemeManager().getCurrent()
  iconTheme.registerDefault("scripting.deteccion-alturas", "action", "tools-deteccion-alturas-show", None, icon_show)
  
  extension = DeteccionDeAlturasExtension()
  actionManager = PluginsLocator.getActionInfoManager()
  action_show = actionManager.createAction(
    extension, 
    "tools-deteccion-alturas-show", # Action name
    "Deteccion de alturas", # Text
    "show", # Action command
    "tools-deteccion-alturas-show", # Icon name
    None, # Accelerator
    1009000000, # Position 
    "Deteccion de alturas" # Tooltip
  )
  action_show = actionManager.registerAction(action_show)
  
  application.addMenu(action_show, "tools/Deteccion de alturas")
  application.addTool(action_show, "Deteccion de alturas")


def main(*args):
  l = Panel()
  l.showTool("Autodeteccion de alturas")
  pass