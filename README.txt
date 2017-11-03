
Forma de instalación
=====================

La herramienta para la Detección de Alturas se puede instalar desde el administrador
 de complementos de gvSIG.

Funcionalidad
===============

El objetivo final es facilitar el análisis de los datos LIDAR para permitir su 
comparación con una capa de parcelas.

Consta de dos herramientas:
- Detección de alturas
- Análisis de discrepancias

Requerimientos
================

Requiere un "gvSIG desktop" 2.3.0 build > 2430 con los plugins de Geoprocesos y 
Scripting instalados.

Fuentes
========

Los fuentes, el documento de descripcion y este README van incluidos en el "addon"
 de la herramienta.

Datos de prueba
=======

La primera parte de la herramienta necesita de un fichero de datos LIDAR con la extensión .las.

Ficheros de ejemplo se encuentra en: 

  gvSIG/plugins/org.gvsig.scripting.app.mainplugin/scripts/addons/AutodeteccionAlturas/datos

La segunda parte de la herramienta necesita de una capa de resultados proveniente del anterior 
geoproceso, y una capa de catastro.

Ficheros de ejemplo se encuentra en: 

  gvSIG/plugins/org.gvsig.scripting.app.mainplugin/scripts/addons/AutodeteccionAlturas/datos/ayuntamiento

Capa de parcelas: constru_ayuntamiento_valencia
Capa de poligonos: resultado_poligonos_ayuntamiento

