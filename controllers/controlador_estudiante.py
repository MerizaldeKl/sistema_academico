# =====================================================================
# PROCESO 4 · ControladorEstudiante (lógica CRUD)
# CRUD = Crear, Leer, Actualizar (Update), Eliminar (Delete) + Buscar.
#
# Reglas del controlador:
#   - NO usa print() ni input(): no habla con el usuario.
#   - Devuelve una TUPLA (exito, mensaje) o devuelve datos.
#   - Valida ANTES de guardar en el archivo.
# =====================================================================

# Permite ejecutar este archivo solo (botón ▶) para hacer sus pruebas
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.estudiante import Estudiante, CAMPOS_ESTUDIANTE
from shared.archivo_json import ArchivoJSON
from shared.utilidades import siguiente_id, valores_usados, buscar_posicion


class ControladorEstudiante:

    CAMPOS = CAMPOS_ESTUDIANTE   # la Vista usa esta tupla para armar el formulario

    def __init__(self, nombre_archivo="estudiantes.json"):
        # Cada controlador tiene su propio archivo JSON en data/
        self.archivo = ArchivoJSON(nombre_archivo)

    # ---------------- C · CREAR ----------------
    def crear(self, datos):
        """datos: DICCIONARIO con nombre, apellido, email y carnet."""
        estudiante = Estudiante(0, datos["nombre"], datos["apellido"],
                                datos["email"], datos["carnet"])

        # 1) ¿Los datos están bien escritos?
        errores = estudiante.validar()
        if errores:
            return False, " ".join(errores)

        # 2) ¿El email o el carnet ya existen? (se busca en un SET)
        registros = self.archivo.leer()
        if estudiante.email.lower() in valores_usados(registros, "email"):
            return False, "Ese email ya está registrado. Use otro email."
        if estudiante.carnet.lower() in valores_usados(registros, "carnet"):
            return False, "Ese carnet ya está registrado. Use otro carnet."

        # 3) Le doy un id, lo agrego a la LISTA y guardo
        estudiante.id = siguiente_id(registros)
        registros.append(estudiante.a_diccionario())
        self.archivo.guardar(registros)
        return True, f"Estudiante {estudiante.nombre_completo()} creado con id {estudiante.id}."

    # ---------------- R · LEER ----------------
    def obtener_todos(self):
        """Devuelve una LISTA de objetos Estudiante."""
        return [Estudiante.desde_diccionario(r) for r in self.archivo.leer()]

    def obtener_por_id(self, id_estudiante):
        """Devuelve el estudiante con ese id, o None si no existe."""
        for estudiante in self.obtener_todos():
            if estudiante.id == id_estudiante:
                return estudiante
        return None

    # ---------------- BUSCAR ----------------
    def buscar(self, texto):
        """Devuelve los estudiantes que contienen el texto en algún campo."""
        texto = texto.strip().lower()
        encontrados = []
        for estudiante in self.obtener_todos():
            for campo in self.CAMPOS:
                if texto in getattr(estudiante, campo).lower():
                    encontrados.append(estudiante)
                    break   # ya coincidió, paso al siguiente estudiante
        return encontrados

    # ---------------- U · ACTUALIZAR ----------------
    def actualizar(self, id_estudiante, datos):
        registros = self.archivo.leer()
        posicion = buscar_posicion(registros, id_estudiante)
        if posicion is None:
            return False, f"No existe un estudiante con id {id_estudiante}."

        nuevo = Estudiante(id_estudiante, datos["nombre"], datos["apellido"],
                           datos["email"], datos["carnet"])
        errores = nuevo.validar()
        if errores:
            return False, " ".join(errores)

        # excepto_id: no comparo el estudiante consigo mismo
        if nuevo.email.lower() in valores_usados(registros, "email", id_estudiante):
            return False, "Ese email ya lo usa otro estudiante."
        if nuevo.carnet.lower() in valores_usados(registros, "carnet", id_estudiante):
            return False, "Ese carnet ya lo usa otro estudiante."

        registros[posicion] = nuevo.a_diccionario()   # reemplazo en la lista
        self.archivo.guardar(registros)
        return True, f"Estudiante {id_estudiante} actualizado."

    # ---------------- D · ELIMINAR ----------------
    def eliminar(self, id_estudiante):
        registros = self.archivo.leer()
        # Lista NUEVA con todos menos el que se elimina
        quedan = [r for r in registros if r["id"] != id_estudiante]
        if len(quedan) == len(registros):
            return False, f"No existe un estudiante con id {id_estudiante}."
        self.archivo.guardar(quedan)
        return True, f"Estudiante {id_estudiante} eliminado."


# ---------------------------------------------------------------------
# PRUEBAS: se ejecutan solo si abres ESTE archivo y le das ▶ (Run).
# Usan un archivo de prueba para no tocar los datos reales.
# ---------------------------------------------------------------------
def probar():
    from shared.utilidades import mostrar_prueba
    print("\n=== PRUEBAS DE ControladorEstudiante ===")
    c = ControladorEstudiante("prueba_estudiantes.json")
    c.archivo.borrar()

    ana = {"nombre": "Ana", "apellido": "Pérez", "email": "ana@correo.com", "carnet": "EST001"}
    exito, _ = c.crear(ana)
    mostrar_prueba("Crear un estudiante correcto", exito)

    exito, mensaje = c.crear(ana)
    mostrar_prueba("No deja repetir el email -> " + mensaje, not exito)

    otro = dict(ana, email="otra@correo.com")   # mismo carnet, otro email
    exito, mensaje = c.crear(otro)
    mostrar_prueba("No deja repetir el carnet -> " + mensaje, not exito)

    vacio = {"nombre": "", "apellido": "", "email": "x", "carnet": ""}
    exito, mensaje = c.crear(vacio)
    mostrar_prueba("No deja crear con datos vacíos", not exito)

    mostrar_prueba("Leer todos devuelve 1 estudiante", len(c.obtener_todos()) == 1)
    mostrar_prueba("Buscar 'pér' encuentra a Ana", len(c.buscar("pér")) == 1)
    mostrar_prueba("Buscar 'zzz' no encuentra nada", c.buscar("zzz") == [])

    cambios = dict(ana, nombre="Ana María")
    exito, _ = c.actualizar(1, cambios)
    mostrar_prueba("Actualizar el nombre", exito and c.obtener_por_id(1).nombre == "Ana María")

    exito, mensaje = c.actualizar(99, cambios)
    mostrar_prueba("No actualiza un id que no existe -> " + mensaje, not exito)

    exito, _ = c.eliminar(1)
    mostrar_prueba("Eliminar el estudiante", exito and c.obtener_todos() == [])

    exito, mensaje = c.eliminar(1)
    mostrar_prueba("No elimina un id que ya no existe -> " + mensaje, not exito)

    c.archivo.borrar()   # dejamos todo limpio


if __name__ == "__main__":
    probar()
