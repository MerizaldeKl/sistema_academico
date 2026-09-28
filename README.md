# Sistema Académico · CRUD en Python con MVC y JSON

Práctica **G001-S05 · Estructura de Datos** (UNEMI).
Sistema de consola para gestionar **Estudiantes, Docentes, Asignaturas y Cursos**,
organizado con el patrón **MVC**, las cuatro colecciones de Python
(`list`, `tuple`, `set`, `dict`) y almacenamiento en archivos **JSON**.

Autor: Kleber Merizalde García

## Cómo ejecutarlo

Requisitos: Python 3.8 o superior (no usa librerías externas).

```bash
cd sistema_academico
python main.py        # en Mac/Linux: python3 main.py
```

La carpeta `data/` y los archivos JSON se crean solos la primera vez que se guarda algo.

## Estructura del proyecto (procesos de la guía G001)

```
sistema_academico/
├── main.py                      ← PROCESO 6: clase SistemaAcademico + menú principal
├── shared/                      ← PROCESO 2: código reutilizable
│   ├── __init__.py
│   ├── archivo_json.py          ← clase ArchivoJSON (leer / guardar)
│   ├── validaciones.py          ← email, campos obligatorios, notas, créditos
│   └── utilidades.py            ← siguiente id, duplicados, búsqueda
├── models/                      ← PROCESO 3: modelos de datos
│   ├── __init__.py
│   ├── estudiante.py            ← clase Estudiante
│   ├── docente.py               ← clase Docente    (TAREA 1)
│   ├── asignatura.py            ← clase Asignatura (TAREA 2)
│   └── curso.py                 ← clase Curso      (TAREA 3)
├── controllers/                 ← PROCESO 4: lógica CRUD
│   ├── __init__.py
│   ├── controlador_estudiante.py
│   ├── controlador_docente.py   ← TAREA 1
│   ├── controlador_asignatura.py← TAREA 2
│   └── controlador_curso.py     ← TAREA 3
├── views/                       ← PROCESO 5: interfaz de usuario
│   ├── __init__.py
│   └── interfaz_consola.py      ← clase InterfazConsola
└── data/                        ← PROCESO 7: se crea automáticamente
    ├── estudiantes.json
    ├── docentes.json
    ├── asignaturas.json
    └── cursos.json
```

## Responsabilidad de cada capa (MVC)

| Capa | Carpeta | Sí hace | Nunca hace |
|---|---|---|---|
| Modelo | `models/` | Define qué es cada dato y lo convierte a/desde diccionario | Leer archivos, `input()`, `print()` |
| Controlador | `controllers/` | CRUD, validaciones, detectar duplicados, guardar con ArchivoJSON | `input()`, `print()` |
| Vista | `views/` | Menús, pedir datos, mostrar tablas y mensajes | Abrir JSON, validar reglas |
| Apoyo | `shared/` | Herramientas reutilizables | Conocer qué es un Estudiante o Docente |
| Integración | `main.py` | Conecta controladores e interfaz | Validar o guardar directamente |

Cada operación del controlador devuelve una tupla `(exito, mensaje)` y la vista decide cómo mostrarla.

## Operaciones disponibles

| Módulo | CRUD + Buscar | Operaciones extra |
|---|---|---|
| Estudiantes | Crear, ver todos, buscar, ver por id, actualizar, eliminar | Agregar nota (0–20), ver promedio, materias en común, materias ofertadas |
| Docentes | Crear, ver todos, buscar, ver por id, actualizar, eliminar | Asignar/quitar asignatura, docentes por especialidad |
| Asignaturas | Crear, ver todas, buscar, ver por id, actualizar, eliminar | — |
| Cursos | Crear, ver todos, buscar, ver detalle, actualizar, eliminar | Asignar docente, agregar asignatura, inscribir/retirar estudiante |

## Validaciones

- Campos obligatorios vacíos.
- Formato de email.
- Email de estudiante y de docente no repetido (con `set`).
- Carnet de estudiante no repetido (con `set`).
- Código de asignatura no repetido y no editable.
- Créditos: número entero entre 1 y 10.
- Nota: número entre 0 y 20.
- Curso: no se repite el mismo nombre en el mismo periodo (`set` de tuplas).
- Id inexistente en ver, actualizar, eliminar y en las conexiones entre módulos.
- Al eliminar un docente, estudiante o asignatura se limpian sus referencias en los cursos.

## Uso de las cuatro colecciones

| Colección | Dónde se usa |
|---|---|
| `list` | Registros leídos del JSON; notas de cada materia |
| `tuple` | Campos de cada modelo, campos obligatorios/buscables, retornos `(exito, mensaje)`, columnas de tablas |
| `set` | Emails/carnets/códigos registrados, materias de un estudiante, asignaturas de un docente, estudiantes de un curso |
| `dict` | Cada registro, notas por materia, opciones de menú, docentes por especialidad |

JSON no conoce los `set`: se guardan como lista (`sorted(...)`) y al leer se vuelven a convertir con `set(...)`.

## Atributos definidos

La guía G001 no especifica los atributos de Docente, Asignatura y Curso. Se definieron así:

- **Estudiante:** id, nombre, apellido, email, carnet, notas, materias (igual que la guía CRUD).
- **Docente:** id, nombre, apellido, email, teléfono, especialidad, asignaturas.
- **Asignatura:** id, código, nombre, créditos.
- **Curso:** id, nombre, periodo, id_docente, asignaturas, estudiantes.
