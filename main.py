# =====================================================================
# PROCESO 6 · Integración: clase SistemaAcademico y menú principal
#
# SistemaAcademico conecta las piezas del MVC:
#   - InterfazConsola (Vista): pide y muestra datos.
#   - Los 4 controladores: hacen el CRUD y guardan en JSON.
#
# Para usar el sistema:   python main.py
# Para correr TODAS las pruebas automáticas:   python pruebas.py
# =====================================================================

from views.interfaz_consola import InterfazConsola
from controllers.controlador_estudiante import ControladorEstudiante
from controllers.controlador_docente import ControladorDocente
from controllers.controlador_asignatura import ControladorAsignatura
from controllers.controlador_curso import ControladorCurso


class SistemaAcademico:

    def __init__(self):
        self.interfaz = InterfazConsola()
        # DICCIONARIO: nombre de la sección -> su controlador
        self.secciones = {
            "1": ("Estudiantes", ControladorEstudiante()),
            "2": ("Docentes", ControladorDocente()),
            "3": ("Asignaturas", ControladorAsignatura()),
            "4": ("Cursos", ControladorCurso()),
        }

    # ---------------- Menú principal ----------------
    def iniciar(self):
        opciones = {"1": "Estudiantes", "2": "Docentes", "3": "Asignaturas",
                    "4": "Cursos", "0": "Salir"}
        while True:
            tecla = self.interfaz.mostrar_menu("SISTEMA ACADÉMICO", opciones)
            if tecla == "0":
                self.interfaz.info("¡Hasta luego!")
                break
            nombre, controlador = self.secciones[tecla]   # desempaqueto la TUPLA
            self.submenu(nombre, controlador)

    # ---------------- Submenú CRUD (sirve para las 4 secciones) ----------------
    def submenu(self, nombre, controlador):
        opciones = {"1": "Crear", "2": "Ver todos", "3": "Buscar",
                    "4": "Actualizar", "5": "Eliminar", "0": "Volver"}
        while True:
            tecla = self.interfaz.mostrar_menu(f"GESTIÓN DE {nombre.upper()}", opciones)
            if tecla == "1":
                self.crear(nombre, controlador)
            elif tecla == "2":
                self.ver_todos(nombre, controlador)
            elif tecla == "3":
                self.buscar(nombre, controlador)
            elif tecla == "4":
                self.actualizar(nombre, controlador)
            elif tecla == "5":
                self.eliminar(nombre, controlador)
            elif tecla == "0":
                break
            self.interfaz.pausa()

    # ---------------- Operaciones ----------------
    def crear(self, nombre, controlador):
        while True:
            self.interfaz.titulo(f"CREAR - {nombre.upper()}")
            datos = self.interfaz.pedir_formulario(controlador.CAMPOS)
            exito, mensaje = controlador.crear(datos)
            self.interfaz.mostrar_resultado(exito, mensaje)
            # Si hubo un error, se le explica y puede volver a intentarlo
            if exito or not self.interfaz.confirmar("\n¿Desea corregir los datos e intentarlo otra vez?"):
                break

    def ver_todos(self, nombre, controlador):
        self.interfaz.titulo(f"LISTA DE {nombre.upper()}")
        self.interfaz.mostrar_lista(controlador.obtener_todos())

    def buscar(self, nombre, controlador):
        self.interfaz.titulo(f"BUSCAR - {nombre.upper()}")
        texto = self.interfaz.pedir_texto("Escriba lo que desea buscar")
        self.interfaz.mostrar_lista(controlador.buscar(texto))

    def pedir_registro_existente(self, controlador):
        """Pide un id y devuelve el registro. Si no existe, avisa y devuelve None."""
        id_buscado = self.interfaz.pedir_entero("Id del registro")
        registro = controlador.obtener_por_id(id_buscado)
        if registro is None:
            self.interfaz.error(f"No existe un registro con id {id_buscado}. "
                                "Use 'Ver todos' para conocer los ids.")
        return registro

    def actualizar(self, nombre, controlador):
        self.interfaz.titulo(f"ACTUALIZAR - {nombre.upper()}")
        registro = self.pedir_registro_existente(controlador)
        if registro is None:
            return
        self.interfaz.info(f"Editando: {registro}")
        datos = self.interfaz.pedir_cambios(controlador.CAMPOS, registro)
        exito, mensaje = controlador.actualizar(registro.id, datos)
        self.interfaz.mostrar_resultado(exito, mensaje)

    def eliminar(self, nombre, controlador):
        self.interfaz.titulo(f"ELIMINAR - {nombre.upper()}")
        registro = self.pedir_registro_existente(controlador)
        if registro is None:
            return
        if self.interfaz.confirmar(f"¿Seguro que desea eliminar {registro}?"):
            exito, mensaje = controlador.eliminar(registro.id)
            self.interfaz.mostrar_resultado(exito, mensaje)
        else:
            self.interfaz.info("Operación cancelada.")


# Punto de inicio del programa
if __name__ == "__main__":
    try:
        SistemaAcademico().iniciar()
    except KeyboardInterrupt:
        # Si el usuario presiona Ctrl+C, se cierra sin mostrar errores feos
        print("\nPrograma cerrado por el usuario.")
