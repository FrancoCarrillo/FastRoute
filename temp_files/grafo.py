import vertice
import networkx as nx
import matplotlib.pyplot as plt
import graphviz as gv
import PIL

PIL.Image.MAX_IMAGE_PIXELS = 933120000


class Grafo:
    def __init__(self):
        self.vertices = {}
        self.grafo = nx.DiGraph()

    def agregarVertice(self, id):
        if id not in self.vertices:
            self.vertices[id] = vertice.vertice(id)

    def agregarArista(self, a, b, p):
        if a in self.vertices and b in self.vertices:
            self.vertices[a].agregarVecino(b, p)
            self.vertices[b].agregarVecino(a, p)

            #self.grafo.add_edge(str(a), str(b), weight=p)
            #self.grafo.add_edge(str(b), str(a))

    def camino(self, a, b):
        camino = []
        actual = b
        while actual != None:
            camino.insert(0, actual)
            actual = self.vertices[actual].padre
        return [camino, self.vertices[b].costo]

    def minimo(self, l):
        if len(l) > 0:
            m = self.vertices[l[0]].costo
            v = l[0]
            for e in l:
                if m > self.vertices[e].costo:
                    m = self.vertices[e].costo
                    v = e
            return v
        return None

    def dijkstra(self, a):
        if a in self.vertices:
            self.vertices[a].costo = 0
            actual = a
            noVisitados = []

            for v in self.vertices:
                noVisitados.append(v)

            while len(noVisitados) > 0:
                for vec in self.vertices[actual].vecinos:
                    if self.vertices[vec[0]].visitado == False:
                        if (
                            self.vertices[actual].costo + vec[1]
                            < self.vertices[vec[0]].costo
                        ):
                            self.vertices[vec[0]].costo = (
                                self.vertices[actual].costo + vec[1]
                            )
                            self.vertices[vec[0]].padre = actual

                self.vertices[actual].visitado = True
                noVisitados.remove(actual)

                actual = self.minimo(noVisitados)
        else:
            return False

    def imprimir(self):
        for v in self.vertices:
            print(
                "El costo del vertice "
                + str(self.vertices[v].id)
                + " es "
                + str(self.vertices[v].costo)
                + " llegando desde "
                + str(self.vertices[v].padre)
            )

    def dibujar_grafo_graphiz(self):
        """#Dibujar grafo con graphviz
        g = gv.Digraph(format='png')
        g.render('grafo', view=True)"""

        nx.nx_agraph.write_dot(self.grafo, "grafo.dot")
        # Mostrar el grafo usando graphviz
        nx.nx_agraph.view_pygraphviz(self.grafo, prog="dot")
        # Mostrar el grafo usando graphviz
        # gv.render('dot', 'pdf', 'grafo.dot')
        # print(PIL.Image.open('grafo.dot.pdf'))
