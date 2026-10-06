# =====================================================================
# PROCESO 4 · ControladorCurso (TAREA 3)
# No usa print() ni input(). Devuelve (exito, mensaje) o datos.
# =====================================================================

# Permite ejecutar este archivo solo (botón ▶) para hacer sus pruebas
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.curso import Curso, CAMPOS_CURSO
from shared.archivo_json import ArchivoJSON
from shared.utilidades import siguiente_id, buscar_posicion


class ControladorCurso:

    CAMPOS = CAMPOS_CURSO

    def __init__(self, nombre_archivo="cursos.json"):
        self.archivo = ArchivoJSON(nombre_archivo)

    def claves_usadas(self, registros, excepto_id=None):
        """SET de TUPLAS (nombre, paralelo, periodo) que ya existen."""
        claves = set()
        for r in registros:
            if r["id"] != excepto_id:
                claves.add(Curso.desde_diccionario(r).clave())
        return claves

    # ---------------- C · CREAR ----------------
    def crear(self, datos):
        curso = Curso(0, datos["nombre"], datos["paralelo"], datos["periodo"])
        errores = curso.validar()
        if errores:
            return False, " ".join(errores)

        registros = self.archivo.leer()
        if curso.clave() in self.claves_usadas(registros):
            return False, "Ya existe ese curso con ese paralelo en ese periodo."

        curso.id = siguiente_id(registros)
        registros.append(curso.a_diccionario())
        self.archivo.guardar(registros)
        return True, f"Curso {curso.nombre} {curso.paralelo} creado con id {curso.id}."

    # ---------------- R · LEER ----------------
    def obtener_todos(self):
        return [Curso.desde_diccionario(r) for r in self.archivo.leer()]

    def obtener_por_id(self, id_curso):
        for curso in self.obtener_todos():
            if curso.id == id_curso:
                return curso
        return None

    # ---------------- BUSCAR ----------------
    def buscar(self, texto):
        texto = texto.strip().lower()
        encontrados = []
        for curso in self.obtener_todos():
            for campo in self.CAMPOS:
                if texto in getattr(curso, campo).lower():
                    encontrados.append(curso)
                    break
        return encontrados

    # ---------------- U · ACTUALIZAR ----------------
    def actualizar(self, id_curso, datos):
        registros = self.archivo.leer()
        posicion = buscar_posicion(registros, id_curso)
        if posicion is None:
            return False, f"No existe un curso con id {id_curso}."

        nuevo = Curso(id_curso, datos["nombre"], datos["paralelo"], datos["periodo"])
        errores = nuevo.validar()
        if errores:
            return False, " ".join(errores)
        if nuevo.clave() in self.claves_usadas(registros, excepto_id=id_curso):
            return False, "Ya existe otro curso con ese nombre, paralelo y periodo."

        registros[posicion] = nuevo.a_diccionario()
        self.archivo.guardar(registros)
        return True, f"Curso {id_curso} actualizado."

    # ---------------- D · ELIMINAR ----------------
    def eliminar(self, id_curso):
        registros = self.archivo.leer()
        quedan = [r for r in registros if r["id"] != id_curso]
        if len(quedan) == len(registros):
            return False, f"No existe un curso con id {id_curso}."
        self.archivo.guardar(quedan)
        return True, f"Curso {id_curso} eliminado."


# ---------------------------------------------------------------------
# PRUEBAS: se ejecutan solo si abres ESTE archivo y le das ▶ (Run).
# ---------------------------------------------------------------------
def probar():
    from shared.utilidades import mostrar_prueba
    print("\n=== PRUEBAS DE ControladorCurso ===")
    c = ControladorCurso("prueba_cursos.json")
    c.archivo.borrar()

    primero = {"nombre": "Primer semestre", "paralelo": "A", "periodo": "2026-2"}
    exito, _ = c.crear(primero)
    mostrar_prueba("Crear un curso correcto", exito)

    exito, mensaje = c.crear(dict(primero, paralelo="a"))
    mostrar_prueba("No deja repetir el mismo curso -> " + mensaje, not exito)

    exito, _ = c.crear(dict(primero, paralelo="B"))
    mostrar_prueba("Sí deja el mismo curso en otro paralelo", exito)

    exito, mensaje = c.actualizar(2, dict(primero, paralelo="A"))
    mostrar_prueba("No deja actualizar a un curso que ya existe -> " + mensaje, not exito)

    exito, _ = c.eliminar(2)
    mostrar_prueba("Eliminar un curso", exito and len(c.obtener_todos()) == 1)

    c.archivo.borrar()


if __name__ == "__main__":
    probar()
