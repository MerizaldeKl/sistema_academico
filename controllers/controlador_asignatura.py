"""
PROCESO 4 · ControladorAsignatura (TAREA 2)
El código de la asignatura funciona como identificador: es único y no se
puede editar (así no se rompen los docentes y cursos que lo usan).
"""

from models.asignatura import Asignatura, CAMPOS_ASIGNATURA
from shared.archivo_json import ArchivoJSON
from shared.validaciones import campos_faltantes, campos_no_validos, convertir_creditos
from shared.utilidades import (
    normalizar_datos, siguiente_id, valores_registrados,
    buscar_posicion, coincide_busqueda,
)


class ControladorAsignatura:
    CAMPOS = CAMPOS_ASIGNATURA
    CAMPOS_EDITABLES = ("nombre", "creditos")      # el código NO se edita
    CAMPOS_OBLIGATORIOS = ("codigo", "nombre", "creditos")
    CAMPOS_BUSCABLES = ("codigo", "nombre")

    def __init__(self):
        self.archivo = ArchivoJSON("asignaturas.json")

    # ==================== C · CREATE ====================
    def crear(self, datos):
        valores = normalizar_datos(datos, self.CAMPOS)
        valores["codigo"] = valores["codigo"].upper()

        faltantes = campos_faltantes(valores, self.CAMPOS_OBLIGATORIOS)
        if faltantes:
            return False, f"Faltan campos obligatorios: {', '.join(faltantes)}"

        creditos = convertir_creditos(valores["creditos"])
        if creditos is None:
            return False, "Los créditos deben ser un número entero entre 1 y 10"
        valores["creditos"] = creditos

        registros = self.archivo.leer()
        if valores["codigo"].lower() in valores_registrados(registros, "codigo"):
            return False, f"Ya existe una asignatura con código {valores['codigo']}"

        asignatura = Asignatura(siguiente_id(registros), **valores)
        registros.append(asignatura.a_diccionario())
        if not self.archivo.guardar(registros):
            return False, "No se pudo escribir el archivo"
        return True, f"Asignatura {asignatura.nombre} creada con id {asignatura.id}"

    # ==================== R · READ ====================
    def obtener_todos(self):
        return [Asignatura.desde_diccionario(r) for r in self.archivo.leer()]

    def obtener_por_id(self, id_asignatura):
        for asignatura in self.obtener_todos():
            if asignatura.id == id_asignatura:
                return asignatura
        return None

    def obtener_por_codigo(self, codigo):
        codigo = str(codigo).strip().upper()
        # DICCIONARIO índice {codigo: asignatura}: acceso directo por clave
        indice = {a.codigo: a for a in self.obtener_todos()}
        return indice.get(codigo)

    # ==================== S · SEARCH ====================
    def buscar(self, termino):
        termino = str(termino).strip().lower()
        if not termino:
            return []
        return [
            Asignatura.desde_diccionario(r)
            for r in self.archivo.leer()
            if coincide_busqueda(r, termino, self.CAMPOS_BUSCABLES)
        ]

    # ==================== U · UPDATE ====================
    def actualizar(self, id_asignatura, cambios):
        cambios = {campo: str(valor).strip() for campo, valor in cambios.items()}

        desconocidos = campos_no_validos(cambios, self.CAMPOS_EDITABLES)
        if desconocidos:
            return False, f"Campos no válidos: {', '.join(sorted(desconocidos))}"
        if not cambios:
            return False, "No se indicó ningún cambio"
        vacios = campos_faltantes(cambios, list(cambios))
        if vacios:
            return False, f"No se pueden dejar vacíos: {', '.join(vacios)}"

        if "creditos" in cambios:
            creditos = convertir_creditos(cambios["creditos"])
            if creditos is None:
                return False, "Los créditos deben ser un número entero entre 1 y 10"
            cambios["creditos"] = creditos

        registros = self.archivo.leer()
        posicion = buscar_posicion(registros, id_asignatura)
        if posicion is None:
            return False, f"No existe una asignatura con id {id_asignatura}"

        registros[posicion].update(cambios)
        if not self.archivo.guardar(registros):
            return False, "No se pudo escribir el archivo"
        return True, f"Asignatura {id_asignatura} actualizada ({len(cambios)} campo/s)"

    # ==================== D · DELETE ====================
    def eliminar(self, id_asignatura):
        registros = self.archivo.leer()
        quedan = [r for r in registros if r["id"] != id_asignatura]
        if len(quedan) == len(registros):
            return False, f"No existe una asignatura con id {id_asignatura}"
        if not self.archivo.guardar(quedan):
            return False, "No se pudo escribir el archivo"
        return True, f"Asignatura {id_asignatura} eliminada"
