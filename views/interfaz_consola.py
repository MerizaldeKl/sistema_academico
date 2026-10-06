# =====================================================================
# PROCESO 5 · Interfaz de Usuario: clase InterfazConsola
# Es la VISTA: el ÚNICO lugar donde se usa print() e input().
# Muestra menús, pide datos y muestra mensajes.
# Si el usuario escribe algo mal, le explica y le deja intentar de
# nuevo, así el programa nunca se cierra por un error al escribir.
# =====================================================================

import os


class InterfazConsola:

    # TUPLAS con las respuestas aceptadas para "sí" y "no"
    RESPUESTAS_SI = ("si", "sí", "s")
    RESPUESTAS_NO = ("no", "n")

    # ---------------- Mensajes ----------------
    def limpiar_pantalla(self):
        os.system("cls" if os.name == "nt" else "clear")   # nt = Windows

    def titulo(self, texto):
        self.limpiar_pantalla()
        print("=" * 60)
        print(texto.center(60))
        print("=" * 60)

    def exito(self, mensaje):
        print(f"\n✔ {mensaje}")

    def error(self, mensaje):
        print(f"\n✘ {mensaje}")

    def info(self, mensaje):
        print(f"\nℹ {mensaje}")

    def pausa(self):
        input("\nPresione Enter para continuar...")

    def mostrar_resultado(self, exito, mensaje):
        """Recibe la TUPLA (exito, mensaje) que devuelve el controlador."""
        if exito:
            self.exito(mensaje)
        else:
            self.error(mensaje)

    def mostrar_lista(self, objetos):
        """Imprime cada objeto usando su __str__."""
        if not objetos:
            self.info("No hay registros para mostrar.")
            return
        print()
        for objeto in objetos:
            print(" ", objeto)
        print(f"\nTotal: {len(objetos)} registro(s)")

    # ---------------- Menús ----------------
    def mostrar_menu(self, titulo, opciones):
        """opciones: DICCIONARIO {"1": "Texto de la opción", ...}.
        Repite la pregunta hasta que el usuario elija una opción válida."""
        self.titulo(titulo)
        for tecla, texto in opciones.items():
            print(f"  {tecla}. {texto}")
        while True:
            tecla = input("\nSeleccione una opción: ").strip()
            if tecla in opciones:          # 'in' busca en las claves del diccionario
                return tecla
            validas = ", ".join(opciones.keys())
            self.error(f"Opción no válida. Escriba uno de estos números: {validas}")

    # ---------------- Pedir datos ----------------
    def pedir_texto(self, etiqueta):
        """Pide un texto que NO puede quedar vacío."""
        while True:
            texto = input(f"{etiqueta}: ").strip()
            if texto != "":
                return texto
            self.error("Este dato no puede quedar vacío. Escríbalo de nuevo.")

    def pedir_entero(self, etiqueta):
        """Pide un número entero. Si escriben letras, vuelve a preguntar."""
        while True:
            texto = input(f"{etiqueta}: ").strip()
            if texto.isdigit():
                return int(texto)
            self.error("Debe escribir un número entero (solo dígitos). Ejemplo: 1")

    def confirmar(self, pregunta):
        """Pregunta sí o no. Repite hasta recibir una respuesta válida."""
        while True:
            respuesta = input(f"{pregunta} (si/no): ").strip().lower()
            if respuesta in self.RESPUESTAS_SI:
                return True
            if respuesta in self.RESPUESTAS_NO:
                return False
            self.error("Responda solo 'si' o 'no'.")

    def pedir_formulario(self, campos):
        """Recorre la TUPLA de campos y arma un DICCIONARIO con las respuestas."""
        datos = {}
        for campo in campos:
            datos[campo] = self.pedir_texto(campo.capitalize())
        return datos

    def pedir_cambios(self, campos, objeto):
        """Muestra el valor actual entre [ ]. Si el usuario presiona Enter
        sin escribir nada, se queda el valor actual."""
        print("Presione Enter para dejar el valor actual.\n")
        datos = {}
        for campo in campos:
            actual = getattr(objeto, campo)     # getattr: lee el atributo por su nombre
            nuevo = input(f"{campo.capitalize()} [{actual}]: ").strip()
            datos[campo] = nuevo if nuevo != "" else actual
        return datos


# ---------------------------------------------------------------------
# PRUEBA MANUAL: se ejecuta solo si abres ESTE archivo y le das ▶ (Run).
# Escribe cosas incorrectas a propósito para comprobar que el
# programa te corrige y no se cierra.
# ---------------------------------------------------------------------
def probar():
    interfaz = InterfazConsola()
    print("\n=== PRUEBA MANUAL DE InterfazConsola ===")
    print("Escriba datos INCORRECTOS a propósito y vea cómo responde.\n")

    print("1) Escriba letras, por ejemplo 'abc', y luego un número:")
    numero = interfaz.pedir_entero("Número")
    interfaz.exito(f"Recibido el número {numero}")

    print("\n2) Presione Enter sin escribir nada, y luego escriba su nombre:")
    nombre = interfaz.pedir_texto("Nombre")
    interfaz.exito(f"Recibido el nombre {nombre}")

    print("\n3) Escriba 'quizás', y luego 'si' o 'no':")
    respuesta = interfaz.confirmar("¿Le gusta programar?")
    interfaz.exito(f"Respuesta recibida: {respuesta}")

    interfaz.info("Prueba terminada: el programa nunca se cerró por un error al escribir.")


if __name__ == "__main__":
    probar()
