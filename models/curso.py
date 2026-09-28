"""
PROCESO 3 · Modelo Curso (TAREA 3)
Un curso conecta a los demás modelos: tiene un docente, varias asignaturas
y varios estudiantes. Guarda solo sus identificadores, no los objetos completos.
"""

# TUPLA de campos que el usuario escribe al crear un curso.
CAMPOS_CURSO = ("nombre", "periodo")


class Curso:
    """MODELO: representa un curso (ej: "Primer semestre A", periodo "2026-2")."""

    def __init__(self, id_curso, nombre, periodo, id_docente=None,
                 asignaturas=None, estudiantes=None):
        self.id = id_curso
        self.nombre = nombre
        self.periodo = periodo
        self.id_docente = id_docente                  # None = sin docente
        # CONJUNTOS: códigos de asignaturas e ids de estudiantes, sin repetir
        self.asignaturas = set(asignaturas) if asignaturas else set()
        self.estudiantes = set(estudiantes) if estudiantes else set()

    def asignar_docente(self, id_docente):
        self.id_docente = id_docente

    def agregar_asignatura(self, codigo):
        if codigo in self.asignaturas:
            return False
        self.asignaturas.add(codigo)
        return True

    def inscribir_estudiante(self, id_estudiante):
        if id_estudiante in self.estudiantes:
            return False
        self.estudiantes.add(id_estudiante)
        return True

    def retirar_estudiante(self, id_estudiante):
        if id_estudiante not in self.estudiantes:
            return False
        self.estudiantes.discard(id_estudiante)
        return True

    def a_diccionario(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "periodo": self.periodo,
            "id_docente": self.id_docente,
            "asignaturas": sorted(self.asignaturas),   # set -> lista para JSON
            "estudiantes": sorted(self.estudiantes),
        }

    @classmethod
    def desde_diccionario(cls, datos):
        return cls(
            datos["id"], datos["nombre"], datos["periodo"],
            id_docente=datos.get("id_docente"),
            asignaturas=set(datos.get("asignaturas", [])),   # lista -> set
            estudiantes=set(datos.get("estudiantes", [])),
        )

    def __str__(self):
        return (f"[{self.id}] {self.nombre} ({self.periodo}) - "
                f"{len(self.estudiantes)} estudiante(s)")
