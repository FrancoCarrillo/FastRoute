import math
import grafo
import numpy as np
import calle
import interseccion
import grafo
import random


class Fast_Route:
    def __init__(self):
        self.lectura_calles = np.loadtxt(
            "FastRoute/data/Calles.txt", dtype=np.str_, delimiter=","
        )
        self.letura_intersecciones = np.loadtxt(
            "FastRoute/data/Interseccion.txt",
            delimiter=",",
            converters=lambda x: float(x),
        )
        self.calles = dict()
        self.intersecciones = dict()
        self.grafo_ruta = grafo.Grafo()

    def leer_archivos(self):
        # Mapeo de datos al un diccionario de objetos tipo Calle
        for columna in self.lectura_calles:
            self.calles[int(columna[0])] = calle.Calle(int(columna[0]), columna[1])

        # Mapeo de datos al un diccionario de objetos tipo Interseccion
        for columna in self.letura_intersecciones:
            self.intersecciones[
                int(columna[0]), int(columna[1])
            ] = interseccion.Interseccion(
                int(columna[0]), int(columna[1]), columna[2], columna[3]
            )

    def realizar_grafo(self):
        # Agrega todos las calles como vertices del grafo
        for clave in self.calles:
            self.grafo_ruta.agregarVertice(int(self.calles[clave].id))

        # TODO--> Realizar validacion en el UI para que seleccione si la ruta es con trafico o no.
        # TODO--> Hallar la distancia entre dos puntos
        for clave in self.intersecciones:
            self.grafo_ruta.agregarArista(
                int(self.intersecciones[clave].calle1Id),
                int(self.intersecciones[clave].calle2Id),
                random.randint(1, 100),
            )

    def realizar_dijkstra(self, inicio):
        self.grafo_ruta.dijkstra(inicio)

    def hallar_camino_corto(self, inicio, final):
        print("Camino: ", self.grafo_ruta.camino(inicio, final))
        return self.grafo_ruta.camino(inicio, final)
