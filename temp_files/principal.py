from tkinter import *
from tkinter import messagebox
from tkinter.font import Font
from tkinter.ttk import Combobox


def validar_vacio(campo):
    if campo == "" or campo.isspace():
        return False
    else:
        return True


def leerCalles():
    # Se debe almacenar en una lista las calles de origen. En el archivo calles.txt se encuentra la información de las calles de origen divididas por comas.
    # Se debe leer el archivo y almacenar cada calle en una lista.
    # Se debe retornar la lista.
    with open("data/Calles.txt", "r") as archivo:
        lista = archivo.read().split(",")
    return lista


def leerDirecciones():
    # Se debe almacenar en una lista las direcciones de origen. En el archivo direcciones.txt se encuentra la información de las direcciones de origen divididas por comas.
    # Se debe leer el archivo y almacenar cada dirección en una lista.
    # Se debe retornar la lista.
    with open("data/direcciones.txt", "r") as archivo:
        lista = archivo.read().split(",")
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
        self.h = 200
        self.direccionesOrigen = leerCalles()
        self.direccionesDestino = leerCalles()
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
        lblOrigen = Label(
            self.ventana_principal,
            text="Origen",
            font=("Arial", 12),
            bg=self.bg,
            fg=self.fg,
        )
        lblOrigen.grid(row=1, column=0, padx=self.padX, pady=self.padY)
        # Lista desplegable de direcciones de origen
        # Se debe hacer un combo box
        self.comboOrigen = Combobox(
            self.ventana_principal, values=self.direccionesOrigen, state="readonly"
        )
        self.comboOrigen.grid(row=1, column=1, padx=self.padX, pady=self.padY)
        lblDestino = Label(
            self.ventana_principal,
            text="Destino",
            font=("Arial", 12),
            bg=self.bg,
            fg=self.fg,
        )
        lblDestino.grid(row=2, column=0, padx=self.padX, pady=self.padY)
        self.comboDestino = Combobox(
            self.ventana_principal, values=self.direccionesDestino, state="readonly"
        )
        self.comboDestino.grid(row=2, column=1, padx=self.padX, pady=self.padY)
        btnBuscar = Button(
            self.ventana_principal,
            text="Buscar",
            font=("Arial", 12),
            bg=self.btnBg,
            fg=self.btnFg,
            command=self.buscar,
        )
        btnBuscar.grid(row=3, column=0, columnspan=2, padx=self.padX, pady=self.padY)

        self.ventana_principal.mainloop()

    def buscar(self):
        if validar_vacio(self.comboOrigen.get()) and validar_vacio(
            self.comboDestino.get()
        ):
            messagebox.showinfo("Mensaje", "Buscando ruta")
            origen = self.comboOrigen.get()
            destino = self.comboDestino.get()
            self.ventana_principal.destroy()
            Ruta(origen, destino)
        else:
            messagebox.showerror("Error", "Debe ingresar origen y destino")


class Ruta(InterfazGenerica):
    def __init__(self, origen, destino):
        super().__init__()
        self.w = 400
        self.h = 330
        self.lista = leerDirecciones()
        self.origen = origen
        self.destino = destino
        self.bg = "#ffffff"
        self.fg = "#000000"
        self.btnFg = "#ffffff"
        self.btnBg = "#0077c2"
        self.padX = 20
        self.padY = 10
        self.iniciar("Ruta")
        lblTituloRuta = Label(
            self.ventana_principal,
            text="Ruta",
            font=("Arial", 20, "bold"),
            bg=self.bg,
            fg=self.fg,
        )
        lblTituloRuta.grid(
            row=0, column=0, columnspan=2, padx=self.padX, pady=self.padY
        )
        print("Origen : ", self.origen)
        print("Destino : ", self.destino)
        # Se debe hacer un for para que se muestren todas las direcciones en la lista : self.lista. Cada direccion se debe mostrar en un label. Debe haber un scroll para que se pueda ver todas las direcciones en caso de que sean muchas.
        # El scroll debe ir en la columna 1
        scroll = Scrollbar(self.ventana_principal, orient=VERTICAL)
        scroll.grid(row=1, column=1, rowspan=len(self.lista), sticky="nsew")
        # Las direcciones deben ir en la columna 0
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
