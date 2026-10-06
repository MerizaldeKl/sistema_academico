# =====================================================================
# PROCESO 3 · Modelo Docente (TAREA 1)
# Igual que Estudiante, pero con los datos de un docente.
# =====================================================================

# Permite ejecutar este archivo solo (botón ▶) para hacer sus pruebas
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from shared.validaciones import esta_vacio, es_email_valido

# TUPLA con los campos que el usuario escribe
CAMPOS_DOCENTE = ("nombre", "apellido", "email", "especialidad")


class Docente:

    def __init__(self, id_docente, nombre, apellido, email, especialidad):
        self.id = id_docente
        self.nombre = str(nombre).strip()
        self.apellido = str(apellido).strip()
        self.email = str(email).strip()
        self.especialidad = str(especialidad).strip()

    def nombre_completo(self):
        return f"{self.nombre} {self.apellido}"

    def validar(self):
        """Devuelve una LISTA de errores. Lista vacía = datos correctos."""
        errores = []
        if esta_vacio(self.nombre):
            errores.append("El nombre es obligatorio. Escríbalo, por favor.")
        if esta_vacio(self.apellido):
            errores.append("El apellido es obligatorio. Escríbalo, por favor.")
        if not es_email_valido(self.email):
            errores.append("El email no es válido. Ejemplo correcto: docente@correo.com")
        if esta_vacio(self.especialidad):
            errores.append("La especialidad es obligatoria. Ejemplo: Matemática")
        return errores

    def a_diccionario(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "apellido": self.apellido,
            "email": self.email,
            "especialidad": self.especialidad,
        }

    @classmethod
    def desde_diccionario(cls, datos):
        return cls(datos["id"], datos["nombre"], datos["apellido"],
                   datos["email"], datos["especialidad"])

    def __str__(self):
        return f"[{self.id}] {self.nombre_completo()} | {self.email} | {self.especialidad}"


# ---------------------------------------------------------------------
# PRUEBAS: se ejecutan solo si abres ESTE archivo y le das ▶ (Run).
# ---------------------------------------------------------------------
def probar():
    from shared.utilidades import mostrar_prueba
    print("\n=== PRUEBAS DEL MODELO Docente ===")

    bueno = Docente(1, "Daniel", "Vera", "dvera@unemi.edu.ec", "Software")
    mostrar_prueba("Datos correctos no tienen errores", bueno.validar() == [])

    sin_especialidad = Docente(2, "Rosa", "León", "rosa@correo.com", "   ")
    mostrar_prueba("Detecta especialidad vacía (solo espacios)",
                   len(sin_especialidad.validar()) == 1)

    mal_email = Docente(3, "Rosa", "León", "rosa@correo", "Física")
    mostrar_prueba("Detecta email sin punto en el dominio", len(mal_email.validar()) == 1)

    todo_vacio = Docente(4, "", "", "", "")
    mostrar_prueba("Detecta los 4 campos vacíos", len(todo_vacio.validar()) == 4)

    copia = Docente.desde_diccionario(bueno.a_diccionario())
    mostrar_prueba("Convertir a diccionario y volver no pierde datos",
                   copia.a_diccionario() == bueno.a_diccionario())

    print("\nMensajes que vería el usuario si deja todo vacío:")
    for error in todo_vacio.validar():
        print("  -", error)


if __name__ == "__main__":
    probar()
