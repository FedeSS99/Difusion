from numpy import zeros, float64
from pyqtgraph.Qt import QtCore
import pyqtgraph as pg

from RutinasDifusion import DifusionLim

#Dimensiones de la "caja"
N = 512
#Numero de celdas caminantes
Nceldas =  15000

#Creamos la superficie original con una "gota" en el centro
Superficie = zeros((N,N)).astype(float64)
celda_centro = int(N/2)
Superficie[celda_centro, celda_centro] = 1.0

#Fijamos el aspecto de la ventana para siempre visualizar
#celdas cuadradas
ventana = pg.GraphicsLayoutWidget(size=(700,700))
ventana.setWindowTitle(f"Simulación de difusión limitada, {Nceldas=}")
vista = ventana.addViewBox()
vista.setAspectLocked(True)

#Creamos la imagen donde desplagaremos nuestro arreglo de difusion
ImagenSuperficie = pg.ImageItem()
vista.addItem(ImagenSuperficie)
#Fijamos dimensiones visuales iniciales
vista.setRange(QtCore.QRectF(0,0, N, N))

#Fijando mapa de color
cm = pg.colormap.get(name="nipy_spectral", source="matplotlib")
bar =pg.ColorBarItem(values=(0.0, 1.0), limits=(0.0, 1.0), colorMap=cm)
ventana.addItem(bar)
bar.setImageItem(ImagenSuperficie)

#Generamos el patrón de difusión entorno a un elemento en el centro
DifusionLim(Superficie, Nceldas)
ImagenSuperficie.setImage(Superficie)

ventana.show()

if __name__=="__main__":
    pg.exec()
