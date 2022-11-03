import math
import heapq as hq
import numpy as np
import calle
import interseccion
import random
import pandas as pd
from collections import defaultdict


class Fast_Route:
    def __init__(self):
        self.letura_intersecciones = pd.read_csv("data\Interseccion.txt", sep=";", header=None)
        self.calles = dict()
        self.intersecciones = {}
        self.grafo_ruta = defaultdict(list)


    def leer_archivos(self):
        # Mapeo de datos al un diccionario de objetos tipo Interseccion
        for linea in self.letura_intersecciones.index:
            self.intersecciones[
                (self.letura_intersecciones[5][linea], self.letura_intersecciones[6][linea])
            ] = interseccion.Interseccion( self.letura_intersecciones[1][linea],
                self.letura_intersecciones[2][linea], self.letura_intersecciones[5][linea], self.letura_intersecciones[6][linea], self.letura_intersecciones[7][linea],
                self.letura_intersecciones[11][linea], self.letura_intersecciones[12][linea], self.letura_intersecciones[13][linea], self.letura_intersecciones[14][linea]
            )

    def realizar_grafo(self):
        # TODO--> Realizar validacion en el UI para que seleccione si la ruta es con trafico o no.
        # TODO--> Hallar la distancia entre dos puntos
        for clave in self.intersecciones:
                self.grafo_ruta[self.intersecciones[clave].origenId].append(
                    (self.intersecciones[clave].destinoId, self.intersecciones[clave].distancia))

    def dijkstra(self, nodoInicial):
        visitado = defaultdict(lambda: False)
        recorrido = defaultdict(lambda: None)
        distancia_recorrido = defaultdict(lambda: math.inf)
        distancia_recorrido[nodoInicial] = 0
        cola_nodo = [(0, nodoInicial)]
        while cola_nodo:
            pesoAcumulado, nodoActual = hq.heappop(cola_nodo)
            if not visitado[nodoActual]:
                visitado[nodoActual] = True
                for nodoVecino, peso in self.grafo_ruta[nodoActual]:
                    temp_peso = float(pesoAcumulado) + float(peso)
                    if temp_peso < distancia_recorrido[nodoVecino]:
                        distancia_recorrido[nodoVecino] = temp_peso
                        recorrido[nodoVecino] = nodoActual
                        hq.heappush(cola_nodo, (temp_peso, nodoVecino))
        return recorrido, distancia_recorrido

    def camino_corto(self, nodoInicial, nodoFinal, recorrido):
        no_camino = False
        nodoAnterior = nodoFinal
        caminoCorto = [nodoFinal]
        while not no_camino:
            if recorrido[nodoAnterior] == None:
                return False
            nodoAnterior = recorrido[nodoAnterior]
            caminoCorto.insert(0, nodoAnterior)
            if nodoAnterior == nodoInicial:
                no_camino = True
        return caminoCorto

    def hallar_camino_corto(self, nodoInicial, nodoFinal):
        recorrido, distancia_recorrido = self.dijkstra(nodoInicial)
        camino_corto = self.camino_corto(nodoInicial, nodoFinal, recorrido)

        print(camino_corto)
        print("El costo es: ", distancia_recorrido[nodoFinal], "km")

        if camino_corto == False:
            return False
        
        return [camino_corto, distancia_recorrido[nodoFinal]]


