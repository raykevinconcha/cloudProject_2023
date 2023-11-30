import inquirer
import sys
import json
import webbrowser
import pickle
from tabulate import tabulate
from ..logging.Exceptions import InputException

from ..validador.validador import obtener_int
from ..validador.validador import obtener_tipo_topologia
from ..validador.validador import obtener_infraestructura

from ..validador.validador import obtener_numero_vcpus
from ..validador.validador import obtener_memoria
from ..validador.validador import obtener_fs
from ..validador.validador import obtener_imagen

from ..administracion.administracion import importar_imagen

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

    def opcion_2(self):
        """
        # TODO se rellenaría un objeto de Topología con los atributos obtenidos
        tipo_topologia = None
        infraestructura = None
        try:
            print() # se imprime una nueva línea en el menú
            tipo_topologia = obtener_tipo_topologia()
            infraestructura = obtener_infraestructura()

            # TODO se pide el número de vms a crear y para cada vm se piden los siguientes datos
            n_vcpus = obtener_numero_vcpus()
            memoria = obtener_memoria()
            # fs = obtener_fs()
            # imagen = obtener_imagen()

            # TODO preguntar qué VLANs desea interconectar

        except InputException as inputException:
            print(inputException)
            return

        # TODO mostrar resumen de información ingresada para que el usuario confirme

        # TODO se crean las VMs usando el módulo correspondiente
        """

    def opcion_3(self):
        opciones_opcion_3 = [
            ("Borrar topología", 1),
            ("Añadir nodo en topología", 2),
            ("Eliminar nodo en topología", 3),
            ("Aumentar capacidad de slice", 4),
            ("Editar conectividad", 5),
            ("Añadir imagen", 6),
            ("Regresar", 7)
        ]
        while True:
            respuesta = inquirer.prompt([
                inquirer.List('opcion', message="Seleccione una opción", choices=opciones_opcion_3)
            ])

            sub_opcion = respuesta['opcion']

            if sub_opcion == 1:
                # TODO: Lógica para borrar topología
                pass
            elif sub_opcion == 2:
                # TODO: Lógica para añadir nodo en topología
                pass
            elif sub_opcion == 6:
                importar_imagen()
                pass
            elif sub_opcion == 7:
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
                self.opcion_2()
            elif opcion == 3:
                self.opcion_3()
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
