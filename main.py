import math
import grafo 
import numpy as np


calles = np.loadtxt("data\Calles.txt", dtype=np.str_ , delimiter=",")
intersecciones = np.loadtxt("data\Interseccion.txt", dtype=int, delimiter=",")

g = grafo.grafo()

for c in calles:
    g.agregarVertice(int(c[0]))

for  inter in intersecciones:
    g.agregarArista(int(inter[0]), int(inter[1]), 0)

g.dibujar_grafo_graphiz()