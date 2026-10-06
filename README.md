# Sistema Académico · CRUD en Python con MVC y JSON

Práctica **G001 · Estructura de Datos** (UNEMI)
Autor: Kelvin Merizalde García

Sistema de consola para gestionar **Estudiantes, Docentes, Asignaturas y Cursos**
con el patrón **MVC**, guardando los datos en archivos **JSON**.

## Cómo ejecutar

Requisito: Python 3 (no usa librerías externas).

| Qué quiero hacer | Comando |
|---|---|
| Usar el sistema | `python main.py` |
| Correr todas las pruebas automáticas | `python pruebas.py` |
| Probar un solo archivo | Abrirlo en VS Code y presionar ▶ (Run) |

## Estructura (procesos de G001)

```
sistema_academico/
├── main.py                 ← PROCESO 6: clase SistemaAcademico y menú principal
├── pruebas.py              ← ejecuta todas las pruebas
├── shared/                 ← PROCESO 2: código reutilizable
│   ├── archivo_json.py     ← clase ArchivoJSON (leer y guardar)
│   ├── validaciones.py     ← funciones de validación
│   └── utilidades.py       ← siguiente id, duplicados, posiciones
├── models/                 ← PROCESO 3: modelos de datos
│   ├── estudiante.py       ← clase Estudiante
│   ├── docente.py          ← clase Docente    (TAREA 1)
│   ├── asignatura.py       ← clase Asignatura (TAREA 2)
│   └── curso.py            ← clase Curso      (TAREA 3)
├── controllers/            ← PROCESO 4: lógica CRUD
│   ├── controlador_estudiante.py
│   ├── controlador_docente.py     (TAREA 1)
│   ├── controlador_asignatura.py  (TAREA 2)
│   └── controlador_curso.py       (TAREA 3)
├── views/                  ← PROCESO 5: interfaz de usuario
│   └── interfaz_consola.py ← clase InterfazConsola
└── data/                   ← PROCESO 7: se crea sola con los archivos JSON
```

Cada carpeta tiene un `__init__.py` vacío para que Python la reconozca como paquete.

## MVC: qué hace cada capa

| Capa | Carpeta | Qué hace |
|---|---|---|
| Modelo | `models/` | Define cada dato, lo valida y lo convierte a diccionario |
| Controlador | `controllers/` | Crear, leer, buscar, actualizar y eliminar; evita duplicados; guarda en JSON |
| Vista | `views/` | Único lugar con `print()` e `input()` |
| Apoyo | `shared/` | Herramientas que usan todos |

## Pruebas

Cada archivo tiene al final una función `probar()` que se ejecuta solo cuando se
abre ese archivo directamente. Las pruebas revisan los errores que puede cometer
un usuario (campos vacíos, email mal escrito, letras donde van números, datos
repetidos, ids que no existen).

Además, el programa **no se cierra** cuando el usuario escribe mal: le explica
qué está mal y le deja escribir de nuevo.

## Datos de cada registro

G001 no especifica los atributos, así que se definieron estos:

- **Estudiante:** id, nombre, apellido, email, carnet (email y carnet no se repiten)
- **Docente:** id, nombre, apellido, email, especialidad (email no se repite)
- **Asignatura:** id, código, nombre, créditos del 1 al 10 (código no se repite)
- **Curso:** id, nombre, paralelo, periodo (no se repite el mismo curso, paralelo y periodo)
