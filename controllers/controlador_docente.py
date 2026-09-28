"""
PROCESO 4 · ControladorDocente (TAREA 1)
Mismas cinco operaciones que ControladorEstudiante, aplicadas a Docente.
Sin print() ni input(). Devuelve tuplas (exito, mensaje) o datos.
"""

from models.docente import Docente, CAMPOS_DOCENTE
from shared.archivo_json import ArchivoJSON
from shared.validaciones import es_email_valido, campos_faltantes, campos_no_validos
from shared.utilidades import (
    normalizar_datos, siguiente_id, valores_registrados,
    buscar_posicion, coincide_busqueda,
)


class ControladorDocente:
    CAMPOS = CAMPOS_DOCENTE
    CAMPOS_EDITABLES = CAMPOS_DOCENTE
    CAMPOS_OBLIGATORIOS = ("nombre", "apellido", "email", "especialidad")
    CAMPOS_BUSCABLES = ("nombre", "apellido", "email", "especialidad")

    def __init__(self, controlador_asignatura):
        self.archivo = ArchivoJSON("docentes.json")
        # Se recibe el controlador de asignaturas para comprobar que existan
        self.controlador_asignatura = controlador_asignatura

    # ==================== C · CREATE ====================
    def crear(self, datos):
        valores = normalizar_datos(datos, self.CAMPOS)

        faltantes = campos_faltantes(valores, self.CAMPOS_OBLIGATORIOS)
        if faltantes:
            return False, f"Faltan campos obligatorios: {', '.join(faltantes)}"

        if not es_email_valido(valores["email"]):
            return False, f"El email '{valores['email']}' no tiene un formato válido"

        registros = self.archivo.leer()
        if valores["email"].lower() in valores_registrados(registros, "email"):
            return False, "Ese email ya está registrado"

        docente = Docente(siguiente_id(registros), **valores)
        registros.append(docente.a_diccionario())
        if not self.archivo.guardar(registros):
            return False, "No se pudo escribir el archivo"
        return True, (f"Docente {docente.obtener_nombre_completo()} "
                      f"creado con id {docente.id}")

    # ==================== R · READ ====================
    def obtener_todos(self):
        return [Docente.desde_diccionario(r) for r in self.archivo.leer()]

    def obtener_por_id(self, id_docente):
        for docente in self.obtener_todos():
            if docente.id == id_docente:
                return docente
        return None

    # ==================== S · SEARCH ====================
    def buscar(self, termino):
        termino = str(termino).strip().lower()
        if not termino:
            return []
        return [
            Docente.desde_diccionario(r)
            for r in self.archivo.leer()
            if coincide_busqueda(r, termino, self.CAMPOS_BUSCABLES)
        ]

    # ==================== U · UPDATE ====================
    def actualizar(self, id_docente, cambios):
        cambios = {campo: str(valor).strip() for campo, valor in cambios.items()}

        desconocidos = campos_no_validos(cambios, self.CAMPOS_EDITABLES)
        if desconocidos:
            return False, f"Campos no válidos: {', '.join(sorted(desconocidos))}"
        if not cambios:
            return False, "No se indicó ningún cambio"
        vacios = campos_faltantes(cambios, [c for c in cambios
                                            if c in self.CAMPOS_OBLIGATORIOS])
        if vacios:
            return False, f"No se pueden dejar vacíos: {', '.join(vacios)}"

        registros = self.archivo.leer()
        posicion = buscar_posicion(registros, id_docente)
        if posicion is None:
            return False, f"No existe un docente con id {id_docente}"

        if "email" in cambios:
            if not es_email_valido(cambios["email"]):
                return False, "El email no tiene un formato válido"
            if cambios["email"].lower() in valores_registrados(
                    registros, "email", excepto_id=id_docente):
                return False, "Ese email ya lo usa otro docente"

        registros[posicion].update(cambios)
        if not self.archivo.guardar(registros):
            return False, "No se pudo escribir el archivo"
        return True, f"Docente {id_docente} actualizado ({len(cambios)} campo/s)"

    # ==================== D · DELETE ====================
    def eliminar(self, id_docente):
        registros = self.archivo.leer()
        quedan = [r for r in registros if r["id"] != id_docente]
        if len(quedan) == len(registros):
            return False, f"No existe un docente con id {id_docente}"
        if not self.archivo.guardar(quedan):
            return False, "No se pudo escribir el archivo"
        return True, f"Docente {id_docente} eliminado"

    # ==================== EXTRAS ====================
    def asignar_asignatura(self, id_docente, codigo):
        codigo = str(codigo).strip().upper()
        if self.controlador_asignatura.obtener_por_codigo(codigo) is None:
            return False, f"No existe una asignatura con código {codigo}"

        registros = self.archivo.leer()
        posicion = buscar_posicion(registros, id_docente)
        if posicion is None:
            return False, f"No existe un docente con id {id_docente}"

        docente = Docente.desde_diccionario(registros[posicion])
        if not docente.asignar_asignatura(codigo):
            return False, f"El docente ya tenía asignada {codigo}"
        registros[posicion] = docente.a_diccionario()
        if not self.archivo.guardar(registros):
            return False, "No se pudo escribir el archivo"
        return True, f"Asignatura {codigo} asignada a {docente.obtener_nombre_completo()}"

    def quitar_asignatura(self, id_docente, codigo):
        codigo = str(codigo).strip().upper()
        registros = self.archivo.leer()
        posicion = buscar_posicion(registros, id_docente)
        if posicion is None:
            return False, f"No existe un docente con id {id_docente}"

        docente = Docente.desde_diccionario(registros[posicion])
        if not docente.quitar_asignatura(codigo):
            return False, f"El docente no tenía asignada {codigo}"
        registros[posicion] = docente.a_diccionario()
        if not self.archivo.guardar(registros):
            return False, "No se pudo escribir el archivo"
        return True, f"Asignatura {codigo} retirada de {docente.obtener_nombre_completo()}"

    def quitar_asignatura_de_todos(self, codigo):
        """Se usa cuando se elimina una asignatura del sistema."""
        registros = self.archivo.leer()
        for registro in registros:
            registro["asignaturas"] = [c for c in registro.get("asignaturas", [])
                                       if c != codigo]
        self.archivo.guardar(registros)

    def docentes_por_especialidad(self):
        """DICCIONARIO DE LISTAS: {"Matemática": ["Ana Pérez", ...], ...}"""
        agrupados = {}
        for docente in self.obtener_todos():
            clave = docente.especialidad.strip().title()
            agrupados.setdefault(clave, []).append(docente.obtener_nombre_completo())
        return agrupados
