"""
PROCESO 4 · ControladorCurso (TAREA 3)
Es el controlador que CONECTA el sistema: para asignar un docente, una
asignatura o un estudiante, primero pregunta a los otros controladores si existen.
"""

from models.curso import Curso, CAMPOS_CURSO
from shared.archivo_json import ArchivoJSON
from shared.validaciones import campos_faltantes, campos_no_validos
from shared.utilidades import (
    normalizar_datos, siguiente_id, buscar_posicion, coincide_busqueda,
)


class ControladorCurso:
    CAMPOS = CAMPOS_CURSO
    CAMPOS_EDITABLES = CAMPOS_CURSO
    CAMPOS_OBLIGATORIOS = ("nombre", "periodo")
    CAMPOS_BUSCABLES = ("nombre", "periodo")

    def __init__(self, controlador_docente, controlador_asignatura,
                 controlador_estudiante):
        self.archivo = ArchivoJSON("cursos.json")
        self.controlador_docente = controlador_docente
        self.controlador_asignatura = controlador_asignatura
        self.controlador_estudiante = controlador_estudiante

    # ==================== AYUDAS INTERNAS ====================
    def _claves_registradas(self, registros, excepto_id=None):
        """CONJUNTO de TUPLAS (nombre, periodo): no puede haber dos cursos
        con el mismo nombre en el mismo periodo. Una tupla sí puede ir en un set."""
        return {
            (r["nombre"].strip().lower(), r["periodo"].strip().lower())
            for r in registros
            if r["id"] != excepto_id
        }

    def _cargar(self, registros, id_curso):
        """Devuelve (posicion, objeto Curso) o (None, None)."""
        posicion = buscar_posicion(registros, id_curso)
        if posicion is None:
            return None, None
        return posicion, Curso.desde_diccionario(registros[posicion])

    def _guardar_curso(self, registros, posicion, curso):
        registros[posicion] = curso.a_diccionario()
        return self.archivo.guardar(registros)

    # ==================== C · CREATE ====================
    def crear(self, datos):
        valores = normalizar_datos(datos, self.CAMPOS)

        faltantes = campos_faltantes(valores, self.CAMPOS_OBLIGATORIOS)
        if faltantes:
            return False, f"Faltan campos obligatorios: {', '.join(faltantes)}"

        registros = self.archivo.leer()
        clave = (valores["nombre"].lower(), valores["periodo"].lower())
        if clave in self._claves_registradas(registros):
            return False, "Ya existe un curso con ese nombre en ese periodo"

        curso = Curso(siguiente_id(registros), **valores)
        registros.append(curso.a_diccionario())
        if not self.archivo.guardar(registros):
            return False, "No se pudo escribir el archivo"
        return True, f"Curso {curso.nombre} ({curso.periodo}) creado con id {curso.id}"

    # ==================== R · READ ====================
    def obtener_todos(self):
        return [Curso.desde_diccionario(r) for r in self.archivo.leer()]

    def obtener_por_id(self, id_curso):
        for curso in self.obtener_todos():
            if curso.id == id_curso:
                return curso
        return None

    def detalle(self, id_curso):
        """DICCIONARIO con los NOMBRES de docente, asignaturas y estudiantes."""
        curso = self.obtener_por_id(id_curso)
        if curso is None:
            return None

        docente = None
        if curso.id_docente is not None:
            docente = self.controlador_docente.obtener_por_id(curso.id_docente)

        asignaturas = []
        for codigo in sorted(curso.asignaturas):
            asignatura = self.controlador_asignatura.obtener_por_codigo(codigo)
            if asignatura:
                asignaturas.append(f"{codigo} - {asignatura.nombre}")

        estudiantes = []
        for id_estudiante in sorted(curso.estudiantes):
            estudiante = self.controlador_estudiante.obtener_por_id(id_estudiante)
            if estudiante:
                estudiantes.append(
                    f"{estudiante.carnet} - {estudiante.obtener_nombre_completo()}")

        return {
            "id": curso.id,
            "nombre": curso.nombre,
            "periodo": curso.periodo,
            "docente": docente.obtener_nombre_completo() if docente else "Sin asignar",
            "asignaturas": asignaturas,
            "estudiantes": estudiantes,
        }

    # ==================== S · SEARCH ====================
    def buscar(self, termino):
        termino = str(termino).strip().lower()
        if not termino:
            return []
        return [
            Curso.desde_diccionario(r)
            for r in self.archivo.leer()
            if coincide_busqueda(r, termino, self.CAMPOS_BUSCABLES)
        ]

    # ==================== U · UPDATE ====================
    def actualizar(self, id_curso, cambios):
        cambios = {campo: str(valor).strip() for campo, valor in cambios.items()}

        desconocidos = campos_no_validos(cambios, self.CAMPOS_EDITABLES)
        if desconocidos:
            return False, f"Campos no válidos: {', '.join(sorted(desconocidos))}"
        if not cambios:
            return False, "No se indicó ningún cambio"
        vacios = campos_faltantes(cambios, list(cambios))
        if vacios:
            return False, f"No se pueden dejar vacíos: {', '.join(vacios)}"

        registros = self.archivo.leer()
        posicion = buscar_posicion(registros, id_curso)
        if posicion is None:
            return False, f"No existe un curso con id {id_curso}"

        actual = registros[posicion]
        clave = (cambios.get("nombre", actual["nombre"]).lower(),
                 cambios.get("periodo", actual["periodo"]).lower())
        if clave in self._claves_registradas(registros, excepto_id=id_curso):
            return False, "Ya existe un curso con ese nombre en ese periodo"

        registros[posicion].update(cambios)
        if not self.archivo.guardar(registros):
            return False, "No se pudo escribir el archivo"
        return True, f"Curso {id_curso} actualizado ({len(cambios)} campo/s)"

    # ==================== D · DELETE ====================
    def eliminar(self, id_curso):
        registros = self.archivo.leer()
        quedan = [r for r in registros if r["id"] != id_curso]
        if len(quedan) == len(registros):
            return False, f"No existe un curso con id {id_curso}"
        if not self.archivo.guardar(quedan):
            return False, "No se pudo escribir el archivo"
        return True, f"Curso {id_curso} eliminado"

    # ==================== CONEXIONES ====================
    def asignar_docente(self, id_curso, id_docente):
        docente = self.controlador_docente.obtener_por_id(id_docente)
        if docente is None:
            return False, f"No existe un docente con id {id_docente}"

        registros = self.archivo.leer()
        posicion, curso = self._cargar(registros, id_curso)
        if curso is None:
            return False, f"No existe un curso con id {id_curso}"

        curso.asignar_docente(id_docente)
        if not self._guardar_curso(registros, posicion, curso):
            return False, "No se pudo escribir el archivo"
        return True, f"{docente.obtener_nombre_completo()} asignado al curso {curso.nombre}"

    def agregar_asignatura(self, id_curso, codigo):
        codigo = str(codigo).strip().upper()
        if self.controlador_asignatura.obtener_por_codigo(codigo) is None:
            return False, f"No existe una asignatura con código {codigo}"

        registros = self.archivo.leer()
        posicion, curso = self._cargar(registros, id_curso)
        if curso is None:
            return False, f"No existe un curso con id {id_curso}"

        if not curso.agregar_asignatura(codigo):
            return False, f"El curso ya tenía la asignatura {codigo}"
        if not self._guardar_curso(registros, posicion, curso):
            return False, "No se pudo escribir el archivo"
        return True, f"Asignatura {codigo} agregada al curso {curso.nombre}"

    def inscribir_estudiante(self, id_curso, id_estudiante):
        estudiante = self.controlador_estudiante.obtener_por_id(id_estudiante)
        if estudiante is None:
            return False, f"No existe un estudiante con id {id_estudiante}"

        registros = self.archivo.leer()
        posicion, curso = self._cargar(registros, id_curso)
        if curso is None:
            return False, f"No existe un curso con id {id_curso}"

        if not curso.inscribir_estudiante(id_estudiante):
            return False, "El estudiante ya estaba inscrito en este curso"
        if not self._guardar_curso(registros, posicion, curso):
            return False, "No se pudo escribir el archivo"
        return True, (f"{estudiante.obtener_nombre_completo()} inscrito en "
                      f"el curso {curso.nombre}")

    def retirar_estudiante(self, id_curso, id_estudiante):
        registros = self.archivo.leer()
        posicion, curso = self._cargar(registros, id_curso)
        if curso is None:
            return False, f"No existe un curso con id {id_curso}"

        if not curso.retirar_estudiante(id_estudiante):
            return False, "Ese estudiante no está inscrito en este curso"
        if not self._guardar_curso(registros, posicion, curso):
            return False, "No se pudo escribir el archivo"
        return True, f"Estudiante {id_estudiante} retirado del curso {curso.nombre}"

    def quitar_referencias(self, tipo, valor):
        """Limpia los cursos cuando se elimina un docente, asignatura o estudiante.
        tipo: "docente", "asignatura" o "estudiante"."""
        registros = self.archivo.leer()
        for registro in registros:
            if tipo == "docente" and registro.get("id_docente") == valor:
                registro["id_docente"] = None
            elif tipo == "asignatura":
                registro["asignaturas"] = [c for c in registro.get("asignaturas", [])
                                           if c != valor]
            elif tipo == "estudiante":
                registro["estudiantes"] = [e for e in registro.get("estudiantes", [])
                                           if e != valor]
        self.archivo.guardar(registros)
