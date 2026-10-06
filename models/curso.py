# =====================================================================
# PROCESO 3 · Modelo Curso (TAREA 3)
# Ejemplo de curso: nombre "Primer semestre", paralelo "A", periodo "2026-2"
# =====================================================================

# Permite ejecutar este archivo solo (botón ▶) para hacer sus pruebas
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from shared.validaciones import esta_vacio

# TUPLA con los campos que el usuario escribe
CAMPOS_CURSO = ("nombre", "paralelo", "periodo")


class Curso:

    def __init__(self, id_curso, nombre, paralelo, periodo):
        self.id = id_curso
        self.nombre = str(nombre).strip()
        self.paralelo = str(paralelo).strip().upper()   # "a" -> "A"
        self.periodo = str(periodo).strip()

    def clave(self):
        """TUPLA que identifica al curso. No pueden existir dos cursos
        con el mismo nombre, paralelo y periodo."""
        return (self.nombre.lower(), self.paralelo.lower(), self.periodo.lower())

    def validar(self):
        """Devuelve una LISTA de errores. Lista vacía = datos correctos."""
        errores = []
        if esta_vacio(self.nombre):
            errores.append("El nombre del curso es obligatorio. Ejemplo: Primer semestre")
        if esta_vacio(self.paralelo):
            errores.append("El paralelo es obligatorio. Ejemplo: A")
        if esta_vacio(self.periodo):
            errores.append("El periodo es obligatorio. Ejemplo: 2026-2")
        return errores

    def a_diccionario(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "paralelo": self.paralelo,
            "periodo": self.periodo,
        }

    @classmethod
    def desde_diccionario(cls, datos):
        return cls(datos["id"], datos["nombre"], datos["paralelo"], datos["periodo"])

    def __str__(self):
        return f"[{self.id}] {self.nombre} - Paralelo {self.paralelo} ({self.periodo})"


# ---------------------------------------------------------------------
# PRUEBAS: se ejecutan solo si abres ESTE archivo y le das ▶ (Run).
# ---------------------------------------------------------------------
def probar():
    from shared.utilidades import mostrar_prueba
    print("\n=== PRUEBAS DEL MODELO Curso ===")

    bueno = Curso(1, "Primer semestre", "a", "2026-2")
    mostrar_prueba("Datos correctos no tienen errores", bueno.validar() == [])
    mostrar_prueba("El paralelo se guarda en mayúscula", bueno.paralelo == "A")

    sin_periodo = Curso(2, "Segundo semestre", "B", "")
    mostrar_prueba("Detecta periodo vacío", len(sin_periodo.validar()) == 1)

    todo_vacio = Curso(3, "", "", "")
    mostrar_prueba("Detecta los 3 campos vacíos", len(todo_vacio.validar()) == 3)

    otro = Curso(9, "PRIMER SEMESTRE", "A", "2026-2")
    mostrar_prueba("Dos cursos iguales tienen la misma clave (aunque cambien mayúsculas)",
                   bueno.clave() == otro.clave())

    copia = Curso.desde_diccionario(bueno.a_diccionario())
    mostrar_prueba("Convertir a diccionario y volver no pierde datos",
                   copia.a_diccionario() == bueno.a_diccionario())

    print("\nMensajes que vería el usuario si deja todo vacío:")
    for error in todo_vacio.validar():
        print("  -", error)


if __name__ == "__main__":
    probar()
