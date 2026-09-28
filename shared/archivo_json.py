"""
PROCESO 2 · Código reutilizable
Clase ArchivoJSON: es la ÚNICA parte del programa que toca el disco.

Recibe y devuelve LISTAS de DICCIONARIOS. No sabe qué es un Estudiante,
un Docente, una Asignatura ni un Curso: por eso la pueden usar todos los
controladores sin cambiar nada.
"""

import json
import os

# Carpeta raíz del proyecto (la que contiene main.py).
# Se calcula a partir de la ubicación de ESTE archivo, así el programa
# encuentra la carpeta data/ aunque se ejecute desde otra carpeta.
RAIZ_PROYECTO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CARPETA_DATA = os.path.join(RAIZ_PROYECTO, "data")


class ArchivoJSON:
    """Lee y guarda una lista de diccionarios en un archivo de la carpeta data/."""

    def __init__(self, nombre_archivo):
        self.ruta = os.path.join(CARPETA_DATA, nombre_archivo)
        # PROCESO 7: la carpeta data/ se crea automáticamente si no existe
        os.makedirs(CARPETA_DATA, exist_ok=True)

    def leer(self):
        """Devuelve SIEMPRE una lista: vacía si el archivo no existe o está dañado."""
        if not os.path.exists(self.ruta):
            return []
        try:
            with open(self.ruta, "r", encoding="utf-8") as archivo:
                datos = json.load(archivo)
            return datos if isinstance(datos, list) else []
        except (json.JSONDecodeError, OSError):
            # Capturamos errores concretos, nunca un "except:" pelado
            return []

    def guardar(self, datos):
        """Escribe la lista completa. Devuelve True si pudo guardar."""
        try:
            with open(self.ruta, "w", encoding="utf-8") as archivo:
                json.dump(datos, archivo, ensure_ascii=False, indent=2)
            return True
        except (TypeError, OSError):
            # TypeError aparece si intentas guardar un set: JSON no lo conoce
            return False
