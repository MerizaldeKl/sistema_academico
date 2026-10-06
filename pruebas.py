# =====================================================================
# Ejecuta TODAS las pruebas automáticas del proyecto de una sola vez.
# Uso:  python pruebas.py
# Cada línea con ✔ es una prueba que pasó; con ✘ es una que falló.
# (La prueba de InterfazConsola es manual: se ejecuta abriendo
#  views/interfaz_consola.py y presionando ▶.)
# =====================================================================

from shared import archivo_json, validaciones, utilidades
from models import estudiante, docente, asignatura, curso
from controllers import (controlador_estudiante, controlador_docente,
                         controlador_asignatura, controlador_curso)

# LISTA con todos los módulos que tienen una función probar()
modulos = [
    archivo_json, validaciones, utilidades,
    estudiante, docente, asignatura, curso,
    controlador_estudiante, controlador_docente,
    controlador_asignatura, controlador_curso,
]

for modulo in modulos:
    modulo.probar()

print("\n=== FIN DE LAS PRUEBAS ===")
