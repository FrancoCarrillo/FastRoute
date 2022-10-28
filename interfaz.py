from tkinter import *
from tkinter import messagebox
from tkinter.font import Font
from tkinter.ttk import Combobox
import fast_route as fr


def validar_vacio(campo):
    if campo == "" or campo.isspace():
        return False
    else:
        return True


def leerCalles():
    # El archivo Calles.txt contiene la información de las calles. Se debe leer el archivo y almacenar cada calle en una lista. Estan registradas en el formato: id_calle, nombre_calle.
    # Se debe retornar la lista.
    with open("FastRoute/data/Calles.txt", "r") as archivo:
        id_calle = []
        nombre_calle = []
        for linea in archivo:
            id_calle.append(linea.split(",")[0])
            nombre_calle.append(linea.split(",")[1])
    return id_calle, nombre_calle


def leerDirecciones():
    # Se debe almacenar en una lista las direcciones de origen. En el archivo direcciones.txt se encuentra la información de las direcciones de origen divididas por comas.
    # Se debe leer el archivo y almacenar cada dirección en una lista.
    # Se debe retornar la lista.
    with open("FastRoute/data/direcciones.txt", "r") as archivo:
        lista = archivo.read().split(",")
    return lista


def buscarCalleXId(lista_ids):
    lista_ids = [
        str(i)
        if len(str(i)) == 2 or len(str(i)) == 3 or len(str(i)) == 4
        else "0" + str(i)
        for i in lista_ids
    ]
    # Mostrar la lista_ids
    # print(lista_ids)
    # print("*****************")
    # Ahora si leer el archivo y buscar el nombre de la calle
    with open("FastRoute/data/Calles.txt", "r") as archivo:
        lista = []
        # Se debe buscar en todo el archivo id por id en el orden que vienen los de lista_ids. Y no debe continuar hasta que lo encuentre
        for id in lista_ids:
            archivo.seek(0)
            for linea in archivo:
                if id == linea.split(",")[0]:
                    lista.append(linea.split(",")[1])
                    break
    return lista


class InterfazGenerica:
    def __init__(self):
        self.w = 800
        self.h = 400
        self.ventana_principal = Tk()
        self.iniciar()

    def iniciar(self, ventana_nombre=None):
        screen_width = self.ventana_principal.winfo_screenwidth()
        screen_height = self.ventana_principal.winfo_screenheight()
        x = (screen_width / 2) - (self.w / 2)
        y = (screen_height / 2) - (self.h / 2)
        self.ventana_principal.title(ventana_nombre)
        self.ventana_principal.geometry("%dx%d+%d+%d" % (self.w, self.h, x, y))
        self.ventana_principal.config(bg="#ffffff")
        self.ventana_principal.resizable(0, 0)


class Menu(InterfazGenerica):
    def __init__(self):
        super().__init__()
        self.w = 350
        self.h = 250
        self.id_origen, self.direccionesOrigen = leerCalles()
        self.id_destino, self.direccionesDestino = leerCalles()
        self.bg = "#ffffff"
        self.fg = "#000000"
        self.btnFg = "#ffffff"
        self.btnBg = "#0077c2"
        self.padX = 20
        self.padY = 10
        self.iniciar("Menu")
        lblTituloMenu = Label(
            self.ventana_principal,
            text="Menu",
            font=("Arial", 20, "bold"),
            bg=self.bg,
            fg=self.fg,
        )
        lblTituloMenu.grid(
            row=0, column=0, columnspan=2, padx=self.padX, pady=self.padY
        )
        # Checkbox con trafico o sin trafico
        self.trafico = IntVar()
        self.trafico.set(1)
        self.checkTrafico = Checkbutton(
            self.ventana_principal,
            text="Trafico",
            variable=self.trafico,
            onvalue=1,
            offvalue=0,
            bg=self.bg,
            fg=self.fg,
        )
        self.checkTrafico.grid(
            row=1, column=0, columnspan=2, padx=self.padX, pady=self.padY
        )

        lblOrigen = Label(
            self.ventana_principal,
            text="Origen",
            font=("Arial", 12),
            bg=self.bg,
            fg=self.fg,
        )
        lblOrigen.grid(row=2, column=0, padx=self.padX, pady=self.padY)
        # Lista desplegable de direcciones de origen
        # Se debe hacer un combo box
        self.comboOrigen = Combobox(
            self.ventana_principal, values=self.direccionesOrigen, state="readonly"
        )
        self.comboOrigen.grid(row=2, column=1, padx=self.padX, pady=self.padY)
        lblDestino = Label(
            self.ventana_principal,
            text="Destino",
            font=("Arial", 12),
            bg=self.bg,
            fg=self.fg,
        )
        lblDestino.grid(row=3, column=0, padx=self.padX, pady=self.padY)
        self.comboDestino = Combobox(
            self.ventana_principal, values=self.direccionesDestino, state="readonly"
        )
        self.comboDestino.grid(row=3, column=1, padx=self.padX, pady=self.padY)
        btnBuscar = Button(
            self.ventana_principal,
            text="Buscar",
            font=("Arial", 12),
            bg=self.btnBg,
            fg=self.btnFg,
            command=self.buscar,
        )
        btnBuscar.grid(row=4, column=0, columnspan=2, padx=self.padX, pady=self.padY)

        self.ventana_principal.mainloop()

    def buscar(self):
        if validar_vacio(self.comboOrigen.get()) and validar_vacio(
            self.comboDestino.get()
        ):
            messagebox.showinfo("Mensaje", "Buscando ruta")
            origen = self.comboOrigen.get()
            # Necesito el id de la calle de origen
            id_origen = self.id_origen[self.direccionesOrigen.index(origen)]
            id_destino = self.id_destino[
                self.direccionesDestino.index(self.comboDestino.get())
            ]
            try:
                id_origen = int(id_origen)
                id_destino = int(id_destino)
            except ValueError as e:
                print("Error" + str(e))
            # IMPLEMENTACION DE CODIGO DIJKSTRA
            program = fr.Fast_Route()
            program.leer_archivos()
            program.realizar_grafo()
            program.realizar_dijkstra(id_origen)
            lista_listas = program.hallar_camino_corto(id_origen, id_destino)
            lista_direcciones = []
            for lista in lista_listas[0]:
                lista_direcciones.append(lista)
            # Se debe obtener el tiempo total
            tiempo_total = lista_listas[1]
            destino = self.comboDestino.get()
            self.ventana_principal.destroy()
            calles = buscarCalleXId(lista_direcciones)
            # Castear la variable self.trafico a booleano
            if self.trafico.get() == 1:
                check = True
            else:
                check = False
            Ruta(origen, destino, calles, tiempo_total, check)
        else:
            messagebox.showerror("Error", "Debe ingresar origen y destino")


class Ruta(InterfazGenerica):
    def __init__(self, origen, destino, lista_direcciones, tiempo_total, checkTrafico):
        super().__init__()
        self.w = 400
        self.h = 330
        self.lista = lista_direcciones
        self.tiempo_total = tiempo_total
        self.origen = origen
        self.destino = destino
        self.checkTrafico = checkTrafico
        self.bg = "#ffffff"
        self.fg = "#000000"
        self.btnFg = "#ffffff"
        self.btnBg = "#0077c2"
        self.padX = 20
        self.padY = 10
        self.iniciar("Ruta")
        if self.checkTrafico:
            lblTituloRuta = Label(
                self.ventana_principal,
                text="La Ruta demora " + str(tiempo_total) + " minutos",
                font=("Arial", 20, "bold"),
                bg=self.bg,
                fg=self.fg,
            )
        else:
            lblTituloRuta = Label(
                self.ventana_principal,
                text="La Ruta tiene " + str(tiempo_total) + " metros",
                font=("Arial", 20, "bold"),
                bg=self.bg,
                fg=self.fg,
            )
        lblTituloRuta.grid(
            row=0, column=0, columnspan=2, padx=self.padX, pady=self.padY
        )
        # print("Origen : ", self.origen)
        # print("Destino : ", self.destino)
        scroll = Scrollbar(self.ventana_principal, orient=VERTICAL)
        scroll.grid(row=1, column=1, rowspan=len(self.lista), sticky="nsew")
        self.listaDirecciones = Listbox(
            self.ventana_principal, yscrollcommand=scroll.set
        )
        for i in range(len(self.lista)):
            self.listaDirecciones.insert(END, self.lista[i])
        font = Font(family="Arial", size=12, weight="normal")
        self.listaDirecciones.config(font=font)
        self.listaDirecciones.grid(
            row=1,
            column=0,
            rowspan=len(self.lista),
            sticky="nsew",
            padx=self.padX,
            pady=self.padY,
        )
        btnRegresar = Button(
            self.ventana_principal,
            text="Regresar",
            font=("Arial", 12),
            bg=self.btnBg,
            fg=self.btnFg,
            command=self.regresar,
        )
        # El boton regresar debe ir abajo del listbox
        btnRegresar.grid(
            row=len(self.lista) + 1,
            column=0,
            columnspan=2,
            padx=self.padX,
            pady=self.padY,
        )

        self.ventana_principal.mainloop()

    def regresar(self):
        self.ventana_principal.destroy()
        Menu()


if __name__ == "__main__":
    Menu()
