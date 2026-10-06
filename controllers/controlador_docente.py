# =====================================================================
# PROCESO 4 · ControladorDocente (TAREA 1)
# Mismas operaciones que ControladorEstudiante, pero para docentes.
# No usa print() ni input(). Devuelve (exito, mensaje) o datos.
# =====================================================================

# Permite ejecutar este archivo solo (botón ▶) para hacer sus pruebas
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.docente import Docente, CAMPOS_DOCENTE
from shared.archivo_json import ArchivoJSON
from shared.utilidades import siguiente_id, valores_usados, buscar_posicion


class ControladorDocente:

    CAMPOS = CAMPOS_DOCENTE

    def __init__(self, nombre_archivo="docentes.json"):
        self.archivo = ArchivoJSON(nombre_archivo)

    # ---------------- C · CREAR ----------------
    def crear(self, datos):
        docente = Docente(0, datos["nombre"], datos["apellido"],
                          datos["email"], datos["especialidad"])
        errores = docente.validar()
        if errores:
            return False, " ".join(errores)

        registros = self.archivo.leer()
        if docente.email.lower() in valores_usados(registros, "email"):
            return False, "Ese email ya está registrado. Use otro email."

        docente.id = siguiente_id(registros)
        registros.append(docente.a_diccionario())
        self.archivo.guardar(registros)
        return True, f"Docente {docente.nombre_completo()} creado con id {docente.id}."

    # ---------------- R · LEER ----------------
    def obtener_todos(self):
        return [Docente.desde_diccionario(r) for r in self.archivo.leer()]

    def obtener_por_id(self, id_docente):
        for docente in self.obtener_todos():
            if docente.id == id_docente:
                return docente
        return None

    # ---------------- BUSCAR ----------------
    def buscar(self, texto):
        texto = texto.strip().lower()
        encontrados = []
        for docente in self.obtener_todos():
            for campo in self.CAMPOS:
                if texto in getattr(docente, campo).lower():
                    encontrados.append(docente)
                    break
        return encontrados

    # ---------------- U · ACTUALIZAR ----------------
    def actualizar(self, id_docente, datos):
        registros = self.archivo.leer()
        posicion = buscar_posicion(registros, id_docente)
        if posicion is None:
            return False, f"No existe un docente con id {id_docente}."

        nuevo = Docente(id_docente, datos["nombre"], datos["apellido"],
                        datos["email"], datos["especialidad"])
        errores = nuevo.validar()
        if errores:
            return False, " ".join(errores)
        if nuevo.email.lower() in valores_usados(registros, "email", id_docente):
            return False, "Ese email ya lo usa otro docente."

        registros[posicion] = nuevo.a_diccionario()
        self.archivo.guardar(registros)
        return True, f"Docente {id_docente} actualizado."

    # ---------------- D · ELIMINAR ----------------
    def eliminar(self, id_docente):
        registros = self.archivo.leer()
        quedan = [r for r in registros if r["id"] != id_docente]
        if len(quedan) == len(registros):
            return False, f"No existe un docente con id {id_docente}."
        self.archivo.guardar(quedan)
        return True, f"Docente {id_docente} eliminado."


# ---------------------------------------------------------------------
# PRUEBAS: se ejecutan solo si abres ESTE archivo y le das ▶ (Run).
# ---------------------------------------------------------------------
def probar():
    from shared.utilidades import mostrar_prueba
    print("\n=== PRUEBAS DE ControladorDocente ===")
    c = ControladorDocente("prueba_docentes.json")
    c.archivo.borrar()

    daniel = {"nombre": "Daniel", "apellido": "Vera",
              "email": "dvera@unemi.edu.ec", "especialidad": "Software"}
    exito, _ = c.crear(daniel)
    mostrar_prueba("Crear un docente correcto", exito)

    exito, mensaje = c.crear(dict(daniel, email="DVERA@unemi.edu.ec"))
    mostrar_prueba("No deja repetir el email (aunque cambien mayúsculas) -> " + mensaje,
                   not exito)

    exito, mensaje = c.crear(dict(daniel, email="sin-arroba"))
    mostrar_prueba("No deja crear con email mal escrito", not exito)

    mostrar_prueba("Buscar 'soft' encuentra al docente", len(c.buscar("soft")) == 1)

    exito, _ = c.actualizar(1, dict(daniel, especialidad="Bases de datos"))
    mostrar_prueba("Actualizar la especialidad",
                   exito and c.obtener_por_id(1).especialidad == "Bases de datos")

    exito, _ = c.eliminar(1)
    mostrar_prueba("Eliminar el docente", exito and c.obtener_todos() == [])

    exito, mensaje = c.eliminar(50)
    mostrar_prueba("No elimina un id que no existe -> " + mensaje, not exito)

    c.archivo.borrar()


if __name__ == "__main__":
    probar()
