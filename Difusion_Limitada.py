import numpy as np
from math import hypot
from pyqtgraph.Qt import QtCore
from pyqtgraph.exporters import ImageExporter
import pyqtgraph as pg
from time import perf_counter
from os import system

from RutinasDifusion import DifusionLim


#Dimensiones de la "caja"
N = 200
#Numero de celdas caminantes
Nceldas =  3000
radioMax = 4

PosiblesMovimientos = [(1,1),(1,-1),(-1,-1),(-1,1)]

kernel = np.array([[1,1,1],[1,0,1],[1,1,1]], dtype=np.float64)
dist = hypot(*PosiblesMovimientos[0])

#Creamos la superficie original con una "gota" en el centro
Superficie = np.zeros((N,N)).astype(np.float64)
celda_centro = int(N/2)
Superficie[celda_centro, celda_centro] = 0.5

#Fijamos el aspecto de la ventana para siempre visualizar
#celdas cuadradas
ventana = pg.GraphicsLayoutWidget(size=(600,600))
ventana.setWindowTitle("Simulación de difusión limitada, FPS=0.0, Num. Partículas=0")
vista = ventana.addViewBox()
vista.setAspectLocked(True)

#Creamos la imagen donde desplagaremos nuestro arreglo de difusion
ImagenSuperficie = pg.ImageItem()
vista.addItem(ImagenSuperficie)
#Fijamos dimensiones visuales iniciales
vista.setRange(QtCore.QRectF(0,0, N, N))

#Fijando mapa de color
cm = pg.colormap.get(name="gnuplot2", source="matplotlib")
bar = pg.ColorBarItem(values=(0.0, 1.0), colorMap=cm)
bar.setImageItem(ImagenSuperficie)

#Fijamos el estado inicial
ImagenSuperficie.setImage(Superficie)
ventana.show()

#Iniciando la exportación de la simulación a imagenes
particula = 0
#exporter = ImageExporter(ventana.scene())
#exporter.export(f".\ImagenesDifLim\DifLimitada_{particula}.png")

TiempoActualizar = perf_counter()
transcurrido = 0.0

timer = QtCore.QTimer()
timer.setSingleShot(True)

print(f"Iniciando en una malla de {N}x{N} con {Nceldas} particulas...")

def ActualizarSuperficie():
    global radioMax, TiempoActualizar, transcurrido,particula
    radioMax = DifusionLim(Superficie, kernel, PosiblesMovimientos, Nceldas, particula, radioMax)
    ImagenSuperficie.setImage(Superficie)
    
    particula += 1

    timer.start(1)
    TiempoAct = perf_counter()
    TiempoTrans = TiempoAct - TiempoActualizar
    TiempoActualizar = TiempoAct
    transcurrido = transcurrido*0.9 + TiempoTrans*0.1
    ventana.setWindowTitle(f"Simulación de difusión limitada, FPS={1.0/transcurrido:.2f}, Num. Partículas={particula}")
    #exporter.export(f".\ImagenesDifLim\DifLimitada_{particula}.png")

    if particula==Nceldas:
        timer.stop()

timer.timeout.connect(ActualizarSuperficie)
ActualizarSuperficie()

if __name__=="__main__":
    pg.exec()
    #system("ffmpeg -framerate 60 -i .\ImagenesDifLim\DifLimitada_%d.png DifLimitada.mp4")