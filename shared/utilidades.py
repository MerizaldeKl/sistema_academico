# =====================================================================
# PROCESO 2 · Código reutilizable
# Ayudas que usan los cuatro controladores. Se escriben una sola vez
# aquí para no repetir el mismo código en cada controlador.
# =====================================================================


def siguiente_id(registros):
    """Calcula el id del próximo registro: el mayor id + 1.
    Si la lista está vacía, el primer id es 1."""
    if not registros:
        return 1
    ids = [registro["id"] for registro in registros]   # LISTA de ids
    return max(ids) + 1


def valores_usados(registros, campo, excepto_id=None):
    """Devuelve un CONJUNTO (set) con los valores ya usados en un campo.
    Un set no tiene repetidos y permite preguntar 'in' muy rápido.
    excepto_id sirve al actualizar: no comparo el registro consigo mismo."""
    usados = set()
    for registro in registros:
        if registro["id"] != excepto_id:
            usados.add(str(registro[campo]).strip().lower())
    return usados


def buscar_posicion(registros, id_buscado):
    """Devuelve la posición (índice) del registro en la lista, o None."""
    for posicion, registro in enumerate(registros):
        if registro["id"] == id_buscado:
            return posicion
    return None


def mostrar_prueba(descripcion, paso_la_prueba):
    """Imprime ✔ si la prueba salió bien o ✘ si salió mal.
    Solo se usa en los bloques de PRUEBAS de cada archivo."""
    if paso_la_prueba:
        print(f"✔ {descripcion}")
    else:
        print(f"✘ ERROR: {descripcion}")


# ---------------------------------------------------------------------
# PRUEBAS: se ejecutan solo si abres ESTE archivo y le das ▶ (Run).
# ---------------------------------------------------------------------
def probar():
    print("\n=== PRUEBAS DE utilidades ===")
    registros = [{"id": 1, "email": "ana@x.com"}, {"id": 4, "email": "LUIS@x.com"}]
    mostrar_prueba("Lista vacía: el primer id es 1", siguiente_id([]) == 1)
    mostrar_prueba("El siguiente id después de 4 es 5", siguiente_id(registros) == 5)
    mostrar_prueba("Detecta email usado aunque cambien mayúsculas",
                   "luis@x.com" in valores_usados(registros, "email"))
    mostrar_prueba("excepto_id no cuenta el propio registro",
                   "ana@x.com" not in valores_usados(registros, "email", excepto_id=1))
    mostrar_prueba("Encuentra la posición del id 4", buscar_posicion(registros, 4) == 1)
    mostrar_prueba("Id inexistente devuelve None", buscar_posicion(registros, 99) is None)


if __name__ == "__main__":
    probar()
