# =====================================================================
# PROCESO 3 · Modelo Asignatura (TAREA 2)
# =====================================================================

# Permite ejecutar este archivo solo (botón ▶) para hacer sus pruebas
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from shared.validaciones import esta_vacio, es_entero_en_rango

# TUPLA con los campos que el usuario escribe
CAMPOS_ASIGNATURA = ("codigo", "nombre", "creditos")


class Asignatura:

    def __init__(self, id_asignatura, codigo, nombre, creditos):
        self.id = id_asignatura
        self.codigo = str(codigo).strip().upper()   # upper(): MAT101 siempre en mayúsculas
        self.nombre = str(nombre).strip()
        self.creditos = str(creditos).strip()       # se valida que sea número

    def validar(self):
        """Devuelve una LISTA de errores. Lista vacía = datos correctos."""
        errores = []
        if esta_vacio(self.codigo):
            errores.append("El código es obligatorio. Ejemplo: MAT101")
        if esta_vacio(self.nombre):
            errores.append("El nombre es obligatorio. Ejemplo: Matemática")
        if not es_entero_en_rango(self.creditos, 1, 10):
            errores.append("Los créditos deben ser un número entero del 1 al 10.")
        return errores

    def a_diccionario(self):
        return {
            "id": self.id,
            "codigo": self.codigo,
            "nombre": self.nombre,
            "creditos": int(self.creditos),   # se guarda como número
        }

    @classmethod
    def desde_diccionario(cls, datos):
        return cls(datos["id"], datos["codigo"], datos["nombre"], datos["creditos"])

    def __str__(self):
        return f"[{self.id}] {self.codigo} - {self.nombre} ({self.creditos} créditos)"


# ---------------------------------------------------------------------
# PRUEBAS: se ejecutan solo si abres ESTE archivo y le das ▶ (Run).
# ---------------------------------------------------------------------
def probar():
    from shared.utilidades import mostrar_prueba
    print("\n=== PRUEBAS DEL MODELO Asignatura ===")

    buena = Asignatura(1, "mat101", "Matemática", "4")
    mostrar_prueba("Datos correctos no tienen errores", buena.validar() == [])
    mostrar_prueba("El código se guarda en mayúsculas", buena.codigo == "MAT101")

    letras = Asignatura(2, "FIS1", "Física", "cuatro")
    mostrar_prueba("Detecta créditos escritos con letras", len(letras.validar()) == 1)

    muchos = Asignatura(3, "QUI1", "Química", "50")
    mostrar_prueba("Detecta créditos fuera de rango (50)", len(muchos.validar()) == 1)

    todo_vacio = Asignatura(4, "", "", "")
    mostrar_prueba("Detecta los 3 campos vacíos", len(todo_vacio.validar()) == 3)

    copia = Asignatura.desde_diccionario(buena.a_diccionario())
    mostrar_prueba("Convertir a diccionario y volver no pierde datos",
                   copia.a_diccionario() == buena.a_diccionario())

    print("\nMensajes que vería el usuario si deja todo vacío:")
    for error in todo_vacio.validar():
        print("  -", error)


if __name__ == "__main__":
    probar()
