# Pipeline ETL — TechnoShop

Pipeline ETL modular desarrollado en **Python + Pandas** para transformar los datos CSV de origen en datasets limpios, consistentes y listos para su explotación analítica en SQL y Power BI.

### Stack técnico: ![Python](https://img.shields.io/badge/python-3670A0?style=flat-square&logo=python&logoColor=ffdd54) ![Pandas](https://img.shields.io/badge/pandas-%23150458.svg?style=flat-square&logo=pandas&logoColor=white) ![NumPy](https://img.shields.io/badge/numpy-013243?style=flat-square&logo=numpy&logoColor=white)

---

## Arquitectura del pipeline

![Estructura del Pipeline](./pipeline_estructure.png)


## Características principales

- **Arquitectura modular y escalabilidad:** cada etapa del proceso se encuentra desacoplada en módulos independientes y organizada mediante funciones auxiliares y orquestadores por entidad facilitando su mantenimiento y expansión.
- **Auditoría de calidad:** detección de anomalías técnicas, reglas de negocio e integridad referencial antes de la limpieza.
- **Trazabilidad:** los hallazgos y las acciones aplicadas durante el proceso se registran mediante logs.
- **Reporte estructurado:** generación de un reporte consolidado de calidad en formato JSON.
- **Reglas de negocio:** tratamiento específico de anomalías según la naturaleza de cada entidad.
- **Preparación analítica:** generación de datasets procesados y estructurados para su posterior análisis.

---

## 🔍 `inspect.py` — Auditoría de Calidad de Datos

Realiza una auditoría integral de los datos antes de iniciar la limpieza.

Los hallazgos se registran en terminal y se consolidan en un reporte estructurado en formato JSON.

### Calidad técnica

- Detección de espacios en blanco y registros compuestos únicamente por espacios.
- Identificación de valores nulos.
- Control de consistencia en variables categóricas.
- Detección de duplicados exactos.
- Detección de duplicados de claves primarias (`PK`).
- Identificación de duplicados definidos por reglas de negocio.
- Validación de fechas inválidas o no parseables.

### Reglas de negocio

- Costos superiores al precio de venta.
- Fechas cronológicamente inconsistentes.
- Estados inválidos.
- Valores fuera de los dominios permitidos.
- Validaciones específicas según la entidad.

### Integridad referencial

- Verificación de que las claves foráneas (`FK`) existan en sus correspondientes dimensiones (`PK`).

---

## 🧼 `clean.py` — Limpieza y Normalización

Implementa la limpieza mediante funciones modulares y orquestadores específicos para cada entidad.

Las anomalías son corregidas, imputadas, neutralizadas o descartadas según su naturaleza, manteniendo trazabilidad de las acciones realizadas.

### Calidad técnica

- Eliminación de espacios en los bordes de textos.
- Conversión de cadenas vacías a valores nulos reales (`NA`).
- Normalización de formatos de texto.
- Eliminación de duplicados exactos y duplicados de claves.
- Conversión segura de fechas a `datetime`.
- Neutralización de fechas inválidas o futuras mediante `NaT`.

### Tratamiento de valores nulos

- Descarte de registros sin claves primarias o identificadores esenciales.
- Imputación de variables categóricas con `Sin Dato`.
- Reconstrucción de nombres de productos faltantes.
- Incorporación de un cliente de contingencia con ID `-1`.
- Compleción de cantidades y descuentos faltantes.
- Reconstrucción de precios unitarios a partir de precio de lista y descuento.
- Imputación de precios y costos mediante medianas históricas por producto y año, utilizando como respaldo la categoría y año.
- Descarte de líneas cuyos valores monetarios no pueden recuperarse.

### Reglas de negocio por entidad

- **Productos:** validación de dominios permitidos y normalización de valores inválidos.
- **Clientes:** tratamiento de edades y fechas de nacimiento inconsistentes.
- **Pedidos:** normalización de costos de envío según estado y modalidad de entrega.
- **Detalle de pedidos:** corrección de cantidades inválidas, imputación de precios/costos y recálculo del precio unitario según descuento.
- Generación de un indicador para identificar líneas con margen negativo.

### Integridad referencial

- Reasignación de pedidos con clientes inexistentes al cliente de contingencia `-1`.
- Eliminación de líneas de detalle sin pedido padre válido.
- Eliminación de líneas asociadas a productos inexistentes.

---

## ⚙️ `transform.py` — Transformación y Consolidación

Aplica la lógica de negocio final y prepara los datasets para el análisis.

### Principales transformaciones

- **Consolidación transaccional:** combina mediante `merge` las tablas limpias de `fact_pedidos` y `fact_detalle_pedidos`.
- **Hecho analítico:** genera `fact_pedidos_final` a nivel de línea transaccional.
- **Preparación de dimensiones:** estructura los datasets maestros de clientes y productos para su posterior utilización en el modelo analítico.

---

## 🚀 `load.py` — Carga y generación de datasets procesados

Ejecuta la etapa final del pipeline y exporta los datasets transformados hacia:

```text
data/processed/



