import fast_route as fr


# calles = np.loadtxt("data\Calles.txt", dtype=np.str_ , delimiter=",")
# intersecciones = np.loadtxt("data\Interseccion.txt", dtype=int, delimiter=",")

# g = grafo.grafo()

# for c in calles:
#     g.agregarVertice(int(c[0]))

# for  inter in intersecciones:
#     g.agregarArista(int(inter[0]), int(inter[1]), 0)

# g.dibujar_grafo_graphiz()

if __name__ == "__main__":
    program = fr.Fast_Route()
    program.leer_archivos()
    program.realizar_grafo()
    program.realizar_dijkstra(10)
    program.hallar_camino_corto(10,120)
