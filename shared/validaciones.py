# =====================================================================
# PROCESO 2 · Funciones de validación
# Funciones pequeñas que responden True (correcto) o False (incorrecto).
# Las usan los modelos y los controladores para revisar lo que
# escribió el usuario. Ninguna imprime nada.
# =====================================================================


def esta_vacio(texto):
    """True si el texto está vacío o solo tiene espacios."""
    return str(texto).strip() == ""


def es_email_valido(texto):
    """True si el email tiene un @, algo antes y un punto en el dominio.
    Ejemplo válido: ana@correo.com"""
    texto = str(texto).strip()
    if texto.count("@") != 1:          # debe tener exactamente un @
        return False
    usuario, dominio = texto.split("@")
    return usuario != "" and "." in dominio and not dominio.endswith(".")


def es_entero_en_rango(texto, minimo, maximo):
    """True si el texto es un número entero entre minimo y maximo."""
    texto = str(texto).strip()
    if not texto.isdigit():            # isdigit(): solo dígitos 0-9
        return False
    return minimo <= int(texto) <= maximo


# ---------------------------------------------------------------------
# PRUEBAS: se ejecutan solo si abres ESTE archivo y le das ▶ (Run).
# ---------------------------------------------------------------------
def probar():
    print("\n=== PRUEBAS DE validaciones ===")
    # Cada prueba es una TUPLA: (descripción, resultado obtenido, resultado esperado)
    pruebas = [
        ("Texto vacío se detecta", esta_vacio("   "), True),
        ("Texto con letras no está vacío", esta_vacio("Ana"), False),
        ("Email correcto", es_email_valido("ana@correo.com"), True),
        ("Email sin @", es_email_valido("anacorreo.com"), False),
        ("Email con dos @", es_email_valido("ana@@correo.com"), False),
        ("Email sin punto", es_email_valido("ana@correo"), False),
        ("Número 5 entre 1 y 10", es_entero_en_rango("5", 1, 10), True),
        ("Número 15 fuera de 1 a 10", es_entero_en_rango("15", 1, 10), False),
        ("Letras no son número", es_entero_en_rango("abc", 1, 10), False),
        ("Número negativo no vale", es_entero_en_rango("-3", 1, 10), False),
    ]
    for descripcion, obtenido, esperado in pruebas:
        if obtenido == esperado:
            print(f"✔ {descripcion}")
        else:
            print(f"✘ ERROR: {descripcion}")


if __name__ == "__main__":
    probar()
