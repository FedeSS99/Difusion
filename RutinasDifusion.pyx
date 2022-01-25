# cython: language_level = 3

import cython

import numpy as np
cimport numpy as np

ctypedef np.float64_t Dtype_t

from libc.stdlib cimport rand
from libc.stdio cimport printf

cdef extern from "math.h":
    Dtype_t atan(Dtype_t arg) nogil
    Dtype_t fabs(Dtype_t arg) nogil


@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
cdef Dtype_t sumaVecinos(np.ndarray[Dtype_t, ndim=2] Arreglo, int x, int y):
    cdef:
        Dtype_t suma_total = 0
        int N = <int> Arreglo.shape[0]
        int x1, x2, y1, y2

    x1 = x + 1
    x2 = x - 1
    if x1 == N:
        x1 = 0
    if x2 == -1:
        x2 = N-1

    y1 = y + 1
    y2 = y - 1
    if y1 == N:
        y1 = 0
    if y2 == -1:
        y2 = N-1

    suma_total = Arreglo[x,y1] + Arreglo[x,y2] + Arreglo[x1,y] + Arreglo[x2,y]
    suma_total += Arreglo[x1,y1] + Arreglo[x1,y2] + Arreglo[x1,y1] + Arreglo[x2,y2]

    return suma_total

@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
@cython.cdivision(True)
def DifusionLim(np.ndarray[Dtype_t, ndim=2] Superficie,int Nceldas):
    cdef:
        int N = <int>Superficie.shape[0]
        int posX, posY, dx, dy
        int i
        Dtype_t vecinos_contados, pi, distNorm, maxDist
        int cenX, cenY
    
    pi = 4.0*atan(1.0)
    maxDist = (2**0.5)*N
    cenX = N/2
    cenY = cenX

    for i in range(1, Nceldas+1):
        while True:  
            posX = rand() % N
            posY = rand() % N
            if Superficie[posX, posY]==0:
                break

        vecinos_contados = sumaVecinos(Superficie, posX, posY)
        if vecinos_contados>0:
            difX = posX - cenX
            difY = posY - cenY
            distNorm = <Dtype_t>(difX*difX + difY*difY)**0.5 / maxDist
            Superficie[posX, posY]= 1.0 - 4.0*fabs(atan(distNorm))/pi

        else:
            while True:
                dx = rand() % 3 - 1
                dy = rand() % 3 - 1

                posX += dx
                posY += dy

                if posX == N:
                    posX = 0
                elif posX == -1:
                    posX = N-1

                if posY == N:
                    posY = 0
                if posY == -1:
                    posY = N-1


                vecinos_contados = sumaVecinos(Superficie, posX, posY)

                if vecinos_contados>0:
                    difX = posX - cenX
                    difY = posY - cenY
                    distNorm = <Dtype_t>(difX*difX + difY*difY)**0.5 / maxDist
                    Superficie[posX, posY]= 1.0 - 4.0*fabs(atan(distNorm))/pi
                    printf("Celda %d terminada con valor de %f\r", i, Superficie[posX,posY])
                    break
