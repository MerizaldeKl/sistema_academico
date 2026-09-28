"""
PROCESO 2 · Código reutilizable
Ayudas que se repetían en los cuatro controladores. En lugar de copiar
el mismo código cuatro veces, se escribe una sola vez aquí.
"""


def normalizar_datos(datos, campos):
    """DICCIONARIO con todos los campos de la TUPLA, sin espacios sobrantes."""
    return {campo: str(datos.get(campo, "")).strip() for campo in campos}


def siguiente_id(registros):
    """Calcula el próximo id. Caso explícito para la lista vacía."""
    ids = [registro["id"] for registro in registros]
    return max(ids) + 1 if ids else 1


def valores_registrados(registros, campo, excepto_id=None):
    """CONJUNTO con los valores ya usados en un campo (en minúsculas).
    Sirve para detectar duplicados al instante con el operador 'in'."""
    return {
        str(registro.get(campo, "")).strip().lower()
        for registro in registros
        if registro["id"] != excepto_id
    }


def buscar_posicion(registros, id_registro):
    """Devuelve el índice del registro dentro de la LISTA, o None si no existe."""
    for indice, registro in enumerate(registros):   # enumerate: índice y valor
        if registro["id"] == id_registro:
            return indice
    return None


def coincide_busqueda(registro, termino, campos):
    """Búsqueda lineal: True si el término aparece en alguno de los campos."""
    for campo in campos:                            # recorro la TUPLA de campos
        if termino in str(registro.get(campo, "")).lower():
            return True
    return False
