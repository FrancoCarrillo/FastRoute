class vertice:
	def __init__(self, i):
		self.id = i
		self.vecinos = []
		self.visitado = False
		self.padre = None
		self.costo = float('inf')

	def agregarVecino(self, v, p):
		if v not in self.vecinos:
			self.vecinos.append([v, p])