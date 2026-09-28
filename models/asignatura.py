"""
PROCESO 3 · Modelo Asignatura (TAREA 2)
"""

# TUPLA de campos que el usuario escribe al crear una asignatura.
CAMPOS_ASIGNATURA = ("codigo", "nombre", "creditos")


class Asignatura:
    """MODELO: representa una asignatura (materia)."""

    def __init__(self, id_asignatura, codigo, nombre, creditos):
        self.id = id_asignatura
        self.codigo = codigo          # ej: MAT101 (único, se guarda en mayúsculas)
        self.nombre = nombre
        self.creditos = creditos      # número entero

    def a_diccionario(self):
        return {
            "id": self.id,
            "codigo": self.codigo,
            "nombre": self.nombre,
            "creditos": self.creditos,
        }

    @classmethod
    def desde_diccionario(cls, datos):
        return cls(datos["id"], datos["codigo"], datos["nombre"],
                   datos.get("creditos", 0))

    def __str__(self):
        return f"[{self.codigo}] {self.nombre} ({self.creditos} créditos)"
