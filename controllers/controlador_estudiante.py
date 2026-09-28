"""
PROCESO 4 · ControladorEstudiante
Aquí viven las cinco operaciones (crear, leer, buscar, editar, eliminar).
Tres reglas que se cumplen en todo el archivo (igual que en la guía):
  - No hay ni un print() ni un input(): el Controlador no habla con el usuario.
  - Toda operación devuelve una TUPLA (exito, mensaje) o datos.
  - Las validaciones ocurren ANTES de tocar el archivo.
"""

from models.estudiante import Estudiante, CAMPOS_ESTUDIANTE
from shared.archivo_json import ArchivoJSON
from shared.validaciones import (
    es_email_valido, campos_faltantes, campos_no_validos, convertir_nota,
)
from shared.utilidades import (
    normalizar_datos, siguiente_id, valores_registrados,
    buscar_posicion, coincide_busqueda,
)


class ControladorEstudiante:
    # TUPLAS de configuración: fijas
    CAMPOS = CAMPOS_ESTUDIANTE                 # campos del formulario de creación
    CAMPOS_EDITABLES = CAMPOS_ESTUDIANTE       # campos que se pueden actualizar
    CAMPOS_OBLIGATORIOS = ("nombre", "apellido", "email", "carnet")
    CAMPOS_BUSCABLES = ("nombre", "apellido", "email", "carnet")

    def __init__(self):
        self.archivo = ArchivoJSON("estudiantes.json")

    # ==================== C · CREATE ====================
    def crear(self, datos):
        """datos: diccionario con las claves de CAMPOS. Devuelve (exito, mensaje)."""
        valores = normalizar_datos(datos, self.CAMPOS)

        faltantes = campos_faltantes(valores, self.CAMPOS_OBLIGATORIOS)
        if faltantes:
            return False, f"Faltan campos obligatorios: {', '.join(faltantes)}"

        if not es_email_valido(valores["email"]):
            return False, f"El email '{valores['email']}' no tiene un formato válido"

        registros = self.archivo.leer()
        # Duplicados: búsqueda instantánea dentro de un CONJUNTO
        if valores["email"].lower() in valores_registrados(registros, "email"):
            return False, "Ese email ya está registrado"
        if valores["carnet"].lower() in valores_registrados(registros, "carnet"):
            return False, "Ese carnet ya está registrado"

        # ** convierte el diccionario en argumentos con nombre
        estudiante = Estudiante(siguiente_id(registros), **valores)
        registros.append(estudiante.a_diccionario())      # agrego a la LISTA
        if not self.archivo.guardar(registros):
            return False, "No se pudo escribir el archivo"
        return True, (f"Estudiante {estudiante.obtener_nombre_completo()} "
                      f"creado con id {estudiante.id}")

    # ==================== R · READ ====================
    def obtener_todos(self):
        """LISTA de objetos Estudiante."""
        return [Estudiante.desde_diccionario(r) for r in self.archivo.leer()]

    def obtener_por_id(self, id_estudiante):
        for estudiante in self.obtener_todos():
            if estudiante.id == id_estudiante:
                return estudiante
        return None

    # ==================== S · SEARCH ====================
    def buscar(self, termino):
        """Búsqueda lineal en los campos de CAMPOS_BUSCABLES."""
        termino = str(termino).strip().lower()
        if not termino:
            return []
        return [
            Estudiante.desde_diccionario(r)
            for r in self.archivo.leer()
            if coincide_busqueda(r, termino, self.CAMPOS_BUSCABLES)
        ]

    # ==================== U · UPDATE ====================
    def actualizar(self, id_estudiante, cambios):
        """cambios: diccionario solo con los campos que se quieren modificar."""
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
        posicion = buscar_posicion(registros, id_estudiante)
        if posicion is None:
            return False, f"No existe un estudiante con id {id_estudiante}"

        if "email" in cambios:
            if not es_email_valido(cambios["email"]):
                return False, "El email no tiene un formato válido"
            if cambios["email"].lower() in valores_registrados(
                    registros, "email", excepto_id=id_estudiante):
                return False, "Ese email ya lo usa otro estudiante"
        if "carnet" in cambios:
            if cambios["carnet"].lower() in valores_registrados(
                    registros, "carnet", excepto_id=id_estudiante):
                return False, "Ese carnet ya lo usa otro estudiante"

        registros[posicion].update(cambios)     # actualizo el diccionario
        if not self.archivo.guardar(registros):
            return False, "No se pudo escribir el archivo"
        return True, f"Estudiante {id_estudiante} actualizado ({len(cambios)} campo/s)"

    # ==================== D · DELETE ====================
    def eliminar(self, id_estudiante):
        registros = self.archivo.leer()
        # LISTA NUEVA sin ese registro: nunca borro mientras recorro
        quedan = [r for r in registros if r["id"] != id_estudiante]
        if len(quedan) == len(registros):
            return False, f"No existe un estudiante con id {id_estudiante}"
        if not self.archivo.guardar(quedan):
            return False, "No se pudo escribir el archivo"
        return True, f"Estudiante {id_estudiante} eliminado"

    # ==================== EXTRAS de la guía ====================
    def agregar_nota(self, id_estudiante, materia, nota):
        """La nota debe ser un número entre 0 y 20."""
        materia = str(materia).strip()
        if not materia:
            return False, "La materia es obligatoria"
        valor = convertir_nota(nota)
        if valor is None:
            return False, "La nota debe ser un número entre 0 y 20"

        registros = self.archivo.leer()
        posicion = buscar_posicion(registros, id_estudiante)
        if posicion is None:
            return False, f"No existe un estudiante con id {id_estudiante}"

        estudiante = Estudiante.desde_diccionario(registros[posicion])
        estudiante.agregar_nota(materia, valor)
        registros[posicion] = estudiante.a_diccionario()
        if not self.archivo.guardar(registros):
            return False, "No se pudo escribir el archivo"
        return True, f"Nota {valor} agregada en {materia}"

    def materias_ofertadas(self):
        """CONJUNTO con todas las materias inscritas por todos, sin repetir."""
        todas = set()
        for estudiante in self.obtener_todos():
            todas = todas | estudiante.materias        # UNIÓN de conjuntos
        return todas

    def estudiantes_en_comun(self, id_a, id_b):
        """Devuelve (exito, conjunto_de_materias) o (False, mensaje)."""
        estudiante_a = self.obtener_por_id(id_a)
        estudiante_b = self.obtener_por_id(id_b)
        if estudiante_a is None or estudiante_b is None:
            return False, "Uno de los dos estudiantes no existe"
        return True, estudiante_a.materias_en_comun(estudiante_b)
