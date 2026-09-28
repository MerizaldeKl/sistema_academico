"""
PROCESO 2 · Funciones de validación
Reglas pequeñas y reutilizables. Las usan TODOS los controladores.
Ninguna función imprime nada: solo devuelven True/False o un valor.
"""

# TUPLA: valores fijos del sistema, nadie los modifica en ejecución
RANGO_NOTA = (0, 20)          # (mínimo, máximo) de una nota
RANGO_CREDITOS = (1, 10)      # (mínimo, máximo) de créditos de una asignatura


def es_email_valido(texto):
    """Validación mínima: un @, algo antes, algo después y un punto en el dominio."""
    texto = str(texto).strip()
    if texto.count("@") != 1:
        return False
    usuario, dominio = texto.split("@")
    return len(usuario) > 0 and "." in dominio and not dominio.endswith(".")


def campos_faltantes(valores, obligatorios):
    """LISTA con los campos obligatorios que llegaron vacíos (recorre la TUPLA)."""
    return [campo for campo in obligatorios if not valores.get(campo)]


def campos_no_validos(cambios, permitidos):
    """DIFERENCIA DE CONJUNTOS: campos que se enviaron pero no existen."""
    return set(cambios) - set(permitidos)


def convertir_nota(valor):
    """Devuelve la nota como número si está entre 0 y 20; si no, None."""
    try:
        nota = float(valor)
    except (TypeError, ValueError):
        return None
    minimo, maximo = RANGO_NOTA          # desempaquetado de tupla
    if minimo <= nota <= maximo:
        # 18.0 se guarda como 18; 18.5 se queda como 18.5
        return int(nota) if nota.is_integer() else nota
    return None


def convertir_creditos(valor):
    """Devuelve los créditos como entero si están entre 1 y 10; si no, None."""
    try:
        creditos = int(str(valor).strip())
    except (TypeError, ValueError):
        return None
    minimo, maximo = RANGO_CREDITOS
    if minimo <= creditos <= maximo:
        return creditos
    return None
