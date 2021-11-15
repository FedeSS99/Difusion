# cython: language_level = 3

import cython

from random import choice
import numpy as np
from scipy.ndimage import convolve
cimport numpy as np


@cython.boundscheck(False)
@cython.wraparound(False)
def DifusionLim(double[:,:] Superficie,double[:,:] kernel,list Movimientos,int Nceldas,int i,int rmax):
    cdef:
        int N = Superficie.shape[0]
        int posX, posY
        int centro = int(N/2)

    while True:  
        posX, posY = np.random.randint(centro-rmax, centro+rmax, 2)
        if Superficie[posX, posY]==0:
            break

    vecinos_contados = convolve(Superficie, kernel, mode="constant")
    if vecinos_contados[posX, posY]>0:
        Superficie[posX, posY]= 0.5 + (i+1)/(2.0*(Nceldas))

    else:
        while True:
            pasox, pasoy = choice(Movimientos)
            posX += pasox
            posY += pasoy
            posX, posY= posX % N, posY % N

            if vecinos_contados[posX, posY]>0:
                rmax += 2
                if rmax > centro:
                    rmax += -2

                Superficie[posX, posY]= 1.0 - (i+1)/(2.0*(Nceldas))
                break
   
    return rmax