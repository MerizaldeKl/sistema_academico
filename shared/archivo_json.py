# =====================================================================
# PROCESO 2 · Código reutilizable
# Clase ArchivoJSON: es la ÚNICA parte del programa que lee y escribe
# archivos. Guarda una LISTA de DICCIONARIOS en un archivo .json
# dentro de la carpeta data/.
# =====================================================================

import json   # librería de Python para trabajar con archivos JSON
import os     # librería de Python para trabajar con carpetas y rutas

# Ruta de la carpeta principal del proyecto (donde está main.py).
# Así la carpeta data/ siempre se crea en el lugar correcto.
CARPETA_PROYECTO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CARPETA_DATA = os.path.join(CARPETA_PROYECTO, "data")


class ArchivoJSON:

    def __init__(self, nombre_archivo):
        # Ejemplo: nombre_archivo = "estudiantes.json"
        self.ruta = os.path.join(CARPETA_DATA, nombre_archivo)
        # PROCESO 7: si la carpeta data/ no existe, se crea sola
        os.makedirs(CARPETA_DATA, exist_ok=True)

    def leer(self):
        """Devuelve la lista guardada. Si no hay archivo o está dañado, devuelve []."""
        if not os.path.exists(self.ruta):
            return []
        try:
            with open(self.ruta, "r", encoding="utf-8") as archivo:
                return json.load(archivo)
        except json.JSONDecodeError:
            # El archivo existe pero tiene texto que no es JSON válido
            return []

    def guardar(self, lista):
        """Escribe la lista completa en el archivo."""
        with open(self.ruta, "w", encoding="utf-8") as archivo:
            # indent=2 deja el archivo ordenado y fácil de leer
            # ensure_ascii=False permite guardar tildes y la ñ
            json.dump(lista, archivo, indent=2, ensure_ascii=False)

    def borrar(self):
        """Elimina el archivo. Solo se usa en las pruebas."""
        if os.path.exists(self.ruta):
            os.remove(self.ruta)


# ---------------------------------------------------------------------
# PRUEBAS: se ejecutan solo si abres ESTE archivo y le das ▶ (Run).
# Si el archivo es importado por otro, estas pruebas NO se ejecutan.
# ---------------------------------------------------------------------
def probar():
    print("\n=== PRUEBAS DE ArchivoJSON ===")
    archivo = ArchivoJSON("prueba_archivo.json")
    archivo.borrar()

    # Prueba 1: si el archivo no existe, leer() devuelve una lista vacía
    print("✔ Leer archivo inexistente da []" if archivo.leer() == []
          else "✘ ERROR al leer archivo inexistente")

    # Prueba 2: lo que se guarda es lo mismo que se lee después
    datos = [{"id": 1, "nombre": "Ána Núñez"}]
    archivo.guardar(datos)
    print("✔ Guardar y leer devuelve los mismos datos" if archivo.leer() == datos
          else "✘ ERROR al guardar o leer")

    # Prueba 3: si el archivo está dañado, no se cae el programa
    with open(archivo.ruta, "w", encoding="utf-8") as f:
        f.write("esto no es json")
    print("✔ Archivo dañado devuelve [] sin caerse" if archivo.leer() == []
          else "✘ ERROR con archivo dañado")

    archivo.borrar()   # dejamos todo limpio


if __name__ == "__main__":
    probar()
