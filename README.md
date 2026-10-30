# Data Science II — Módulo 9.1

## Tracking de datasets y experimentos con SQLAlchemy 2.0

**Objetivo.** Demostrar el mapeo declarativo en SQLAlchemy 2.0 mediante dos modelos Python que generan tablas reales en una base de datos SQLite. El ejercicio utiliza `DeclarativeBase`, `Mapped` y `mapped_column` en lugar de la sintaxis ORM heredada.

### Estructura

```text
.
├── models.py                  # Base y dos clases ORM
├── main.py                    # Inicializa SQLite, instancia y persiste ejemplos
├── requirements.txt           # SQLAlchemy 2.x
├── tests/test_models.py       # Pruebas automáticas
├── evidencia/resultado.txt    # Ejecución y pruebas verificadas
├── .gitignore                 # No versiona analytics.db ni __pycache__
└── README.md
```

### Modelos y campos

| Clase / tabla | Columna | Tipo SQLAlchemy | Significado |
| --- | --- | --- | --- |
| `Dataset` / `datasets` | `id` (PK) | `Integer` | Identificador autoincremental |
| | `name` | `String(120)` | Nombre descriptivo del dataset |
| | `source_url` | `String(500)` | URL de procedencia |
| | `num_rows` | `Integer` | Cantidad de filas (≥ 0) |
| `ModelExperiment` / `model_experiments` | `id` (PK) | `Integer` | Identificador autoincremental |
| | `algorithm_name` | `String(120)` | Algoritmo utilizado |
| | `accuracy` | `Float` | Exactitud entre 0 y 1 |
| | `is_deployed` | `Boolean` | Indica si se encuentra desplegado |

Los dos modelos son **independientes**, tal como pide la consigna; una relación entre experimento y dataset podría incorporarse más adelante.

### Requisitos e instalación (Windows / PowerShell)

Necesitás Python 3.10 o superior y acceso a `pip`. Desde la carpeta del proyecto:

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe main.py
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

Alternativa sin entorno virtual, si ya tenés Python configurado:

```powershell
py -m pip install -r requirements.txt
py main.py
py -m unittest discover -s tests -v
```

### ¿Qué sucede al ejecutar?

1. `create_engine("sqlite:///analytics.db")` abre o crea un archivo SQLite **persistente** en la carpeta donde ejecutás el script.
2. `Base.metadata.create_all(engine)` genera `datasets` y `model_experiments` si todavía no existen.
3. Se instancian un `Dataset` y un `ModelExperiment` utilizando el mapeo ORM y se muestran por consola.
4. Como demostración **adicional** (no exigida por la actividad), una `Session` guarda los dos objetos y consulta sus cantidades; si repetís el comando, no duplica los ejemplos.
5. Finaliza mostrando `VALIDACIONES FINALES: OK`.

El nombre de dataset, su URL (`example.com`), cantidad de filas y precisión del experimento son **datos ficticios de demostración**, no resultados de un proyecto real. El `accuracy=0.87` representa 87%.

### Pruebas y validación

`unittest` verifica: clases declarativas, nombres y columnas, claves primarias, tipos, instanciación ORM, persistencia real, restricciones, creación del archivo `.db` y ejecución repetida sin duplicación.

Al ejecutar deberías ver `Ran 12 tests` y `OK`. Los resultados comprobados se incluyen en `evidencia/resultado.txt`.

### Buenas prácticas

- **SQLAlchemy 2.0:** tipado con `Mapped` y `mapped_column`; no se usa `Column()` ni `declarative_base()` heredados.
- **Base persistente local:** el archivo `analytics.db` se crea al ejecutar, pero **no se publica en GitHub** porque está excluido por `.gitignore`.
- **No hay credenciales:** SQLite es local, por lo que no requiere usuario o contraseña.
- **Alcance:** `create_all` inicializa tablas nuevas; **no migra cambios** en tablas existentes. En proyectos mayores convendría una herramienta de migraciones como Alembic.

### Documentación de referencia

- [SQLAlchemy 2.0 — Declarative Mapping](https://docs.sqlalchemy.org/en/20/orm/declarative_styles.html)
- [SQLAlchemy 2.0 — Declarative Tables](https://docs.sqlalchemy.org/en/20/orm/declarative_tables.html)
