import getpass
import pickle
import inquirer
from tabulate import tabulate
import networkx as nx
import matplotlib.pyplot as plt
def guardar_usuarios(usuarios):
    with open("usuarios.pkl", "wb") as file:
        pickle.dump(usuarios, file)

def renombrar_nodos(G):
    nombres_maquinas = {nodo: f"vm{nodo}" for nodo in G.nodes()}
    return nx.relabel_nodes(G, nombres_maquinas)

def crear_topologia_lineal(num_maquinas):
    G = nx.path_graph(num_maquinas)
    G = renombrar_nodos(G)
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, node_size=500, node_color="skyblue", font_size=10, font_color="black")
    plt.title("Topología Lineal")
    plt.show()

def crear_topologia_arbol(r, h):
    G = nx.balanced_tree(r, h)
    G = renombrar_nodos(G)
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, node_size=500, node_color="skyblue", font_size=10, font_color="black")
    plt.title("Topología de Árbol")
    plt.show()



def crear_topologia_malla_full_mesh(num_maquinas):
    G = nx.complete_graph(num_maquinas)
    G = renombrar_nodos(G)
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, node_size=500, node_color="skyblue", font_size=10, font_color="black")
    plt.title("Topología de Malla (Full Mesh)")
    plt.show()


def crear_topologia_anillo(num_maquinas):
    G = nx.cycle_graph(num_maquinas)
    G = renombrar_nodos(G)
    pos = nx.circular_layout(G)
    nx.draw_networkx_nodes(G, pos, node_size=500, node_color="skyblue")
    nx.draw_networkx_edges(G, pos)
    nx.draw_networkx_labels(G, pos, font_size=10, font_color="black")
    plt.title("Topología de Anillo")
    plt.axis("off")
    plt.show()



usuarios = {
    "admin": {"contraseña": "admin", "rol": "admin", "slices": []},
    "user": {"contraseña": "user", "rol": "usuario_normal", "slices": []}
}

usuarios["admin"]["slices"].append({"Nombre": "Slice AWS Admin", "Arquitectura": "AWS"})
usuarios["user"]["slices"].append({"Nombre": "Slice AWS user", "Arquitectura": "aws"})
usuarios["user"]["slices"].append({"Nombre": "Slice 2", "Arquitectura": "aws"})


def mostrar_bienvenida():
    print("\n" + "=" * 50)
    print("Bienvenido al Sistema".center(50))
    print("=" * 50)


def obtener_datos_usuario():
    preguntas = [
        inquirer.Text('usuario', message="Ingrese su nombre de usuario"),
        inquirer.Password('contraseña', message="Ingrese su contraseña")
    ]
    return inquirer.prompt(preguntas)


topologias_options = {
    "1": "Lineal",
    "2": "Árbol",
    "3": "Malla",
    "4": "Anillo",
    "5": "Salir"
}

slices_creados = {}

try:
    with open("slices.pkl", "rb") as file:
        slices_creados = pickle.load(file)
except FileNotFoundError:
    slices_creados = {}



def print_menu(title, options):
    print("\n" + "=" * 50)
    print(f"{title.center(50)}")
    print("=" * 50)

    questions = [
        inquirer.List('opcion',
                      message="Selecciona una operación:",
                      choices=[(option, key) for key, option in options.items()],
                      )
    ]
    respuesta = inquirer.prompt(questions)

    print("=" * 50)
    return respuesta['opcion']


while True:
    mostrar_bienvenida()
    datos_usuario = obtener_datos_usuario()
    usuario = datos_usuario['usuario']
    contraseña = datos_usuario['contraseña']

    if usuario in usuarios and usuarios[usuario]["contraseña"] == contraseña:
        rol = usuarios[usuario]["rol"]
        print("Bienvenido,", usuario + " (Rol: " + rol + ")!")

        while True:
            if rol == "usuario_normal":
                menu_options = {
                    "1": "Crear slice",
                    "2": "Listar mis slices",
                    "3": "Borrar slice",
                    "4": "Editar Slice",
                    "5": "Salir"
                }
                opcion = print_menu("Menú Principal - Usuario Normal", menu_options)
                print(f"Opción seleccionada: {opcion}")

                if opcion == "5":
                    with open("slices.pkl", "wb") as file:
                        pickle.dump(slices_creados, file)
                    print("¡Hasta luego, " + usuario + "!")
                    break


                elif opcion == "1":
                    arquitectura_options = {
                        "1": "Aws",
                        "2": "Openstack",
                        "3": "Salir"
                    }

                    arquitectura = print_menu("Selección de Arquitectura", arquitectura_options)
                    print(f"Arquitectura seleccionada: {arquitectura}")

                    if arquitectura == "3":
                        continue

                    elif arquitectura == "1" or arquitectura == "2":
                        while True:
                            region_options = {
                                "1": "USA",
                                "2": "Latinoamerica",
                                "3": "Salir"
                            }
                            region = print_menu("Selección de Region", region_options)
                            print(f"Region seleccionada: {region}")

                            if region == "3":
                                break
                            elif region == "1":
                                while True:
                                    topologia_questions = [
                                        inquirer.List('topologia',
                                                      message="Selecciona una topología:",
                                                      choices=[(topologia, key) for key, topologia in
                                                               topologias_options.items()],
                                                      )
                                    ]
                                    topologia_respuesta = inquirer.prompt(topologia_questions)
                                    topologia = topologia_respuesta['topologia']
                                    print(f"Topología seleccionada: {topologias_options[topologia]}")

                                    if topologia == "5":
                                        break

                                    elif topologia in topologias_options:
                                        topo_seleccionada = topologias_options[topologia]

                                        nombre_slice = input("Ingresa un nombre para la slice: ")
                                        num_cpus = int(input("Ingresa la cantidad de CPUs: "))

                                        # Variables específicas para la topología de árbol
                                        r = h = None
                                        if topo_seleccionada == "Árbol":
                                            r = int(input("Ingrese el número de ramificaciones por nodo: "))
                                            h = int(input("Ingrese la altura del árbol: "))

                                        total_ram = 0
                                        total_almacenamiento = 0
                                        cpus_info = []

                                        for cpu_num in range(1, num_cpus + 1):
                                            print(f"\nDetalles para la CPU {cpu_num}:")
                                            ram = int(input("Ingresa la cantidad de RAM en MB para esta CPU: "))
                                            almacenamiento = int(
                                                input("Ingresa la cantidad de almacenamiento en MB para esta CPU: "))

                                            cpus_info.append(
                                                {"CPU": cpu_num, "RAM": ram, "Almacenamiento": almacenamiento})
                                            total_ram += ram
                                            total_almacenamiento += almacenamiento

                                        slice_info = {
                                            "Nombre": nombre_slice,
                                            "Topología": topo_seleccionada,
                                            "Total CPUs": num_cpus,
                                            "Total RAM": total_ram,
                                            "Total Almacenamiento": total_almacenamiento,
                                            "Detalle CPUs": cpus_info,
                                            "Ramificaciones": r if r else None,
                                            "Altura": h if h else None
                                        }

                                        if usuario not in slices_creados:
                                            slices_creados[usuario] = []
                                        slices_creados[usuario].append(slice_info)

                                        print(
                                            f"\nSlice creado exitosamente. Detalles del Slice: {slice_info['Nombre']}")
                                        cpu_headers = ["CPU", "RAM (MB)", "Alm. (MB)"]
                                        cpu_table = [[cpu['CPU'], cpu['RAM'], cpu['Almacenamiento']] for cpu in
                                                     slice_info["Detalle CPUs"]]
                                        print(tabulate(cpu_table, cpu_headers, tablefmt="grid"))
                                        post_creation_questions = [
                                            inquirer.List('post_creation_action',
                                                          message="¿Qué acción deseas realizar ahora?",
                                                          choices=['Imprimir topología', 'Mostrar JSON', 'Ambos',
                                                                   'Volver al menú principal'],
                                                          )
                                        ]
                                        post_creation_action = inquirer.prompt(post_creation_questions)[
                                            'post_creation_action']

                                        if post_creation_action == 'Imprimir topología' or post_creation_action == 'Ambos':
                                            if slice_info['Topología'] == "Lineal":
                                                crear_topologia_lineal(slice_info['Total CPUs'])
                                            elif slice_info['Topología'] == "Árbol":
                                                r = slice_info.get('Ramificaciones',2)
                                                h = slice_info.get('Altura', 1)
                                                crear_topologia_arbol(r, h)
                                            elif slice_info['Topología'] == "Malla":
                                                crear_topologia_malla_full_mesh(slice_info['Total CPUs'])
                                            elif slice_info['Topología'] == "Anillo":
                                                crear_topologia_anillo(slice_info['Total CPUs'])
                                            else:
                                                print("Topología no reconocida.")

                                        if post_creation_action in ['Mostrar JSON', 'Ambos']:
                                            print(json.dumps(slice_info, indent=4))
                                        break
                                    else:
                                        print("Topología no válida. Por favor, selecciona una topología válida.")

                            elif region == "2":
                                print("No hay disponibilidad de Recursos en Latam. Intenta con otra región.")
                            else:
                                print("Opción no válida. Por favor, selecciona una región válida.")

                    else:
                        print("Arquitectura no válida. Por favor, selecciona una arquitectura válida.")
                elif opcion == "2":
                    print("\n=== Listado de Tus Slices ===\n")

                    if usuario in slices_creados and slices_creados[usuario]:
                        headers = ["ID", "Nombre", "Topología", "CPUs", "RAM (MB)", "Alm. (MB)"]
                        table = []

                        for idx, slice_info in enumerate(slices_creados[usuario], start=1):
                            row = [idx, slice_info['Nombre'], slice_info.get('Topología', 'No especificada'),
                                   slice_info.get('Total CPUs', 'N/A'), slice_info.get('Total RAM', 'N/A'),
                                   slice_info.get('Total Almacenamiento', 'N/A')]
                            table.append(row)

                        print(tabulate(table, headers, tablefmt="grid"))

                        detalle_opcion = input(
                            "\n¿Deseas ver detalles de algún slice? Ingresa el ID o 'salir' para volver al menú: ")
                        if detalle_opcion.lower() != 'salir':
                            try:
                                slice_idx = int(detalle_opcion) - 1
                                if 0 <= slice_idx < len(slices_creados[usuario]):
                                    selected_slice = slices_creados[usuario][slice_idx]
                                    print(f"\nDetalles del Slice: {selected_slice['Nombre']}")
                                    if 'Detalle CPUs' in selected_slice:
                                        cpu_headers = ["CPU", "RAM (MB)", "Alm. (MB)"]
                                        cpu_table = [[cpu['CPU'], cpu['RAM'], cpu['Almacenamiento']] for cpu in
                                                     selected_slice["Detalle CPUs"]]
                                        print(tabulate(cpu_table, cpu_headers, tablefmt="grid"))
                                        imprimir_topologia_opcion = input(
                                            "\n¿Deseas imprimir la topología de este slice? (sí/no): ")
                                        if imprimir_topologia_opcion.lower() == 'si':
                                            if selected_slice['Topología'] == "Malla":
                                                crear_topologia_malla_full_mesh(selected_slice['Total CPUs'])
                                            elif selected_slice['Topología'] == "Lineal":
                                                crear_topologia_lineal(slice_info['Total CPUs'])
                                            elif selected_slice['Topología'] == "Anillo":
                                                crear_topologia_anillo(slice_info['Total CPUs'])
                                            elif selected_slice['Topología'] == "Árbol":
                                                crear_topologia_arbol(selected_slice['Total CPUs'])



                                    else:
                                        print("No hay detalles adicionales disponibles para este slice.")
                                else:
                                    print("ID de slice no válido.")
                            except ValueError:
                                print("Entrada no válida. Por favor, ingresa un número de ID válido.")
                    else:
                        print("No tienes slices creados.\n")

                    input("\nPresiona Enter para volver al menú principal...")

                elif opcion == "3":

                    print("Selecciona el slice que deseas borrar:")
                    if usuario in slices_creados:
                        for idx, slice_info in enumerate(slices_creados[usuario], start=1):
                            print(f"{idx}. {slice_info['Nombre']}")

                        opcion_borrar = input("Ingresa el número del slice a borrar (o 'cancelar' para salir): ")
                        if opcion_borrar.lower() == 'cancelar':
                            continue

                        try:
                            opcion_borrar = int(opcion_borrar)
                            if opcion_borrar >= 1 and opcion_borrar <= len(slices_creados[usuario]):
                                slice_borrado = slices_creados[usuario].pop(opcion_borrar - 1)
                                print(f"Slice '{slice_borrado['Nombre']}' ha sido borrado correctamente.")
                            else:
                                print("Número de slice no válido.")
                        except ValueError:
                            print("Opción no válida. Ingresa un número válido o 'cancelar' para salir.")
                    else:
                        print("No tienes slices creados para borrar.")
                elif opcion == "4":

                    print("\n=== Edición de Slice ===")

                    if usuario in slices_creados:

                        for idx, slice_info in enumerate(slices_creados[usuario], start=1):
                            print(f"{idx}. {slice_info['Nombre']}")

                        opcion_editar = input("Ingresa el número de la slice a editar (o 'cancelar' para salir): ")
                        if opcion_editar.lower() == 'cancelar':
                            break

                        try:
                            opcion_editar = int(opcion_editar) - 1
                            if 0 <= opcion_editar < len(slices_creados[usuario]):
                                slice_a_editar = slices_creados[usuario][opcion_editar]


                                for cpu in slice_a_editar["Detalle CPUs"]:
                                    print(f"\nEditando CPU {cpu['CPU']}:")
                                    nuevo_cpu_ram = input(
                                        f"  Nueva RAM para CPU {cpu['CPU']} (Actual: {cpu['RAM']} MB, Enter para mantener): ")
                                    nuevo_cpu_almacenamiento = input(
                                        f"  Nuevo almacenamiento para CPU {cpu['CPU']} (Actual: {cpu['Almacenamiento']} MB, Enter para mantener): ")
                                    if nuevo_cpu_ram:
                                        cpu['RAM'] = int(nuevo_cpu_ram)
                                    if nuevo_cpu_almacenamiento:
                                        cpu['Almacenamiento'] = int(nuevo_cpu_almacenamiento)



                                print("Slice editado exitosamente.")
                            else:
                                print("Número de slice no válido.")
                        except ValueError:
                            print("Opción no válida. Ingresa un número válido o 'cancelar' para salir.")

                    else:
                        print("No tienes slices creados para editar.")


                else:
                    print("Opción no válida. Por favor, selecciona una opción válida.")

            elif rol == "admin":
                print("\n=== Menú Principal ===")
                print("Selecciona una operación:")
                print("1. Crear slice")
                print("2. Listar mis slices")
                print("3. Borrar slice")
                print("4. Editar Slice")
                print("5. Gestión de Usuarios")
                print("6. Salir")
                opcion = input("Ingresa el número de la operación que deseas realizar: ")

                if opcion == "6":
                    print("¡Hasta luego, " + usuario + "!")
                    break
                elif opcion == "5":
                    print("\n=== Gestión de Usuarios ===")
                    print("Selecciona una operación:")
                    print("1. Crear usuario")
                    print("2. Editar usuario")
                    print("3. Suspender usuario")
                    print("4. Listar usuario")
                    print("5. Salir")
                    opcion_gestion_usuarios = input("Ingresa el número de la operación que deseas realizar: ")

                    if opcion_gestion_usuarios == "5":
                        guardar_usuarios(usuario)
                        break
                    elif opcion_gestion_usuarios == "4":
                        print("\n=== Lista de Usuarios ===")
                        for nombre_usuario, info_usuario in usuarios.items():
                            if info_usuario["rol"] == "usuario_normal":
                                print(f"Usuario: {nombre_usuario}, Rol: {info_usuario['rol']}")
                    elif opcion_gestion_usuarios == "1":
                        nuevo_usuario = input("Ingrese el nombre del nuevo usuario: ")
                        nueva_contraseña = getpass.getpass("Ingrese la contraseña del nuevo usuario: ")

                        if nuevo_usuario in usuarios:
                            print("El usuario ya existe. No se puede crear.")
                        else:
                            usuarios[nuevo_usuario] = {"contraseña": nueva_contraseña, "rol": "usuario_normal",
                                                       "slices": []}
                            print(f"Usuario '{nuevo_usuario}' creado exitosamente.")
                            guardar_usuarios(usuario)
                    elif opcion_gestion_usuarios == "2":

                        usuario_a_editar = input("Ingrese el nombre del usuario a editar: ")

                        if usuario_a_editar not in usuarios:
                            print("El usuario no existe. No se puede editar.")
                        elif usuarios[usuario_a_editar]["rol"] != "usuario_normal":
                            print("Solo se pueden editar usuarios con rol 'usuario_normal'.")
                        else:
                            nueva_contraseña = getpass.getpass(
                                "Ingrese la nueva contraseña (deje en blanco para mantener la actual): ")
                            if nueva_contraseña:
                                usuarios[usuario_a_editar]["contraseña"] = nueva_contraseña
                                print(f"Contraseña del usuario '{usuario_a_editar}' actualizada.")
                            else:
                                print("No se ha realizado ninguna modificación en la contraseña.")

                    elif opcion_gestion_usuarios == "3":

                        usuario_a_suspender = input("Ingrese el nombre del usuario a suspender: ")

                        if usuario_a_suspender not in usuarios:
                            print("El usuario no existe. No se puede suspender.")
                        elif usuarios[usuario_a_suspender]["rol"] != "usuario_normal":
                            print("Solo se pueden suspender usuarios con rol 'usuario_normal'.")
                        else:

                            print(f"Usuario '{usuario_a_suspender}' suspendido exitosamente.")
                    else:
                        print("Opción no válida. Por favor, selecciona una opción válida.")


                elif opcion == "1":
                    print("\n=== Selección de Arquitectura ===")
                    print("Selecciona Arquitectura:")
                    print("1. Aws")
                    print("2.Openstack")
                    print("3. Salir")

                    arquitectura = input("Ingresa el número de la arquitectura a implementar: ")

                    if arquitectura == "3":
                        continue
                    elif arquitectura == "1" or arquitectura == "2":
                        while True:
                            print("\n=== Selección de Región ===")
                            print("Selecciona Región:")
                            print("1. USA")
                            print("2. Latam")
                            print("3. Salir")
                            region = input("Ingresa el número de la región: ")

                            if region == "3":
                                break
                            elif region == "1":
                                while True:
                                    print("Hay disponibilidad de recursos")
                                    print("\n=== Selección de Topología ===")
                                    print("Selecciona una topología:")

                                    for topo_id, topo_nombre in topologias_options.items():
                                        print(f"{topo_id}. {topo_nombre}")

                                    print("5. Salir")
                                    topo = input("Ingresa el número de la Topología: ")

                                    if topo == "5":
                                        break
                                    elif topo in topologias_options:
                                        topo_seleccionada = topologias_options[topo]
                                        print(f"Has seleccionado la topología: {topo_seleccionada}")

                                        nombre_slice = input("Ingresa un nombre para la slice: ")

                                        cpu = input("Ingresa la cantidad de CPU: ")
                                        ram = input("Ingresa la cantidad de RAM en MB: ")
                                        almacenamiento = input("Ingresa la cantidad de almacenamiento en MB: ")

                                        slice_info = {
                                            "Nombre": nombre_slice,
                                            "Topología": topo_seleccionada,
                                            "CPU": cpu,
                                            "RAM": ram,
                                            "Almacenamiento": almacenamiento
                                        }
                                        if usuario not in slices_creados:
                                            slices_creados[usuario] = []
                                        slices_creados[usuario].append(slice_info)

                                        print(f"Slice creado exitosamente con la siguiente información:")
                                        print(f"Nombre: {slice_info['Nombre']}")
                                        print(f"Topología: {slice_info['Topología']}")
                                        print(f"CPU: {slice_info['CPU']}")
                                        print(f"RAM: {slice_info['RAM']} MB")
                                        print(f"Almacenamiento: {slice_info['Almacenamiento']} MB")
                                    else:
                                        print("Topología no válida. Por favor, selecciona una topología válida.")

                            elif region == "2":
                                print("No hay disponibilidad de Recursos en Latam. Intenta con otra región.")
                            else:
                                print("Opción no válida. Por favor, selecciona una región válida.")

                    else:
                        print("Arquitectura no válida. Por favor, selecciona una arquitectura válida.")
                elif opcion == "2":
                    print("Listando tus slices...")

                    if usuario in slices_creados:
                        for idx, slice_info in enumerate(slices_creados[usuario], start=1):
                            print(f"\n Slice {idx}:")
                            print(f"Nombre: {slice_info['Nombre']}")
                            print(f"Topología: {slice_info.get('Topología', 'No especificada')}")
                            print(f"CPU: {slice_info['CPU']}")
                            print(f"RAM: {slice_info['RAM']} MB")
                            print(f"Almacenamiento: {slice_info['Almacenamiento']} MB")
                    else:
                        print("No tienes slices creados.")
                    if usuario in usuarios and "slices" in usuarios[usuario]:
                        print("\nInterfaces predefinidas:")
                        for idx, slice_info in enumerate(usuarios[usuario]["slices"], start=1):
                            print(f"\n Slice {idx}:")
                            print(f"Nombre: {slice_info['Nombre']}")
                            print(f"Arquitectura: {slice_info['Arquitectura']}")

                elif opcion == "3":

                    print("Selecciona el slice que deseas borrar:")
                    if usuario in slices_creados:
                        for idx, slice_info in enumerate(slices_creados[usuario], start=1):
                            print(f"{idx}. {slice_info['Nombre']}")

                        opcion_borrar = input("Ingresa el número del slice a borrar (o 'cancelar' para salir): ")
                        if opcion_borrar.lower() == 'cancelar':
                            continue

                        try:
                            opcion_borrar = int(opcion_borrar)
                            if opcion_borrar >= 1 and opcion_borrar <= len(slices_creados[usuario]):
                                slice_borrado = slices_creados[usuario].pop(opcion_borrar - 1)
                                print(f"Slice '{slice_borrado['Nombre']}' ha sido borrado correctamente.")
                            else:
                                print("Número de slice no válido.")
                        except ValueError:
                            print("Opción no válida. Ingresa un número válido o 'cancelar' para salir.")
                    else:
                        print("No tienes slices creados para borrar.")
                elif opcion == "4":

                    print("\n=== Edición de Slice ===")
                    print("Selecciona la slice que deseas editar:")

                    if usuario in slices_creados:
                        for idx, slice_info in enumerate(slices_creados[usuario], start=1):
                            print(f"{idx}. {slice_info['Nombre']}")

                        opcion_editar = input("Ingresa el número de la slice a editar (o 'cancelar' para salir): ")
                        if opcion_editar.lower() == 'cancelar':
                            continue

                        try:
                            opcion_editar = int(opcion_editar)
                            if opcion_editar >= 1 and opcion_editar <= len(slices_creados[usuario]):
                                slice_a_editar = slices_creados[usuario][opcion_editar - 1]

                                print("Editando slice:")
                                print(f"Nombre: {slice_a_editar['Nombre']}")
                                print(f"Topología: {slice_a_editar['Topología']}")
                                print(f"CPU: {slice_a_editar['CPU']}")
                                print(f"RAM: {slice_a_editar['RAM']} MB")
                                print(f"Almacenamiento: {slice_a_editar['Almacenamiento']} MB")

                                nuevo_nombre = input("Nuevo nombre para la slice (o Enter para mantener el mismo): ")
                                nuevo_cpu = input("Nueva cantidad de CPU (o Enter para mantener la misma): ")
                                nuevo_ram = input("Nueva cantidad de RAM en MB (o Enter para mantener la misma): ")
                                nuevo_almacenamiento = input(
                                    "Nueva cantidad de almacenamiento en MB (o Enter para mantener el mismo): ")

                                if nuevo_nombre:
                                    slice_a_editar['Nombre'] = nuevo_nombre
                                if nuevo_cpu:
                                    slice_a_editar['CPU'] = nuevo_cpu
                                if nuevo_ram:
                                    slice_a_editar['RAM'] = nuevo_ram
                                if nuevo_almacenamiento:
                                    slice_a_editar['Almacenamiento'] = nuevo_almacenamiento

                                print(f"Slice '{slice_a_editar['Nombre']}' ha sido editado correctamente.")
                            else:
                                print("Número de slice no válido.")
                        except ValueError:
                            print("Opción no válida. Ingresa un número válido o 'cancelar' para salir.")
                    else:
                        print("No tienes slices creados para editar.")
                else:
                    print("Opción no válida. Por favor, selecciona una opción válida.")


            else:
                print("Rol no válido.")

        with open("slices.pkl", "wb") as file:
            pickle.dump(slices_creados, file)
        break
    else:
        print("Usuario o contraseña incorrectos. Por favor, inténtalo de nuevo.")
