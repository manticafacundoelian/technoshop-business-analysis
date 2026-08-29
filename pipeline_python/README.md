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

*   **Estructura Decoupled:** Módulos independientes orquestados por entidad mediante funciones auxiliares dedicadas.
*   **Data Quality Gating:** Auditoría preventiva exhaustiva de anomalías técnicas e integridad referencial antes de la fase de limpieza.
*   **Trazabilidad Centralizada:** Registro continuo y estructurado de hallazgos mediante un sistema dinámico de logs.
*   **Data Profiling Automatizado:** Consolidación de métricas de calidad en un reporte estructurado nativo en formato **JSON**.
*   **Inyección de Lógica Financiera:** Consolidación transaccional fina unificando pedidos y líneas con prorrateo logístico a nivel de ítem.

---

## Detalle de Módulos

### 📥 `extract.py` — Ingesta de Datos 

Carga a prueba de errores de los archivos CSV de origen desde la ruta `data/raw/`.

- **Entradas (Disco - `data/raw/`):**
  - `fact_pedidos_raw.csv`
  - `fact_detalle_pedidos_raw.csv`
  - `dim_clientes_raw.csv`
  - `dim_productos_raw.csv`
- **Salidas (Memoria):**
  - DataFrames en bruto: `pedidos_raw`, `detalle_raw`, `clientes_raw`, `productos_raw`.
- **Detalle técnico:**
  Captura fallos de infraestructura (archivos no encontrados o corruptos) evitando interrupciones abruptas de ejecución y registra en logs la cantidad exacta de filas extraídas por cada entidad.
 
*Ver script de extracción:* [`/src/extract.py`](./src/extract.py)

---

### 🔍 `inspect.py` — Auditoría de Calidad de Datos 

Realiza una auditoría integral de los datos antes de iniciar la limpieza. Los hallazgos se registran en terminal y se consolidan en un reporte estructurado en formato JSON.

- **Entradas (Memoria):**
  - DataFrames raw (`pedidos_raw`, `detalle_raw`, `clientes_raw`, `productos_raw`).
- **Salidas (Consola / JSON):**
  - Diccionario estructurado `quality_report` (impreso en consola en formato JSON).
- **Detalle técnico:**

Los datos se auditan en tres capas:

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

*Ver script de auditoría de calidad:* [`/src/inspect.py`](./src/inspect.py)

---

### 🧼 `clean.py` — Limpieza y Normalización de Datos 

Implementa la limpieza mediante funciones modulares y orquestadores específicos para cada entidad. Las anomalías son corregidas, imputadas, neutralizadas o descartadas según su naturaleza, manteniendo trazabilidad de las acciones realizadas.

- **Entradas (Memoria):**
  - DataFrames raw (`pedidos_raw`, `detalle_raw`, `clientes_raw`, `productos_raw`).
- **Salidas (Memoria):**
  - DataFrames limpios: `pedidos_clean`, `detalle_clean`, `clientes_clean`, `productos_clean`.
- **Detalle técnico:**

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

*Ver script de limpieza y normalización:* [`/src/clean.py`](./src/clean.py)

---

### ⚙️ `transform.py` — Transformación y Consolidación de Datos 

Aplica la lógica de negocio final, prorratea costos operativos y consolida los datasets finales.

- **Entradas (Memoria):**
  - DataFrames limpios (`pedidos_clean`, `detalle_clean`, `clientes_clean`, `productos_clean`).
- **Salidas (Memoria):**
  - Modelo dimensional final: `fact_pedidos_final`, `dim_clientes`, `dim_productos`.
- **Detalle técnico:**

#### Principales transformaciones
- **Prorrateo del costo de envío:** Cálculo automatizado de `items_por_pedido` para prorratear equitativamente el costo de envío por cada línea transaccional (`costo_envio_linea`).
- **Consolidación transaccional:** Fusión (`Inner Join`) entre `fact_detalle_pedidos_clean` y la cabecera `fact_pedidos_clean` sobre `pedido_id`.
- **Control de integridad de merge:** Logging de advertencia si alguna línea de detalle pierde su cabecera de pedido durante la integración.
- **tabla de hechos transaccional:** Selección de columnas para generar `fact_pedidos_final` con granularidad de línea transaccional, donde cada registro representa un producto dentro de un pedido.
- **Preparación de dimensiones:** Estructuración y paso directo de los datasets maestros de clientes y productos limpios.

*Ver script de transformación y consolidación de datos:* [`/src/transform.py`](./src/transform.py)

---

### 💾 `load.py` — Carga y Generación de Datasets Procesados

Módulo encargado de exportar los DataFrames desde la memoria hacia las carpetas correspondientes en disco.

- **Entradas (Memoria):**
  - DataFrames de la capa Clean/Staging.
  - DataFrames del modelo analítico final.
- **Salidas (Disco):**
  - **Capa Staging (`data/clean/`):** `fact_pedidos_clean.csv`, `fact_detalle_pedidos_clean.csv`, `dim_clientes_clean.csv`, `dim_productos_clean.csv`.
  - **Capa Procesada (`data/processed/`):** `fact_pedidos_final.csv`, `dim_clientes.csv`, `dim_productos.csv`.
- **Detalle técnico:**
  - Funciones independientes para la persistencia de datasets Clean/Staging y Processed.
  - Control preventivo que valida el estado de cada DataFrame y evita generar o sobrescribir archivos si el dataset llega vacío o como `None`.
 
*Ver script de carga de datasets procesados:* [`/src/load.py`](./src/load.py)

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


---

# 🐍 TechnoShop | Pipeline ETL Modular en Python

Pipeline de ingeniería de datos desarrollado con **Python, Pandas y NumPy** bajo una arquitectura modular para transformar datos transaccionales crudos en conjuntos de datos limpios, consistentes y optimizados para su explotación analítica en SQL y Power BI.

### 🛠️ Stack Técnico Principal
![Python](https://img.shields.io/badge/python-3670A0?style=flat-square&logo=python&logoColor=ffdd54) ![Pandas](https://img.shields.io/badge/pandas-%23150458.svg?style=flat-square&logo=pandas&logoColor=white) ![NumPy](https://img.shields.io/badge/numpy-013243?style=flat-square&logo=numpy&logoColor=white)

---

## 🏗️ Arquitectura del Pipeline

El sistema implementa un diseño multicapa desacoplado basado en buenas prácticas de ingeniería de software (**Raw → Clean/Staging → Processed**). La segregación de responsabilidades garantiza la mantenibilidad y escalabilidad del código.

![Estructura del Pipeline](./pipeline_estructure.png)

---

## 🚀 Características Principales

*   **Estructura Decoupled:** Módulos independientes orquestados por entidad mediante funciones auxiliares dedicadas.
*   **Data Quality Gating:** Auditoría preventiva exhaustiva de anomalías técnicas e integridad referencial antes de la fase de limpieza.
*   **Trazabilidad Centralizada:** Registro continuo y estructurado de hallazgos mediante un sistema dinámico de logs.
*   **Data Profiling Automatizado:** Consolidación de métricas de calidad en un reporte estructurado nativo en formato **JSON**.
*   **Inyección de Lógica Financiera:** Consolidación transaccional fina unificando pedidos y líneas con prorrateo logístico a nivel de ítem.

---

## 🛠️ Detalle de Módulos Técnicos

### 📥 1. `extract.py` — Ingesta de Datos Resiliente
Carga tolerante a fallos de los archivos transaccionales de origen desde la capa de almacenamiento en disco.

*   **Entradas (`data/raw/`):** `fact_pedidos_raw.csv`, `fact_detalle_pedidos_raw.csv`, `dim_clientes_raw.csv`, `dim_productos_raw.csv`.
*   **Salidas (In-Memory DataFrames):** `pedidos_raw`, `detalle_raw`, `clientes_raw`, `productos_raw`.
*   **Enfoque de Ingeniería:** Captura excepciones de infraestructura (archivos ausentes o corruptos) evitando interrupciones abruptas del sistema, mientras documenta de forma estricta en logs el volumen exacto de registros inyectados.

📄 *Ver script de extracción:* [`/src/extract.py`](./src/extract.py)

---

### 🔍 2. `inspect.py` — Data Quality Gating & Auditoría
Módulo encargado del escaneo integral de los datasets antes de la transformación. Centraliza los hallazgos en la salida estándar y genera una firma de calidad reproducible en **JSON**.

*   **Entradas:** DataFrames en memoria (`pedidos_raw`, `detalle_raw`, `clientes_raw`, `productos_raw`).
*   **Salidas:** Reporte consolidado estructurado (`quality_report.json`).

El framework de auditoría evalúa tres capas críticas:

#### A. Calidad Técnica Estructural
*   Detección exhaustiva de strings vacíos, espacios en blanco y registros nulos (`NaN`).
*   Validación de consistencia en dominios de variables categóricas.
*   Identificación de colisiones y duplicados de Claves Primarias (`PK`) y duplicados exactos de registros.
*   Validación automatizada de formatos cronológicos inválidos o no parseables.

#### B. Reglas de Negocio Lógicas
*   Auditoría de anomalías comerciales (costos unitarios superiores al precio de venta).
*   Validación de consistencia en secuencias lógicas de fechas y estados de órdenes.
*   Control de rangos y valores fuera de los límites de negocio permitidos.

#### C. Integridad Referencial
*   Validación cruzada de Claves Foráneas (`FK`) contra Claves Primarias (`PK`) de las dimensiones para prevenir registros huérfanos.

💡 *Ejemplo de estructura de salida del reporte de auditoría:*
```json
{
  "timestamp": "2026-08-28T21:41:00",
  "entity": "fact_pedidos",
  "metrics": {
    "total_records": 1500,
    "null_values": { "customer_id": 0, "order_date": 3 },
    "duplicate_pks": 0,
    "business_rule_violations": { "cost_greater_than_price": 12 }
  }
}
```

📄 *Ver script de auditoría de calidad:* [`/src/inspect.py`](./src/inspect.py)

### 🧼 3. `clean.py` — Sanitización y Normalización de Datos
Módulo encargado de la corrección, imputación y neutralización de anomalías mediante orquestadores y funciones modulares específicas por entidad, garantizando la trazabilidad estricta en logs.

*   **Entradas:** `pedidos_raw`, `detalle_raw`, `clientes_raw`, `productos_raw` (In-Memory).
*   **Salidas:** `pedidos_clean`, `detalle_clean`, `clientes_clean`, `productos_clean` (Layer Staging).

El proceso de limpieza implementa técnicas robustas en cuatro dimensiones:

#### A. Refactorización Técnica y Formatos
*   **Normalización Estructural:** Eliminación de *leading/trailing spaces* y conversión de strings vacíos a nulos reales (`NaN`).
*   **Seguridad Cronológica:** Conversión asertiva a tipos `datetime` inyectando `NaT` ante datos futuros o fechas inválidas.
*   **Deduplicación:** Eliminación algorítmica de duplicados exactos y colisiones en llaves de negocio.

#### B. Estrategias Avanzadas de Imputación de Nulos
*   **Gating de Identificadores:** Descarte inmediato de registros huérfanos sin Clave Primaria (`PK`) válida.
*   **Failsafe de Dimensiones:** Implementación de registros de contingencia de negocio (Inyección de un *Default Client* con ID `-1`).
*   **Modelado Heurístico Monetario:** Reconstrucción de precios unitarios mediante spread de lista/descuento e imputación predictiva de precios y costos utilizando **medianas históricas anidadas por Producto/Año y Categoría/Año**.

#### C. Control Avanzado de Integridad Referencial
*   **Limpieza en Cascada:** Eliminación de líneas de detalle huérfanas sin pedido padre o asociadas a productos inexistentes en el maestro.
*   **Reasignación de Negocio:** Derivación de pedidos con clientes inválidos hacia el ID de contingencia `-1`.

📄 *Ver script de limpieza:* [`/src/clean.py`](./src/clean.py)

---

### ⚙️ 4. `transform.py` — Consolidación Dimensional y Lógica de Negocio
Aplica el procesamiento analítico final, resuelve cálculos operativos distribuidos y consolida las estructuras de destino.

*   **Entradas:** DataFrames en capa Clean/Staging en memoria.
*   **Salidas:** Tablas finales optimizadas para el Data Warehouse (`fact_pedidos_final`, `dim_clientes`, `dim_productos`).

*   **Prorrateo Logístico Distribuido:** Cálculo dinámico de la densidad de ítems por orden para prorratear de manera equitativa el costo de envío fijo a nivel de línea transaccional (`costo_envio_linea`).
*   **Consolidación de Hechos (Fact Denormalization):** Ejecución de un `Inner Join` controlado entre detalles y cabeceras mediante `pedido_id` para establecer una **granularidad atómica a nivel de ítem**.
*   **Failsafe de Integración:** Sistema de logging preventivo que emite alertas críticas si alguna línea transaccional pierde su cabecera de pedido durante el merge.

📄 *Ver script de transformación:* [`/src/transform.py`](./src/transform.py)

---

### 💾 5. `load.py` — Persistencia y Generación de Capas
Módulo responsable de escribir y materializar los DataFrames desde la memoria hacia estructuras físicas en disco de manera desacoplada.

*   **Entradas:** DataFrames procesados e intermedios.
*   **Salidas (Persistencia física):**
    *   **Capa Staging (`data/clean/`):** Almacenamiento seguro de estructuras intermedias sanitizadas.
    *   **Capa Procesada (`data/processed/`):** Almacenamiento optimizado de tablas listas para explotación analítica.
*   **Mecanismo de Control:** Implementación de guardas lógicas (*guard clauses*) que bloquean la escritura o sobrescritura de archivos si un dataset llega vacío o como `None`.

📄 *Ver script de carga:* [`/src/load.py`](./src/load.py)

---

## 🎛️ 6. `main.py` — Orquestador Central del Pipeline

Punto de entrada (*Entry Point*) principal del sistema. Controla y secuencia el flujo lógico completo de la arquitectura (**Extract ➔ Inspect ➔ Clean ➔ Save Clean ➔ Transform ➔ Save Processed**), centralizando el flujo de logs en tiempo real y exponiendo el reporte JSON de calidad.

📄 *Ver orquestador principal:* [`/main.py`](./main.py)

### 🚀 Guía de Despliegue y Ejecución

Para inicializar y ejecutar el pipeline completo desde la raíz del módulo:

```bash
# 1. Instalar el stack de dependencias requeridas
pip install pandas numpy

# 2. Ejecutar el pipeline de datos
python main.py
```


