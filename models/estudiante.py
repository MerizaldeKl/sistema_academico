# =====================================================================
# PROCESO 3 · Modelo Estudiante
# Un MODELO dice QUÉ ES un dato: qué atributos tiene y cómo se
# convierte a diccionario para guardarlo en JSON.
# No pide datos al usuario ni imprime (excepto en sus pruebas).
# =====================================================================

# Estas 3 líneas permiten ejecutar este archivo solo (botón ▶) para
# hacer sus pruebas: le dicen a Python dónde está la carpeta del proyecto.
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from shared.validaciones import esta_vacio, es_email_valido

# TUPLA con los campos que el usuario escribe. Es tupla porque no cambia.
CAMPOS_ESTUDIANTE = ("nombre", "apellido", "email", "carnet")


class Estudiante:

    # Constructor: se ejecuta al crear un estudiante nuevo
    def __init__(self, id_estudiante, nombre, apellido, email, carnet):
        self.id = id_estudiante
        self.nombre = str(nombre).strip()      # strip() quita espacios sobrantes
        self.apellido = str(apellido).strip()
        self.email = str(email).strip()
        self.carnet = str(carnet).strip()

    def nombre_completo(self):
        return f"{self.nombre} {self.apellido}"

    def validar(self):
        """Revisa los datos y devuelve una LISTA de errores.
        Si la lista está vacía, los datos están bien."""
        errores = []
        if esta_vacio(self.nombre):
            errores.append("El nombre es obligatorio. Escríbalo, por favor.")
        if esta_vacio(self.apellido):
            errores.append("El apellido es obligatorio. Escríbalo, por favor.")
        if not es_email_valido(self.email):
            errores.append("El email no es válido. Ejemplo correcto: ana@correo.com")
        if esta_vacio(self.carnet):
            errores.append("El carnet es obligatorio. Ejemplo: EST001")
        return errores

    def a_diccionario(self):
        """Objeto -> DICCIONARIO (para guardarlo en JSON)."""
        return {
            "id": self.id,
            "nombre": self.nombre,
            "apellido": self.apellido,
            "email": self.email,
            "carnet": self.carnet,
        }

    @classmethod
    def desde_diccionario(cls, datos):
        """DICCIONARIO -> objeto (al leerlo del JSON).
        Se usa así: Estudiante.desde_diccionario({...})"""
        return cls(datos["id"], datos["nombre"], datos["apellido"],
                   datos["email"], datos["carnet"])

    def __str__(self):
        # Esto es lo que se ve al hacer print(estudiante)
        return f"[{self.id}] {self.nombre_completo()} | {self.email} | Carnet: {self.carnet}"


# ---------------------------------------------------------------------
# PRUEBAS: se ejecutan solo si abres ESTE archivo y le das ▶ (Run).
# Prueban los errores que podría cometer un usuario.
# ---------------------------------------------------------------------
def probar():
    from shared.utilidades import mostrar_prueba
    print("\n=== PRUEBAS DEL MODELO Estudiante ===")

    bueno = Estudiante(1, "  Ana ", "Pérez", "ana@correo.com", "EST001")
    mostrar_prueba("Datos correctos no tienen errores", bueno.validar() == [])
    mostrar_prueba("Quita los espacios sobrantes del nombre", bueno.nombre == "Ana")

    sin_nombre = Estudiante(2, "", "Pérez", "ana@correo.com", "EST002")
    mostrar_prueba("Detecta nombre vacío", len(sin_nombre.validar()) == 1)

    mal_email = Estudiante(3, "Luis", "García", "luis.correo", "EST003")
    mostrar_prueba("Detecta email mal escrito", len(mal_email.validar()) == 1)

    todo_vacio = Estudiante(4, "", "", "", "")
    mostrar_prueba("Detecta los 4 campos vacíos", len(todo_vacio.validar()) == 4)

    copia = Estudiante.desde_diccionario(bueno.a_diccionario())
    mostrar_prueba("Convertir a diccionario y volver no pierde datos",
                   copia.a_diccionario() == bueno.a_diccionario())

    # Muestra cómo vería el usuario los mensajes de error
    print("\nMensajes que vería el usuario si deja todo vacío:")
    for error in todo_vacio.validar():
        print("  -", error)


if __name__ == "__main__":
    probar()
