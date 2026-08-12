# Pipeline ETL — TechnoShop

Pipeline ETL modular desarrollado en **Python + Pandas** para transformar los datos CSV de origen en datasets limpios, consistentes y listos para su explotación analítica en SQL y Power BI.

### Stack técnico: ![Python](https://img.shields.io/badge/python-3670A0?style=flat-square&logo=python&logoColor=ffdd54) ![Pandas](https://img.shields.io/badge/pandas-%23150458.svg?style=flat-square&logo=pandas&logoColor=white) ![NumPy](https://img.shields.io/badge/numpy-013243?style=flat-square&logo=numpy&logoColor=white)

---

## 🏗️ Arquitectura del pipeline

El proceso sigue una arquitectura multicapa desacoplada (*Raw → Clean/Staging → Processed*). A continuación se detalla la organización de carpetas, la responsabilidad de cada módulo y el flujo de ejecución:

![Estructura del Pipeline](./pipeline_estructure.png)

---

## ✨ Características principales

- **Arquitectura modular y escalabilidad:** Cada etapa del proceso se encuentra desacoplada en módulos independientes y organizada mediante funciones auxiliares y orquestadores por entidad, facilitando su mantenimiento y expansión.
- **Auditoría de calidad:** Detección de anomalías técnicas, reglas de negocio e integridad referencial antes de la limpieza.
- **Trazabilidad:** Los hallazgos y las acciones aplicadas durante el proceso se registran continuamente mediante logs.
- **Reporte estructurado:** Generación de un reporte consolidado de calidad en formato JSON.
- **Reglas de negocio:** Tratamiento específico de anomalías según la naturaleza de cada entidad.
- **Estructuración de datos:** Integración de las tablas de pedidos y detalle de pedidos para generar una tabla transaccional consolidada a nivel de línea de producto.
- **Preparación analítica:** Generación de datasets procesados y estructurados para su posterior carga en la base de datos y explotación analítica.

---

## 📦 Detalle de Módulos

### 📥 `extract.py` — Ingesta de Datos 

Carga defensiva de los archivos CSV de origen desde la ruta `data/raw/`.

- **📥 Entradas (Disco - `data/raw/`):**
  - `fact_pedidos_raw.csv`
  - `fact_detalle_pedidos_raw.csv`
  - `dim_clientes_raw.csv`
  - `dim_productos_raw.csv`
- **📤 Salidas (Memoria):**
  - DataFrames en bruto: `pedidos_raw`, `detalle_raw`, `clientes_raw`, `productos_raw`.
- **⚙️ Detalle técnico:**
  - **Lectura segura (`_read_csv_safe`):** Captura fallos de infraestructura (archivos no encontrados o corruptos) evitando interrupciones abruptas de ejecución.
  - **Auditoría de volumen inicial:** Registra en logs la cantidad exacta de filas extraídas por cada entidad antes de cualquier procesamiento.

---

### 🔍 `inspect.py` — Auditoría de Calidad de Datos 

Realiza una auditoría integral de los datos antes de iniciar la limpieza. Los hallazgos se registran en terminal y se consolidan en un reporte estructurado en formato JSON.

- **📥 Entradas (Memoria):**
  - DataFrames raw (`pedidos_raw`, `detalle_raw`, `clientes_raw`, `productos_raw`).
- **📤 Salidas (Consola / JSON):**
  - Diccionario estructurado `quality_report` (impreso en consola en formato JSON).
- **⚙️ Detalle técnico:**

#### Calidad técnica
- Detección de espacios en blanco y registros compuestos únicamente por espacios.
- Identificación de valores nulos.
- Control de consistencia en variables categóricas.
- Detección de duplicados exactos.
- Detección de duplicados de claves primarias (`PK`).
- Identificación de duplicados definidos por reglas de negocio.
- Validación de fechas inválidas o no parseables.

#### Reglas de negocio
- Costos superiores al precio de venta.
- Fechas cronológicamente inconsistentes.
- Estados inválidos.
- Valores fuera de los dominios permitidos.
- Validaciones específicas según la entidad.

#### Integridad referencial
- Verificación de que las claves foráneas (`FK`) existan en sus correspondientes dimensiones (`PK`).

---

### 🧼 `clean.py` — Limpieza y Normalización de Datos 

Implementa la limpieza mediante funciones modulares y orquestadores específicos para cada entidad. Las anomalías son corregidas, imputadas, neutralizadas o descartadas según su naturaleza, manteniendo trazabilidad de las acciones realizadas.

- **📥 Entradas (Memoria):**
  - DataFrames raw (`pedidos_raw`, `detalle_raw`, `clientes_raw`, `productos_raw`).
- **📤 Salidas (Memoria):**
  - DataFrames limpios: `pedidos_clean`, `detalle_clean`, `clientes_clean`, `productos_clean`.
- **⚙️ Detalle técnico:**

#### Calidad técnica
- Eliminación de espacios en los bordes de textos.
- Conversión de cadenas vacías a valores nulos reales (`NA`).
- Normalización de formatos de texto.
- Eliminación de duplicados exactos y duplicados de claves.
- Conversión segura de fechas a `datetime`.
- Neutralización de fechas inválidas o futuras mediante `NaT`.

#### Tratamiento de valores nulos
- Descarte de registros sin claves primarias o identificadores esenciales.
- Imputación de variables categóricas con `Sin Dato`.
- Reconstrucción de nombres de productos faltantes.
- Incorporación de un cliente de contingencia con ID `-1`.
- Compleción de cantidades y descuentos faltantes.
- Reconstrucción de precios unitarios a partir de precio de lista y descuento.
- Imputación de precios y costos mediante medianas históricas por producto y año, utilizando como respaldo la categoría y año.
- Descarte de líneas cuyos valores monetarios no pueden recuperarse.

#### Reglas de negocio por entidad
- **Productos:** Validación de dominios permitidos y normalización de valores inválidos.
- **Clientes:** Tratamiento de edades y fechas de nacimiento inconsistentes.
- **Pedidos:** Normalización de costos de envío según estado y modalidad de entrega.
- **Detalle de pedidos:** Corrección de cantidades inválidas, imputación de precios/costos y recálculo del precio unitario según descuento.
- Generación de un indicador para identificar líneas con margen negativo.

#### Integridad referencial
- Reasignación de pedidos con clientes inexistentes al cliente de contingencia `-1`.
- Eliminación de líneas de detalle sin pedido padre válido.
- Eliminación de líneas asociadas a productos inexistentes.

---

### ⚙️ `transform.py` — Transformación y Consolidación de Datos 

Aplica la lógica de negocio final, prorratea costos operativos y consolida los datasets finales para el modelo analítico.

- **📥 Entradas (Memoria):**
  - DataFrames limpios (`pedidos_clean`, `detalle_clean`, `clientes_clean`, `productos_clean`).
- **📤 Salidas (Memoria):**
  - Modelo dimensional final: `fact_pedidos_final`, `clientes_clean` (como `dim_clientes`), `productos_clean` (como `dim_productos`).
- **⚙️ Detalle técnico:**

#### Principales transformaciones
- **Prorrateo del costo de envío:** Cálculo automatizado de `items_por_pedido` para prorratear equitativamente el costo de envío por cada línea transaccional (`costo_envio_linea`).
- **Consolidación transaccional:** Fusión (`Inner Join`) entre `fact_detalle_pedidos_clean` y la cabecera `fact_pedidos_clean` sobre `pedido_id`.
- **Control de integridad de merge:** Logging de advertencia si alguna línea de detalle pierde su cabecera de pedido durante la integración.
- **Hecho analítico:** Ordenamiento cronológico por `fecha_pedido` y selección estricta de columnas para generar `fact_pedidos_final` con granularidad de línea transaccional, donde cada registro representa un producto dentro de un pedido.
- **Preparación de dimensiones:** Estructuración y paso directo de los datasets maestros de clientes y productos limpios.

---

### 💾 `load.py` — Carga y Generación de Datasets Procesados

Módulo encargado de exportar los DataFrames desde la memoria hacia las carpetas correspondientes en disco.

- **📥 Entradas (Memoria):**
  - DataFrames de la capa Clean/Staging.
  - DataFrames del modelo analítico final.
- **📤 Salidas (Disco):**
  - **Capa Staging (`data/clean/`):** `fact_pedidos_clean.csv`, `fact_detalle_pedidos_clean.csv`, `dim_clientes_clean.csv`, `dim_productos_clean.csv`.
  - **Capa Procesada (`data/processed/`):** `fact_pedidos_final.csv`, `dim_clientes.csv`, `dim_productos.csv`.
- **⚙️ Detalle técnico:**
  - Funciones independientes para la persistencia de datasets Clean/Staging y Processed.
  - Control preventivo que valida el estado de cada DataFrame y evita generar o sobrescribir archivos si el dataset llega vacío o como `None`.

---

## 🛠️ `main.py` — Orquestador Central

Punto de entrada principal al pipeline. Ejecuta la secuencia ordenada de transformación (*Extract → Inspect → Clean → Save Clean → Transform → Save Processed*), gestiona el registro unificado de logs en consola y expone el reporte final de calidad en formato JSON.

### Ejemplo de Ejecución

Para correr el pipeline completo desde la raíz del módulo:

```bash
# 1. Asegurar la instalación de dependencias
pip install pandas numpy

# 2. Ejecutar el orquestador principal
python main.py
