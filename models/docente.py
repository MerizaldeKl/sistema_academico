"""
PROCESO 3 · Modelo Docente (TAREA 1)
Misma estructura que Estudiante: atributos, a_diccionario(), desde_diccionario().
"""

# TUPLA de campos que el usuario escribe.
CAMPOS_DOCENTE = ("nombre", "apellido", "email", "telefono", "especialidad")


class Docente:
    """MODELO: representa a un docente."""

    def __init__(self, id_docente, nombre, apellido, email, telefono,
                 especialidad, asignaturas=None):
        self.id = id_docente
        self.nombre = nombre
        self.apellido = apellido
        self.email = email
        self.telefono = telefono
        self.especialidad = especialidad
        # CONJUNTO con los códigos de las asignaturas que dicta (sin repetir)
        self.asignaturas = set(asignaturas) if asignaturas else set()

    def obtener_nombre_completo(self):
        return f"{self.nombre} {self.apellido}"

    def asignar_asignatura(self, codigo):
        """Devuelve False si ya la tenía asignada."""
        if codigo in self.asignaturas:        # búsqueda instantánea en el set
            return False
        self.asignaturas.add(codigo)
        return True

    def quitar_asignatura(self, codigo):
        """Devuelve False si no la tenía asignada."""
        if codigo not in self.asignaturas:
            return False
        self.asignaturas.discard(codigo)
        return True

    def a_diccionario(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "apellido": self.apellido,
            "email": self.email,
            "telefono": self.telefono,
            "especialidad": self.especialidad,
            "asignaturas": sorted(self.asignaturas),   # set -> lista para JSON
        }

    @classmethod
    def desde_diccionario(cls, datos):
        return cls(
            datos["id"], datos["nombre"], datos["apellido"], datos["email"],
            datos.get("telefono", ""),
            datos.get("especialidad", ""),
            asignaturas=set(datos.get("asignaturas", [])),  # lista -> set
        )

    def __str__(self):
        return (f"[{self.id}] {self.obtener_nombre_completo()} - "
                f"{self.especialidad} - {self.email}")
