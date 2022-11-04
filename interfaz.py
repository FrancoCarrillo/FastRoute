from tkinter import *
from tkinter import messagebox
from tkinter.font import Font
from tkinter.ttk import Combobox
import fast_route as fr
import webbrowser
from geojson import Point, Feature, FeatureCollection, dump, LineString
import os
import folium

def validar_vacio(campo):
    if campo == "" or campo.isspace():
        return False
    else:
        return True


def leerCalles():
    # Se debe retornar la lista.
    with open("data/Interseccion_prueba.txt", "r", encoding="utf-8") as archivo:
        id_calle = []
        nombre_calle = []
        for linea in archivo:
            id_calle.append(linea.split(";")[5])
            nombre_calle.append(linea.split(";")[0] + " " + linea.split(";")[2])
    return id_calle, nombre_calle

def buscarCalleXId(lista_ids):
    lista_ids = [
        str(i)
        for i in lista_ids
    ]
    # Ahora si leer el archivo y buscar el nombre de la calle
    with open("data/Interseccion_prueba.txt", "r", encoding="utf-8") as archivo:
        lista = []
        # Se debe buscar en todo el archivo id por id en el orden que vienen los de lista_ids. Y no debe continuar hasta que lo encuentre
        for id in lista_ids:
            archivo.seek(0)
            for linea in archivo:
                if id == linea.split(";")[5]:
                    lista.append(linea.split(";")[2])
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
        self.id_origen, self.direccionesOrigen =  self.id_destino, self.direccionesDestino = leerCalles()
        self.bg = "#ffffff"
        self.fg = "#000000"
        self.btnFg = "#ffffff"
        self.btnBg = "#0077c2"
        self.padX = 20
        self.padY = 10
        self.iniciar("Menu")
        self.program = fr.Fast_Route()
        self.program.leer_archivos()
        self.program.realizar_grafo()
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

        # Lista desplegable de direcciones de origen
        lblOrigen = Label(
            self.ventana_principal,
            text="Origen",
            font=("Arial", 12),
            bg=self.bg,
            fg=self.fg,
        )
        lblOrigen.grid(row=2, column=0, padx=self.padX, pady=self.padY)

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
            
            lista_listas = self.program.hallar_camino_corto(id_origen, id_destino)

            if lista_listas == False:
                messagebox.showerror("Error", "No se ha encontrado una ruta")
            else:
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
                Ruta(origen, destino, calles, tiempo_total, check, lista_direcciones, self.program)
        else:
            messagebox.showerror("Error", "Debe ingresar origen y destino")


class Ruta(InterfazGenerica):
    def __init__(self, origen, destino, lista_direcciones, tiempo_total, checkTrafico, direccioes_id, program):
        super().__init__()
        self.w = 500
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
        self.direccioes_id = direccioes_id
        self.program = program
        self.iniciar("Ruta")
        if self.checkTrafico:
            lblTituloRuta = Label(
                self.ventana_principal,
                text="La Ruta demora " + str(int(tiempo_total)) + " minutos",
                font=("Arial", 20, "bold"),
                bg=self.bg,
                fg=self.fg,
            )
        else:
            if float(tiempo_total) < 1:
                lblTituloRuta = Label(
                    self.ventana_principal,
                    text="La Ruta tiene " + str(round(float(tiempo_total)*1000,2)) + " metros",
                    font=("Arial", 20, "bold"),
                    bg=self.bg,
                    fg=self.fg,
                )
            else:
                lblTituloRuta = Label(
                    self.ventana_principal,
                    text="La Ruta tiene " + str(round(float(tiempo_total),2)) + " kilometros",
                    font=("Arial", 20, "bold"),
                    bg=self.bg,
                    fg=self.fg,
                )
        lblTituloRuta.grid(
            row=0, column=0, columnspan=2, padx=self.padX, pady=self.padY
        )


        scroll = Scrollbar(self.ventana_principal, orient=VERTICAL)
        scroll.grid(row=1, column=1, columnspan=1, rowspan=len(self.lista), sticky="ns")
        self.listaDirecciones = Listbox(
            self.ventana_principal, yscrollcommand=scroll.set
        )
        for i in range(len(self.lista)):
            ruta = str(i + 1) + " "  + self.lista[i]
            self.listaDirecciones.insert(END, ruta)
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
            padx=self.padX,
            pady=self.padY,
            )
            
        btnMapa = Button(
            self.ventana_principal,
            text="Mostrar Mapa",
            font=("Arial", 12),
            bg=self.btnBg,
            fg=self.btnFg,
            command= self.mostrar_mapa,
        )
        # El boton regresar debe ir abajo del listbox
        btnMapa.grid(
            row=len(self.lista) + 1,
            column=1,
            padx=self.padX,
            pady=self.padY,
            )

        self.ventana_principal.mainloop()

    def regresar(self):
        self.ventana_principal.destroy()
        Menu()


    def hacer_mapa(self, direccioes_id, program):
        m = folium.Map(location=(program.intersecciones[(direccioes_id[0], direccioes_id[0 + 1])].origenX, program.intersecciones[(direccioes_id[0], direccioes_id[0 + 1])].origenY), zoom_start=17)
        folium.TileLayer(tiles='Stamen Terrain', attr="<a href=https://endless-sky.github.io/>Endless Sky</a>").add_to(m)
        features = []

        len_intersecciones = len(direccioes_id)

        folium.Marker(
            (program.intersecciones[(direccioes_id[0], direccioes_id[0 + 1])].origenX, program.intersecciones[(direccioes_id[0], direccioes_id[0 + 1])].origenY),
            popup=f"<i>{program.intersecciones[(direccioes_id[0], direccioes_id[0 + 1])].calle}</i>", 
            tooltip="Start Place",
            icon=folium.Icon(color="green")
        ).add_to(m)



        anterior = -1
        
        range_geo = len(direccioes_id) - 1

        for indice in range(range_geo):
            if anterior != int(program.intersecciones[(direccioes_id[indice], direccioes_id[indice + 1])].calleId):
                anterior = int(program.intersecciones[(direccioes_id[indice], direccioes_id[indice + 1])].calleId)
            
            if indice == range_geo-1:
                folium.Marker(
                        (program.intersecciones[(direccioes_id[indice], direccioes_id[indice+1])].destinoX, 
                        program.intersecciones[(direccioes_id[indice], direccioes_id[indice+1])].destinoY), 
                        popup=f"<i>{program.intersecciones[(direccioes_id[indice], direccioes_id[indice+1])].calle}</i>", 
                        tooltip="End Place",
                        icon=folium.Icon(color="red")
                    ).add_to(m)

            linea = LineString([(program.intersecciones[(direccioes_id[indice], direccioes_id[indice + 1])].origenY, 
                            program.intersecciones[(direccioes_id[indice], direccioes_id[indice + 1])].origenX), (
                            program.intersecciones[(direccioes_id[indice], direccioes_id[indice + 1])].destinoY,
                            program.intersecciones[(direccioes_id[indice], direccioes_id[indice + 1])].destinoX)], color="red")
            features.append(Feature(geometry=linea))

        feature_collection = FeatureCollection(features)

        with open('temp/fast_route.geojson', 'w') as f:
            dump(feature_collection, f)

        rutaData = os.path.join("temp/fast_route.geojson")
        folium.GeoJson(rutaData, name='fast_route').add_to(m)
        m.save("index.html")
        webbrowser.open_new_tab('index.html')

    def mostrar_mapa(self):
        self.hacer_mapa(self.direccioes_id, self.program)

if __name__ == "__main__":
    Menu()
