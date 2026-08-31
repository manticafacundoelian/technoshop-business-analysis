# 🐍 TechnoShop | Pipeline ETL Modular en Python

Pipeline de ingeniería de datos desarrollado con **Python, Pandas y NumPy** bajo una arquitectura modular para transformar datos transaccionales crudos en conjuntos de datos limpios, consistentes y optimizados para su explotación analítica en SQL y Power BI.

### Stack Técnico Principal:   
![Python](https://img.shields.io/badge/python-3670A0?style=flat-square&logo=python&logoColor=ffdd54) ![Pandas](https://img.shields.io/badge/pandas-%23150458.svg?style=flat-square&logo=pandas&logoColor=white) ![NumPy](https://img.shields.io/badge/numpy-013243?style=flat-square&logo=numpy&logoColor=white)

---

## 🏗️ Arquitectura del Pipeline

El proceso sigue una arquitectura multicapa desacoplada (*Raw → Clean → Processed*). A continuación se detalla la organización de carpetas, la responsabilidad de cada módulo y el flujo de ejecución:

![Estructura del Pipeline](./pipeline_estructure.png)

---

## Características principales

* **Estructura Decoupled:** Módulos independientes orquestados por entidad mediante funciones auxiliares dedicadas.
* **Data Quality Gating:** Auditoría preventiva exhaustiva de anomalías técnicas, reglas de negocio e integridad referencial antes de la fase de limpieza.
* **Sanitización Heurística Extensiva:** Procesamiento modular que abarca normalización de texto, deduplicación e imputaciones lógicas orientadas a la minimización de pérdida de información, integrando mecanismos de contingencia para blindar la integridad referencial.
* **Trazabilidad Centralizada:** Registro continuo y estructurado de hallazgos mediante un sistema dinámico de logs.
* **Data Profiling Automatizado:** Consolidación de métricas de calidad en un reporte estructurado nativo en formato **JSON**.
* **Inyección de Lógica Financiera:** Consolidación transaccional fina unificando pedidos y líneas con prorrateo logístico a nivel de ítem.

---

## Detalle de Módulos

### 📥 1. `extract.py` — Ingesta de Datos Resiliente
Carga tolerante a fallos de los archivos transaccionales de origen desde la capa de almacenamiento en disco.

*   **Entradas (`data/raw/`):** `fact_pedidos_raw.csv`, `fact_detalle_pedidos_raw.csv`, `dim_clientes_raw.csv`, `dim_productos_raw.csv`.
*   **Salidas (In-Memory DataFrames):** `pedidos_raw`, `detalle_raw`, `clientes_raw`, `productos_raw`.
*   **Enfoque de Ingeniería:** Captura excepciones de infraestructura (archivos ausentes o corruptos) evitando interrupciones abruptas del sistema, mientras documenta de forma estricta en logs el volumen exacto de registros inyectados.

📄 *Ver script de extracción:* [`/src/extract.py`](./src/extract.py)

---

### 🔍 2. `inspect.py` — Data Quality Gating & Auditoría
Módulo encargado del escaneo integral no destructivo de los *datasets* crudos previo a las fases de transformación y limpieza. Centraliza las alertas en tiempo de ejecución (*logs*) y consolida una matriz jerárquica de diagnóstico en un reporte **JSON** reproducible.

*   **Entradas:** DataFrames en memoria (`pedidos_raw`, `detalle_raw`, `clientes_raw`, `productos_raw`).
*   **Salidas:** Diccionario de diagnóstico consolidado (`quality_report.json`).

El framework de auditoría evalúa la salud de los datos a través de tres capas de control:

#### A. Calidad Técnica Estructural
*   **Espacios Anómalos por Regex:** Discriminación de espacios en bordes (*leading/trailing*) respecto a cadenas compuestas exclusivamente por espacios sin contenido (*whitespace-only*).
*   **Deduplicación Jerárquica:** Auditoría cuantitativa de colisiones en tres niveles: filas idénticas (100%), Claves Primarias (`PK`) duplicadas y Claves de Negocio (*Business Keys*).
*   **Consistencia Categórica (Case Sensitivity):** Detección de variaciones de mayúsculas y minúsculas que generan duplicidades lógicas (ej. `'Online'` vs `'online'`).
*   **Auditoría de Fechas:** Identificación de cadenas no parseables a `datetime` (`NaT`) y detección de registros anacrónicos proyectados en el futuro (`> Timestamp.now()`).

#### B. Reglas de Negocio Lógicas
*   **Validación Financiera y Descuentos:** Verificación de precios o costos inviables (`<= 0`), alerta de margen de ganancia negativo (`precio_unitario < costo_unitario`) y **auditoría de la ecuación de descuento** (`precio_lista * (1 - descuento) != precio_unitario`).
*   **Auditoría Logística de Pedidos:** Detección de cobros indebidos en pedidos cancelados o retiros en sucursal, y alerta de envíos a domicilio entregados con costo `$0`.
*   **Integridad Demográfica de Clientes:** Detección de edades imposibles (`< 0` o `> 100`), identificación de clientes menores de edad (`< 18`) y anacronismos donde la fecha de registro precede a la fecha de nacimiento.
*   **Dominio de Catálogo:** Verificación del atributo `gama` frente al conjunto restringido de valores permitidos (`alta`, `media`, `baja`).

#### C. Integridad Referencial
*   **Validación Cruzada de Claves Foráneas (`FK`):** Búsqueda eficiente en memoria mediante conjuntos (`set`) para auditar la existencia de:
    *   Pedidos vinculados a `cliente_id` inexistentes.
    *   Líneas de detalle asociadas a `producto_id` inexistentes.
    *   Líneas transaccionales huérfanas sin un `pedido_id` padre válido.

📄 *Ver script de auditoría de calidad:* [`/src/inspect.py`](./src/inspect.py)

---

### 🧼 3. `clean.py` — Sanitización, Normalización e Imputación de Datos
Módulo encargado de la corrección, imputación y neutralización de anomalías transaccionales mediante orquestadores específicos por entidad. Garantiza la calidad de datos, trazabilidad estricta vía *logs* descriptivos y minimización del descarte de registros mediante heurísticas avanzadas.

*   **Entradas:** `pedidos_raw`, `detalle_raw`, `clientes_raw`, `productos_raw` (DataFrames en memoria).
*   **Salidas:** `pedidos_clean`, `detalle_clean`, `clientes_clean`, `productos_clean` (Staging Layer).
*   **Orden de Orquestación:** Procesamiento dependiente que prioriza dimensiones (`Productos` → `Clientes`) antes de evaluar tablas de hechos (`Pedidos` → `Detalle`) para habilitar cruzamientos de integridad y contexto temporal.

#### A. Refactorización Técnica y Formatos
*   **Estandarización y Casing Semántico:** Eliminación de espacios marginales (*leading/trailing spaces*), conversión de cadenas vacías/espacios a nulos explícitos (`NA`) y formateo según el rol de la columna (`UPPERCASE` para identificadores `_id` y `Title Case` para texto descriptivo).
*   **Seguridad Cronológica:** Parseo asertivo a tipos `datetime` inyectando `NaT` ante registros corruptos o fechas anómalas en el futuro respecto a la fecha de ejecución (`now`).
*   **Deduplicación Jerárquica en 3 Capas:** Depuración algorítmica secuencial de: (1) Filas 100% idénticas, (2) Colisiones por Clave Primaria (`PK`), y (3) Registro duplicado por Claves de Negocio (*Business Keys*).

#### B. Estrategias Avanzadas de Imputación y Resiliencia
*   **Gating de Identificadores Críticos:** Descarte preventivo de registros transaccionales o dimensionales que carecen de Claves Primarias (`PK`) esenciales (`producto_id`, `cliente_id`, `pedido_id`, `detalle_id`).
*   **Saneamiento Categórico y Reconstrucción Sintética:** Imputación estandarizada de categóricos faltantes con la etiqueta `'Sin Dato'` y reconstrucción automatizada de nombres de productos ausentes combinando `marca` e `ID`.
*   **Compleción Lógica Operativa:** Asignación de valores por defecto en variables transaccionales (`cantidad = 1`, `descuento_aplicado = 0.0`).
*   **Modelado Heurístico Monetario e Inflacionario:** 
    *   **Reparación Directa:** Recálculo del `precio_unitario` a partir del `precio_lista` y `descuento_aplicado`.
    *   **Imputación Jerárquica por Mediana Temporal:** Relleno de precios y costos faltantes o invalidados (`<= 0`) mediante medianas históricas anidadas por **`[Producto / Año Fiscal]`**, utilizando como respaldo (*fallback*) la combinación **`[Categoría / Año Fiscal]`**.
    *   **Control de Pérdida Extrema:** Descarte definitivo y controlado únicamente de aquellas líneas cuyo valor monetario no pudo recuperarse tras agotar toda la cadena de *fallbacks*.

#### C. Inyección de Reglas de Negocio por Entidad
*   **Módulo Productos:** Validación del atributo `gama` contra un dominio cerrado permitido (`Alta`, `Media`, `Baja`, `Sin Dato`), reasignando desvíos a `'Sin Dato'`.
*   **Módulo Clientes:** Neutralización de fechas de nacimiento inverosímiles (edades fuera del rango 0–100 años) y rectificación automatizada de anacronismos cronológicos donde la fecha de registro era anterior a la de nacimiento.
*   **Módulo Pedidos:** Ajuste de costos logísticos forzando `$0.0` en órdenes canceladas o retiros en tienda. Para envíos a domicilio con costo incoherente (`<= 0`), se imputa la mediana agrupada por `[Año Fiscal / Tipo Envio]`.
*   **Módulo Detalle de Pedidos:** Corrección de cantidades negativas o nulas (`<= 0`), recálculo del precio neto final y generación de un **indicador binario analítico (`flag_margen_negativo`)** para alertar sobre transacciones vendidas por debajo del costo unitario.

#### D. Control de Integridad Referencial
*   **Failsafe de Clientes (Sintético `-1`):** Inyección de un registro de cliente predeterminado (*Consumidor Final*, `ID -1`) y reasignación automatizada de pedidos huérfanos hacia este ID para no perder la facturación global en el modelo analítico.
*   **Depuración en Cascada:** Eliminación de líneas de detalle que hagan referencia a órdenes de compra (`pedido_id`) o productos (`producto_id`) inexistentes en los maestros limpios.

📄 *Ver script completo de limpieza y normalización:* [`/src/clean.py`](./src/clean.py)

---

### ⚙️ 4. `transform.py` — Consolidación Dimensional y Lógica de Negocio
Módulo encargado de consolidar la tabla de hechos (`fact_pedidos_final`) integrando la cabecera de pedidos con el detalle transaccional, resolviendo el prorrateo logístico y ordenando el modelo dimensional resultante.

*   **Entradas:** DataFrames limpios (`pedidos_clean`, `detalle_clean`, `clientes_clean`, `productos_clean`).
*   **Salidas:** Tupla con DataFrames listos para ingesta `(fact_consolidada, clientes_clean, productos_clean)`.

#### A. Consolidación de Hechos y Prorrateo Logístico
*   **Conteo Vectorizado de Ítems:** Cálculo de la densidad de ítems por pedido mediante `groupby().transform('count')` sobre `detalle_clean`.
*   **Prorrateo de Envío por Línea:** Distribución equitativa del costo logístico fijo del pedido (`costo_envio / items_por_pedido`) redondeado a 2 decimales (`costo_envio_linea`). Esto permite medir el margen neto y la rentabilidad real a nivel de ítem.
*   **Desnormalización Controlada:** Selección de atributos clave de cabecera y fusión mediante `Inner Join` por `pedido_id`.

#### B. Controles de Integridad y Estructuración Final
*   **Auditoría de Registro Huérfanos:** Medición de descalce de filas pre y post *merge* (`descartados_merge`). Emite una advertencia en los *logs* si existen líneas de detalle que perdieron su cabecera durante la limpieza previa.
*   **Ordenamiento y Selección de Esquema:** Ordenamiento cronológico explícito por `fecha_pedido` y filtrado proyectado a las 16 columnas finales requeridas para la tabla de hechos, descartando atributos temporales de cálculo.
*   **Pasaje de Dimensiones:** Traspaso directo de `dim_clientes` y `dim_productos` hacia la capa de carga (`load.py`).

📄 *Ver script de transformación:* [`/src/transform.py`](./src/transform.py)

---

### 💾 5. `load.py` — Persistencia y Carga Multicapa
Módulo encargado de la exportación estructurada y segura de los DataFrames desde la memoria RAM hacia el sistema de archivos (`data/clean/` y `data/processed/`), garantizando la trazabilidad del pipeline y la preparación de archivos para su consumo analítico o ingesta en base de datos.

*   **Entradas (Memoria):** DataFrames intermedios saneados de la capa Clean y DataFrames finales del modelo dimensional.
*   **Salidas (Disco):**
    *   **Capa Staging / Clean (`data/clean/`):** `fact_pedidos_clean.csv`, `fact_detalle_pedidos_clean.csv`, `dim_clientes_clean.csv`, `dim_productos_clean.csv`.
    *   **Capa Procesada / Analytics (`data/processed/`):** `fact_pedidos_final.csv`, `dim_clientes.csv`, `dim_productos.csv`.

#### A. Arquitectura Modular y Principio DRY
*   **Función Auxiliar Privada (`_save_datasets`):** Encapsula la lógica de I/O y serialización en un único componente reutilizable, abstrayendo el guardado mediante iteración de diccionarios y etiquetado dinámico de *logs* (`layer_tag`).
*   **Gestión Autogestionada del File System:** Verificación e inicialización automática de las rutas de destino mediante `os.makedirs(..., exist_ok=True)` para prevenir fallos de ejecución por carpetas inexistentes.

#### B. Programación Defensiva y Estandarización I/O
*   **Guard Clauses contra Corrupción de Datos:** Validación previa de integridad (`if df is None or df.empty`). Si un DataFrame llega vacío o no inicializado, se cancela la escritura en disco y se emite un *warning*, evitando la sobrescritura accidental de archivos previos.
*   **Estandarización de Serialización:** Persistencia homogénea codificada en `utf-8` y omisión explícita de los índices autogenerados por Pandas (`index=False`) para garantizar una estructura tabular limpia.
*   **Observabilidad de Carga:** Registro de métricas operativas en *logs* informando la finalización exitosa del guardado junto con el conteo exacto de filas escritas por cada archivo.

📄 *Ver script de carga:* [`/src/load.py`](./src/load.py)

---

## 🛠️ `main.py` — Orquestador Central

Punto de entrada principal al pipeline. Ejecuta la secuencia ordenada de transformación (*Extract → Inspect → Clean → Save Clean → Transform → Save Processed*), gestiona el registro unificado de logs en consola y expone el reporte final de calidad en formato JSON.

*Ver script del orquesator central:* [`/main.py`](./main.py)

### Ejemplo de Ejecución

Para correr el pipeline completo desde la raíz del módulo:

```bash
# 1. Asegurar la instalación de dependencias
pip install pandas numpy

# 2. Ejecutar el orquestador principal
python main.py

```


