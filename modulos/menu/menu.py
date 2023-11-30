import inquirer
import sys
import json
import webbrowser
import pickle
from tabulate import tabulate

class Menu:
    def __init__(self):
        self.slices = [] # data obtenida de la db
        pass

    def cargar_usuarios(self):
        try:
            with open("usuarios.pkl", "rb") as file:
                self.usuarios = pickle.load(file)
        except FileNotFoundError:
            self.usuarios = {}

    def grafico_topologia(self):
        id = input('[?] Ingrese el ID de la topologia: ')
        # TODO validar que sea un ID valido (int o string)
        # TODO validar que exista el ID

        # TODO con el ID se obtiene la topologia buscada dentro de self.topologies
        topologia_json = {
            "nodes": [
                {
                    "id": 0,
                    "name": "PC0",
                    "icon": "host",
                    "Management": "192.168.0.10/24",
                    "vncLink": "https://tipo.vnrt/token=?"
                },
                {
                    "id": 1,
                    "name": "PC1",
                    "icon": "host",
                    "Management": "192.168.0.10/24",
                    "vncLink": "https://tipo.vnrt/token=?"
                },
                {
                    "id": 2,
                    "name": "PC2",
                    "icon": "host",
                    "Management": "192.168.0.10/24",
                    "vncLink": "https://tipo.vnrt/token=?"
                }
            ],
            "links": [
                {
                    "source": 0,
                    "target": 1,

                    "srcDevice": "PC0",
                    "tgtDevice": "PC1",

                    "srcIfName": "ens1",
                    "tgtIfName": "ens3"
                },
                {
                    "source": 0,
                    "target": 2,

                    "srcDevice": "PC0",
                    "tgtDevice": "PC2",

                    "srcIfName": "ens2",
                    "tgtIfName": "ens3"
                }
            ]
        }

        # TODO se formatea a JSON para el modulo visualizacion (usar el json de la opcion1.3)
        # opciones "icon": unknown, switch, router, server, phone, host, cloud, firewall

        # TODO se guarda en ./modulos/visualizador/data.json
        header = "\n\nvar topologyData = "
        with open('modulos/visualizador/data.js', 'w') as data_json:
            data_json.write(header)
            data_json.write(json.dumps(topologia_json, indent=4, sort_keys=True))
            data_json.write(';')

        # TODO se abre el browser para visualizar la topologia
        webbrowser.open_new_tab('modulos/visualizador/app.html')

    def opcion_1(self):
        opciones_opcion_1 = [
            ("Tabla resumen de todas las Slices", 1),
            ("Tabla con detalle de una Slice en particular", 2),
            ("JSON con detalle de una Slice en particular", 3),
            ("Gráfico de Slice en particular", 4),
            ("Regresar", 5)
        ]

        while True:
            respuesta = inquirer.prompt([
                inquirer.List('opcion', message="Seleccione una opción", choices=opciones_opcion_1)
            ])

            sub_opcion = respuesta['opcion']

            if sub_opcion == 1:
                # TODO: Lógica para mostrar resumen de todas las topologías
                pass
            elif sub_opcion == 2:
                # TODO: Lógica para mostrar detalle de una topología
                pass
            elif sub_opcion == 3:
                # TODO: Lógica para mostrar JSON de una topología
                pass
            elif sub_opcion == 4:
                self.grafico_topologia()
            elif sub_opcion == 5:
                break


    def iniciar_menu(self):
        menu_options = [
            ("Listar Slices existentes", 1),
            ("Crear nuevo Slice", 2),
            ("Editar Slice", 3),
            ("Gestionar usuarios", 4),
            ("Salir", 5)
        ]

        while True:
            respuesta = inquirer.prompt([
                inquirer.List('opcion', message="Seleccione una opción", choices=menu_options)
            ])

            opcion = respuesta['opcion']

            if opcion == 1:
                self.opcion_1()
            elif opcion == 2:
                self.crear_topologia()
            elif opcion == 3:
                # Lógica para editar topología
                pass
            elif opcion == 4:
                self.gestionar_usuarios()
            elif opcion == 5:
                self.guardar_usuarios()
                sys.exit(0)

    def guardar_usuarios(self):
        with open("usuarios.pkl", "wb") as file:
            pickle.dump(self.usuarios, file)


# Para ejecutar el menú
if __name__ == "__main__":
    menu = Menu()
    menu.iniciar_menu()
