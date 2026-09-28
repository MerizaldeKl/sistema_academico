"""
PROCESO 5 · Interfaz de Usuario: clase InterfazConsola
La Vista solo hace tres cosas: mostrar, pedir datos y mostrar resultados.
No valida reglas del negocio ni abre archivos JSON.
Es el ÚNICO lugar del proyecto donde hay print() e input().
"""

import os


class InterfazConsola:
    # DICCIONARIO: cada color tiene su etiqueta y su código de consola
    COLORES = {
        "ROJO": "\033[91m",
        "VERDE": "\033[92m",
        "AZUL": "\033[94m",
        "AMARILLO": "\033[93m",
        "CYAN": "\033[96m",
        "BLANCO": "\033[97m",
        "RESET": "\033[0m",
    }
    # TUPLA: respuestas afirmativas aceptadas. Es fija, por eso no es lista.
    RESPUESTAS_SI = ("si", "sí", "s", "yes", "y")

    # ---------------- mensajes ----------------
    def limpiar_pantalla(self):
        os.system("clear" if os.name == "posix" else "cls")

    def imprimir_color(self, texto, color):
        codigo = self.COLORES.get(color, self.COLORES["BLANCO"])
        print(f"{codigo}{texto}{self.COLORES['RESET']}")

    def titulo(self, texto):
        self.limpiar_pantalla()
        self.imprimir_color("=" * 70, "AZUL")
        print(texto.center(70))
        self.imprimir_color("=" * 70, "AZUL")
        print()

    def exito(self, mensaje):
        self.imprimir_color(f"✓ {mensaje}", "VERDE")

    def error(self, mensaje):
        self.imprimir_color(f"✗ {mensaje}", "ROJO")

    def info(self, mensaje):
        self.imprimir_color(f"ℹ {mensaje}", "CYAN")

    def mostrar_resultado(self, exito, mensaje):
        """Recibe la TUPLA (exito, mensaje) que devuelven los controladores."""
        if exito:
            self.exito(mensaje)
        else:
            self.error(mensaje)

    def pausa(self):
        input("\nPresione Enter para continuar...")

    # ---------------- menús ----------------
    def mostrar_menu(self, titulo, opciones):
        """opciones: DICCIONARIO {tecla: (texto, funcion)}. Devuelve la tecla."""
        self.titulo(titulo)
        for tecla, (texto, _funcion) in opciones.items():
            print(f"  {tecla}. {texto}")
        print()
        return input("Seleccione una opción: ").strip()

    # ---------------- pedir datos ----------------
    def pedir_texto(self, etiqueta):
        return input(f"{etiqueta}: ").strip()

    def pedir_entero(self, etiqueta):
        """Devuelve un entero, o None si el usuario no escribió un número."""
        try:
            return int(input(f"{etiqueta}: "))
        except ValueError:
            self.error("Debe escribir un número entero")
            return None

    def confirmar(self, pregunta):
        respuesta = input(f"{pregunta} (si/no): ").strip().lower()
        return respuesta in self.RESPUESTAS_SI

    def pedir_formulario(self, campos):
        """Recorre la TUPLA de campos y arma un DICCIONARIO con las respuestas.
        Si mañana se agrega un campo al Modelo, este formulario se actualiza solo."""
        datos = {}
        for campo in campos:
            datos[campo] = input(f"{campo.capitalize()}: ")
        return datos

    def pedir_cambios(self, campos, objeto):
        """Arma un DICCIONARIO solo con los campos que el usuario escribió."""
        print("Deje en blanco el campo que no quiera cambiar.\n")
        cambios = {}
        for campo in campos:
            actual = getattr(objeto, campo)
            nuevo = input(f"{campo.capitalize()} [{actual}]: ").strip()
            if nuevo:
                cambios[campo] = nuevo
        return cambios

    # ---------------- mostrar datos ----------------
    def _formatear(self, valor):
        """Convierte listas, conjuntos y diccionarios en texto legible."""
        if isinstance(valor, (list, set, tuple)):
            return ", ".join(str(v) for v in sorted(valor, key=str)) or "-"
        if isinstance(valor, dict):
            partes = [f"{clave}: {valores}" for clave, valores in valor.items()]
            return " | ".join(partes) or "-"
        if valor is None or valor == "":
            return "-"
        return str(valor)

    def mostrar_tabla(self, objetos, columnas):
        """columnas: TUPLA de tuplas (atributo, titulo, ancho)."""
        encabezado = "".join(f"{titulo:<{ancho}}" for _attr, titulo, ancho in columnas)
        total = sum(ancho for _attr, _titulo, ancho in columnas)
        print(encabezado)
        print("-" * total)
        for objeto in objetos:
            fila = ""
            for atributo, _titulo, ancho in columnas:
                texto = self._formatear(getattr(objeto, atributo, ""))
                fila += f"{texto[:ancho - 1]:<{ancho}}"
            print(fila)
        print("-" * total)
        self.info(f"Total: {len(objetos)} registro(s)")

    def mostrar_detalle(self, diccionario):
        """Recorre el DICCIONARIO: clave y valor a la vez."""
        for clave, valor in diccionario.items():
            print(f"  {clave.replace('_', ' ').capitalize():<14}: {self._formatear(valor)}")

    def mostrar_lista(self, titulo, elementos):
        print(titulo)
        if not elementos:
            self.info("(vacío)")
        for elemento in elementos:
            print(f"  • {elemento}")
