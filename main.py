"""
PROCESO 6 · Integración: clase SistemaAcademico y menú principal.

SistemaAcademico conecta todo:
  - crea los cuatro controladores (lógica),
  - crea la InterfazConsola (vista),
  - y en cada opción del menú pide datos a la vista y se los pasa al controlador.
No usa print() ni input() directamente: todo lo muestra a través de la interfaz.

Ejecutar con:  python main.py
"""

from controllers.controlador_estudiante import ControladorEstudiante
from controllers.controlador_docente import ControladorDocente
from controllers.controlador_asignatura import ControladorAsignatura
from controllers.controlador_curso import ControladorCurso
from views.interfaz_consola import InterfazConsola


class SistemaAcademico:

    # TUPLAS de columnas para las tablas: (atributo, título, ancho)
    COLUMNAS_ESTUDIANTE = (("id", "ID", 5), ("carnet", "CARNET", 13),
                           ("nombre", "NOMBRE", 15), ("apellido", "APELLIDO", 15),
                           ("email", "EMAIL", 28))
    COLUMNAS_DOCENTE = (("id", "ID", 5), ("nombre", "NOMBRE", 15),
                        ("apellido", "APELLIDO", 15), ("email", "EMAIL", 26),
                        ("especialidad", "ESPECIALIDAD", 18))
    COLUMNAS_ASIGNATURA = (("id", "ID", 5), ("codigo", "CÓDIGO", 10),
                           ("nombre", "NOMBRE", 30), ("creditos", "CRÉDITOS", 10))
    COLUMNAS_CURSO = (("id", "ID", 5), ("nombre", "NOMBRE", 25),
                      ("periodo", "PERIODO", 12), ("id_docente", "ID DOCENTE", 12))

    def __init__(self):
        self.interfaz = InterfazConsola()
        # El orden importa: docentes y cursos necesitan a los otros controladores
        self.estudiantes = ControladorEstudiante()
        self.asignaturas = ControladorAsignatura()
        self.docentes = ControladorDocente(self.asignaturas)
        self.cursos = ControladorCurso(self.docentes, self.asignaturas, self.estudiantes)

    # =====================================================================
    # MENÚ PRINCIPAL
    # =====================================================================
    def iniciar(self):
        # DICCIONARIO de opciones: tecla -> (texto del menú, función)
        opciones = {
            "1": ("Gestión de Estudiantes", self.menu_estudiantes),
            "2": ("Gestión de Docentes", self.menu_docentes),
            "3": ("Gestión de Asignaturas", self.menu_asignaturas),
            "4": ("Gestión de Cursos", self.menu_cursos),
            "5": ("Resumen del sistema", self.resumen),
            "0": ("Salir", None),
        }
        while True:
            tecla = self.interfaz.mostrar_menu("SISTEMA ACADÉMICO", opciones)
            if tecla == "0":
                self.interfaz.info("¡Hasta luego!")
                break
            if tecla not in opciones:                 # búsqueda instantánea por clave
                self.interfaz.error("Opción no válida")
                self.interfaz.pausa()
                continue
            _texto, funcion = opciones[tecla]
            funcion()

    def ejecutar_submenu(self, titulo, opciones):
        """Repite el submenú hasta que el usuario elija 0 (Volver)."""
        while True:
            tecla = self.interfaz.mostrar_menu(titulo, opciones)
            if tecla == "0":
                return
            if tecla not in opciones:
                self.interfaz.error("Opción no válida")
                self.interfaz.pausa()
                continue
            _texto, funcion = opciones[tecla]
            funcion()

    # =====================================================================
    # OPERACIONES CRUD GENÉRICAS
    # Sirven para los cuatro controladores porque todos tienen los mismos
    # métodos: crear, obtener_todos, obtener_por_id, buscar, actualizar, eliminar.
    # =====================================================================
    def crear(self, controlador, titulo):
        self.interfaz.titulo(titulo)
        datos = self.interfaz.pedir_formulario(controlador.CAMPOS)
        exito, mensaje = controlador.crear(datos)       # desempaqueto la TUPLA
        self.interfaz.mostrar_resultado(exito, mensaje)
        self.interfaz.pausa()

    def ver_todos(self, controlador, titulo, columnas):
        self.interfaz.titulo(titulo)
        registros = controlador.obtener_todos()
        if not registros:
            self.interfaz.info("Todavía no hay registros. Use la opción 1 para crear el primero.")
        else:
            self.interfaz.mostrar_tabla(registros, columnas)
        self.interfaz.pausa()

    def buscar(self, controlador, titulo, columnas):
        self.interfaz.titulo(titulo)
        termino = self.interfaz.pedir_texto("Texto a buscar")
        encontrados = controlador.buscar(termino)
        if not encontrados:
            self.interfaz.info(f"Ningún registro coincide con '{termino}'.")
        else:
            self.interfaz.mostrar_tabla(encontrados, columnas)
        self.interfaz.pausa()

    def ver_por_id(self, controlador, titulo):
        self.interfaz.titulo(titulo)
        id_registro = self.interfaz.pedir_entero("Id")
        if id_registro is None:
            return self.interfaz.pausa()
        objeto = controlador.obtener_por_id(id_registro)
        if objeto is None:
            self.interfaz.error(f"No existe un registro con id {id_registro}")
        else:
            self.interfaz.mostrar_detalle(objeto.a_diccionario())
        self.interfaz.pausa()

    def actualizar(self, controlador, titulo):
        self.interfaz.titulo(titulo)
        id_registro = self.interfaz.pedir_entero("Id")
        if id_registro is None:
            return self.interfaz.pausa()
        objeto = controlador.obtener_por_id(id_registro)
        if objeto is None:
            self.interfaz.error(f"No existe un registro con id {id_registro}")
            return self.interfaz.pausa()

        self.interfaz.info(f"Editando: {objeto}")
        cambios = self.interfaz.pedir_cambios(controlador.CAMPOS_EDITABLES, objeto)
        exito, mensaje = controlador.actualizar(id_registro, cambios)
        self.interfaz.mostrar_resultado(exito, mensaje)
        self.interfaz.pausa()

    def eliminar(self, controlador, titulo, al_eliminar=None):
        """al_eliminar: función opcional para limpiar referencias en otros archivos."""
        self.interfaz.titulo(titulo)
        id_registro = self.interfaz.pedir_entero("Id")
        if id_registro is None:
            return self.interfaz.pausa()
        objeto = controlador.obtener_por_id(id_registro)
        if objeto is None:
            self.interfaz.error(f"No existe un registro con id {id_registro}")
            return self.interfaz.pausa()

        self.interfaz.info(f"Se eliminará: {objeto}")
        if self.interfaz.confirmar("¿Confirma la eliminación?"):
            exito, mensaje = controlador.eliminar(id_registro)
            if exito and al_eliminar:
                al_eliminar(objeto)
            self.interfaz.mostrar_resultado(exito, mensaje)
        else:
            self.interfaz.info("Operación cancelada")
        self.interfaz.pausa()

    # =====================================================================
    # SUBMENÚ ESTUDIANTES
    # "lambda: ..." es una función de una sola línea: guarda la acción
    # para ejecutarla recién cuando el usuario elija esa opción.
    # =====================================================================
    def menu_estudiantes(self):
        c, col = self.estudiantes, self.COLUMNAS_ESTUDIANTE
        opciones = {
            "1": ("Crear estudiante", lambda: self.crear(c, "CREAR ESTUDIANTE")),
            "2": ("Ver todos", lambda: self.ver_todos(c, "LISTA DE ESTUDIANTES", col)),
            "3": ("Buscar", lambda: self.buscar(c, "BUSCAR ESTUDIANTE", col)),
            "4": ("Ver por id", lambda: self.ver_por_id(c, "VER ESTUDIANTE")),
            "5": ("Actualizar", lambda: self.actualizar(c, "ACTUALIZAR ESTUDIANTE")),
            "6": ("Eliminar", lambda: self.eliminar(
                c, "ELIMINAR ESTUDIANTE",
                lambda e: self.cursos.quitar_referencias("estudiante", e.id))),
            "7": ("Agregar nota", self.agregar_nota),
            "8": ("Ver promedio", self.ver_promedio),
            "9": ("Materias en común", self.materias_en_comun),
            "10": ("Materias ofertadas", self.materias_ofertadas),
            "0": ("Volver al menú principal", None),
        }
        self.ejecutar_submenu("GESTIÓN DE ESTUDIANTES", opciones)

    def agregar_nota(self):
        self.interfaz.titulo("AGREGAR NOTA")
        id_estudiante = self.interfaz.pedir_entero("Id del estudiante")
        if id_estudiante is None:
            return self.interfaz.pausa()
        materia = self.interfaz.pedir_texto("Materia")
        nota = self.interfaz.pedir_texto("Nota (0 a 20)")
        exito, mensaje = self.estudiantes.agregar_nota(id_estudiante, materia, nota)
        self.interfaz.mostrar_resultado(exito, mensaje)
        self.interfaz.pausa()

    def ver_promedio(self):
        self.interfaz.titulo("PROMEDIO DEL ESTUDIANTE")
        id_estudiante = self.interfaz.pedir_entero("Id del estudiante")
        if id_estudiante is None:
            return self.interfaz.pausa()
        estudiante = self.estudiantes.obtener_por_id(id_estudiante)
        if estudiante is None:
            self.interfaz.error(f"No existe un estudiante con id {id_estudiante}")
        else:
            self.interfaz.mostrar_detalle({
                "estudiante": estudiante.obtener_nombre_completo(),
                "notas": estudiante.notas,
                "promedio": estudiante.obtener_promedio(),
            })
        self.interfaz.pausa()

    def materias_en_comun(self):
        self.interfaz.titulo("MATERIAS EN COMÚN")
        id_a = self.interfaz.pedir_entero("Id del primer estudiante")
        id_b = self.interfaz.pedir_entero("Id del segundo estudiante")
        if id_a is None or id_b is None:
            return self.interfaz.pausa()
        exito, resultado = self.estudiantes.estudiantes_en_comun(id_a, id_b)
        if exito:
            self.interfaz.mostrar_lista("Materias que comparten:", sorted(resultado))
        else:
            self.interfaz.error(resultado)
        self.interfaz.pausa()

    def materias_ofertadas(self):
        self.interfaz.titulo("MATERIAS OFERTADAS")
        materias = self.estudiantes.materias_ofertadas()
        self.interfaz.mostrar_lista("Materias inscritas (sin repetir):", sorted(materias))
        self.interfaz.pausa()

    # =====================================================================
    # SUBMENÚ DOCENTES (TAREA 1)
    # =====================================================================
    def menu_docentes(self):
        c, col = self.docentes, self.COLUMNAS_DOCENTE
        opciones = {
            "1": ("Crear docente", lambda: self.crear(c, "CREAR DOCENTE")),
            "2": ("Ver todos", lambda: self.ver_todos(c, "LISTA DE DOCENTES", col)),
            "3": ("Buscar", lambda: self.buscar(c, "BUSCAR DOCENTE", col)),
            "4": ("Ver por id", lambda: self.ver_por_id(c, "VER DOCENTE")),
            "5": ("Actualizar", lambda: self.actualizar(c, "ACTUALIZAR DOCENTE")),
            "6": ("Eliminar", lambda: self.eliminar(
                c, "ELIMINAR DOCENTE",
                lambda d: self.cursos.quitar_referencias("docente", d.id))),
            "7": ("Asignar asignatura", self.asignar_asignatura_docente),
            "8": ("Quitar asignatura", self.quitar_asignatura_docente),
            "9": ("Docentes por especialidad", self.docentes_por_especialidad),
            "0": ("Volver al menú principal", None),
        }
        self.ejecutar_submenu("GESTIÓN DE DOCENTES", opciones)

    def asignar_asignatura_docente(self):
        self.interfaz.titulo("ASIGNAR ASIGNATURA A DOCENTE")
        id_docente = self.interfaz.pedir_entero("Id del docente")
        if id_docente is None:
            return self.interfaz.pausa()
        codigo = self.interfaz.pedir_texto("Código de la asignatura")
        exito, mensaje = self.docentes.asignar_asignatura(id_docente, codigo)
        self.interfaz.mostrar_resultado(exito, mensaje)
        self.interfaz.pausa()

    def quitar_asignatura_docente(self):
        self.interfaz.titulo("QUITAR ASIGNATURA A DOCENTE")
        id_docente = self.interfaz.pedir_entero("Id del docente")
        if id_docente is None:
            return self.interfaz.pausa()
        codigo = self.interfaz.pedir_texto("Código de la asignatura")
        exito, mensaje = self.docentes.quitar_asignatura(id_docente, codigo)
        self.interfaz.mostrar_resultado(exito, mensaje)
        self.interfaz.pausa()

    def docentes_por_especialidad(self):
        self.interfaz.titulo("DOCENTES POR ESPECIALIDAD")
        agrupados = self.docentes.docentes_por_especialidad()
        if not agrupados:
            self.interfaz.info("Todavía no hay docentes.")
        for especialidad, nombres in sorted(agrupados.items()):
            self.interfaz.mostrar_lista(f"{especialidad}:", nombres)
        self.interfaz.pausa()

    # =====================================================================
    # SUBMENÚ ASIGNATURAS (TAREA 2)
    # =====================================================================
    def menu_asignaturas(self):
        c, col = self.asignaturas, self.COLUMNAS_ASIGNATURA
        opciones = {
            "1": ("Crear asignatura", lambda: self.crear(c, "CREAR ASIGNATURA")),
            "2": ("Ver todas", lambda: self.ver_todos(c, "LISTA DE ASIGNATURAS", col)),
            "3": ("Buscar", lambda: self.buscar(c, "BUSCAR ASIGNATURA", col)),
            "4": ("Ver por id", lambda: self.ver_por_id(c, "VER ASIGNATURA")),
            "5": ("Actualizar", lambda: self.actualizar(c, "ACTUALIZAR ASIGNATURA")),
            "6": ("Eliminar", lambda: self.eliminar(
                c, "ELIMINAR ASIGNATURA", self.limpiar_asignatura)),
            "0": ("Volver al menú principal", None),
        }
        self.ejecutar_submenu("GESTIÓN DE ASIGNATURAS", opciones)

    def limpiar_asignatura(self, asignatura):
        """Al eliminar una asignatura, se quita de docentes y cursos."""
        self.docentes.quitar_asignatura_de_todos(asignatura.codigo)
        self.cursos.quitar_referencias("asignatura", asignatura.codigo)

    # =====================================================================
    # SUBMENÚ CURSOS (TAREA 3)
    # =====================================================================
    def menu_cursos(self):
        c, col = self.cursos, self.COLUMNAS_CURSO
        opciones = {
            "1": ("Crear curso", lambda: self.crear(c, "CREAR CURSO")),
            "2": ("Ver todos", lambda: self.ver_todos(c, "LISTA DE CURSOS", col)),
            "3": ("Buscar", lambda: self.buscar(c, "BUSCAR CURSO", col)),
            "4": ("Ver detalle por id", self.ver_detalle_curso),
            "5": ("Actualizar", lambda: self.actualizar(c, "ACTUALIZAR CURSO")),
            "6": ("Eliminar", lambda: self.eliminar(c, "ELIMINAR CURSO")),
            "7": ("Asignar docente", self.asignar_docente_curso),
            "8": ("Agregar asignatura", self.agregar_asignatura_curso),
            "9": ("Inscribir estudiante", self.inscribir_estudiante_curso),
            "10": ("Retirar estudiante", self.retirar_estudiante_curso),
            "0": ("Volver al menú principal", None),
        }
        self.ejecutar_submenu("GESTIÓN DE CURSOS", opciones)

    def ver_detalle_curso(self):
        self.interfaz.titulo("DETALLE DEL CURSO")
        id_curso = self.interfaz.pedir_entero("Id del curso")
        if id_curso is None:
            return self.interfaz.pausa()
        detalle = self.cursos.detalle(id_curso)
        if detalle is None:
            self.interfaz.error(f"No existe un curso con id {id_curso}")
        else:
            self.interfaz.mostrar_detalle(detalle)
        self.interfaz.pausa()

    def _operacion_curso(self, titulo, etiqueta, funcion, pedir_numero=True):
        """Patrón repetido: pedir id de curso + un dato, llamar al controlador."""
        self.interfaz.titulo(titulo)
        id_curso = self.interfaz.pedir_entero("Id del curso")
        if id_curso is None:
            return self.interfaz.pausa()
        if pedir_numero:
            valor = self.interfaz.pedir_entero(etiqueta)
            if valor is None:
                return self.interfaz.pausa()
        else:
            valor = self.interfaz.pedir_texto(etiqueta)
        exito, mensaje = funcion(id_curso, valor)
        self.interfaz.mostrar_resultado(exito, mensaje)
        self.interfaz.pausa()

    def asignar_docente_curso(self):
        self._operacion_curso("ASIGNAR DOCENTE AL CURSO", "Id del docente",
                              self.cursos.asignar_docente)

    def agregar_asignatura_curso(self):
        self._operacion_curso("AGREGAR ASIGNATURA AL CURSO", "Código de la asignatura",
                              self.cursos.agregar_asignatura, pedir_numero=False)

    def inscribir_estudiante_curso(self):
        self._operacion_curso("INSCRIBIR ESTUDIANTE EN CURSO", "Id del estudiante",
                              self.cursos.inscribir_estudiante)

    def retirar_estudiante_curso(self):
        self._operacion_curso("RETIRAR ESTUDIANTE DEL CURSO", "Id del estudiante",
                              self.cursos.retirar_estudiante)

    # =====================================================================
    # RESUMEN
    # =====================================================================
    def resumen(self):
        self.interfaz.titulo("RESUMEN DEL SISTEMA")
        # DICCIONARIO de resumen: etiqueta -> cantidad
        self.interfaz.mostrar_detalle({
            "estudiantes": len(self.estudiantes.obtener_todos()),
            "docentes": len(self.docentes.obtener_todos()),
            "asignaturas": len(self.asignaturas.obtener_todos()),
            "cursos": len(self.cursos.obtener_todos()),
        })
        self.interfaz.pausa()


if __name__ == "__main__":
    try:
        SistemaAcademico().iniciar()
    except (KeyboardInterrupt, EOFError):
        print("\nPrograma interrumpido por el usuario.")
