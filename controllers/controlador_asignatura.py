# =====================================================================
# PROCESO 4 · ControladorAsignatura (TAREA 2)
# No usa print() ni input(). Devuelve (exito, mensaje) o datos.
# =====================================================================

# Permite ejecutar este archivo solo (botón ▶) para hacer sus pruebas
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.asignatura import Asignatura, CAMPOS_ASIGNATURA
from shared.archivo_json import ArchivoJSON
from shared.utilidades import siguiente_id, valores_usados, buscar_posicion


class ControladorAsignatura:

    CAMPOS = CAMPOS_ASIGNATURA

    def __init__(self, nombre_archivo="asignaturas.json"):
        self.archivo = ArchivoJSON(nombre_archivo)

    # ---------------- C · CREAR ----------------
    def crear(self, datos):
        asignatura = Asignatura(0, datos["codigo"], datos["nombre"], datos["creditos"])
        errores = asignatura.validar()
        if errores:
            return False, " ".join(errores)

        registros = self.archivo.leer()
        if asignatura.codigo.lower() in valores_usados(registros, "codigo"):
            return False, f"Ya existe una asignatura con código {asignatura.codigo}. Use otro código."

        asignatura.id = siguiente_id(registros)
        registros.append(asignatura.a_diccionario())
        self.archivo.guardar(registros)
        return True, f"Asignatura {asignatura.nombre} creada con id {asignatura.id}."

    # ---------------- R · LEER ----------------
    def obtener_todos(self):
        return [Asignatura.desde_diccionario(r) for r in self.archivo.leer()]

    def obtener_por_id(self, id_asignatura):
        for asignatura in self.obtener_todos():
            if asignatura.id == id_asignatura:
                return asignatura
        return None

    # ---------------- BUSCAR ----------------
    def buscar(self, texto):
        texto = texto.strip().lower()
        encontrados = []
        for asignatura in self.obtener_todos():
            for campo in self.CAMPOS:
                if texto in str(getattr(asignatura, campo)).lower():
                    encontrados.append(asignatura)
                    break
        return encontrados

    # ---------------- U · ACTUALIZAR ----------------
    def actualizar(self, id_asignatura, datos):
        registros = self.archivo.leer()
        posicion = buscar_posicion(registros, id_asignatura)
        if posicion is None:
            return False, f"No existe una asignatura con id {id_asignatura}."

        nueva = Asignatura(id_asignatura, datos["codigo"], datos["nombre"], datos["creditos"])
        errores = nueva.validar()
        if errores:
            return False, " ".join(errores)
        if nueva.codigo.lower() in valores_usados(registros, "codigo", id_asignatura):
            return False, "Ese código ya lo usa otra asignatura."

        registros[posicion] = nueva.a_diccionario()
        self.archivo.guardar(registros)
        return True, f"Asignatura {id_asignatura} actualizada."

    # ---------------- D · ELIMINAR ----------------
    def eliminar(self, id_asignatura):
        registros = self.archivo.leer()
        quedan = [r for r in registros if r["id"] != id_asignatura]
        if len(quedan) == len(registros):
            return False, f"No existe una asignatura con id {id_asignatura}."
        self.archivo.guardar(quedan)
        return True, f"Asignatura {id_asignatura} eliminada."


# ---------------------------------------------------------------------
# PRUEBAS: se ejecutan solo si abres ESTE archivo y le das ▶ (Run).
# ---------------------------------------------------------------------
def probar():
    from shared.utilidades import mostrar_prueba
    print("\n=== PRUEBAS DE ControladorAsignatura ===")
    c = ControladorAsignatura("prueba_asignaturas.json")
    c.archivo.borrar()

    mate = {"codigo": "MAT101", "nombre": "Matemática", "creditos": "4"}
    exito, _ = c.crear(mate)
    mostrar_prueba("Crear una asignatura correcta", exito)

    exito, mensaje = c.crear(dict(mate, codigo="mat101"))
    mostrar_prueba("No deja repetir el código -> " + mensaje, not exito)

    exito, mensaje = c.crear({"codigo": "FIS1", "nombre": "Física", "creditos": "veinte"})
    mostrar_prueba("No acepta créditos con letras -> " + mensaje, not exito)

    mostrar_prueba("Los créditos se guardan como número",
                   c.archivo.leer()[0]["creditos"] == 4)

    exito, _ = c.actualizar(1, dict(mate, creditos="5"))
    mostrar_prueba("Actualizar los créditos", exito and c.obtener_por_id(1).creditos == "5")

    exito, _ = c.eliminar(1)
    mostrar_prueba("Eliminar la asignatura", exito and c.obtener_todos() == [])

    c.archivo.borrar()


if __name__ == "__main__":
    probar()
