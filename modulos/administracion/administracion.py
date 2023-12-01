#!/usr/bin/env python3

from typing import Optional 
from ..validador.validador import obtener_int

def crear_vm(n_vcpus, memoria, tipo_fs, capacidad_fs:Optional[int]=None):
    pass

def importar_imagen():
    print('''
        1. Seleccionar un archivo local
        2. Ingresar un URL para ser descargado por el controlador
    ''')
    opcion = obtener_int('Ingrese la opcion: ', valoresValidos=[1,2])
    if (opcion == 1):
        # subir archivo local
        ruta = input('Ingrese la ruta del archivo: ')
        print('[+] Imagen importada correctamente') 
    elif (opcion == 2):
        # subir url

        ruta = input('Ingrese la url de la imagen: ') # VALIDADOR url
        print('[+] Imagen importada correctamente') 