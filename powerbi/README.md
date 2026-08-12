# TechnoShop | Modelado Analítico y Capa Semántica - PowerBI 

Este directorio contiene el modelo analítico y el reporte desarrollado en **Power BI** para la explotación de los datos procesados por el pipeline ETL, complementados con la lógica analítica desarrollada durante la investigación SQL.

El reporte implementa un **Esquema en Estrella (Star Schema)** y una capa semántica basada en **medidas DAX**, orientada al análisis de ventas, rentabilidad, productos, canales y comportamiento de clientes.

> 📌 Los principales hallazgos y conclusiones de negocio obtenidos a partir del reporte se presentan en el [README principal](../README.md).

---

## Modelo de Datos

El modelo utiliza una estructura dimensional compuesta por una tabla de hechos: `fact_pedidos_final` y dimensiones descriptivas: `dim_clientes`, `dim_productos` y `dim_calendario`.

![Modelo de Datos](./model_view.png)

## Granularidad

La tabla de hechos presenta una **granularidad a nivel de línea de producto**:

> **1 fila = 1 producto dentro de un pedido.**

Esta granularidad permite analizar las transacciones desde distintos niveles de agregación, como pedido, cliente, producto, categoría, canal y período.

Las métricas económicas derivadas no se almacenan necesariamente como columnas físicas en esta tabla, sino que se calculan posteriormente mediante la capa semántica de Power BI.

---

## Capa Semántica — Medidas DAX

Sobre el modelo dimensional se construye una capa semántica mediante **medidas DAX**.

Las medidas permiten centralizar la lógica de cálculo de los principales indicadores y obtener resultados dinámicos según el contexto de filtros, dimensiones y visualizaciones.

Entre las principales métricas implementadas se encuentran:

### _medidas_financieras

- Revenue Bruto
- Descuentos Otorgados
- % Descuentos Otorgados
- Revenue Neto
- Ticket Promedio
- Costo Mercaderia
- % Costo Mercaderia
- Ganancia Neta Real
- % Margen Neto Real
- Promedio Costo
- Promedio Precio

### _medidas_operativas  

- Pedidos Totales
- Pedidos Entregados
- Unidades Entregadas
- Costo Envios Entregados
- % Costo Logistico Entregados
- Perdida Pedidos No Exitosos
- % Perdida Pedidos No Exitosos
- % Costo Logistico
- Pedidos Cancelados
- % Cancelaciones
- Pedidos Devueltos
- % Devoluciones

### _medidas_yoy

- % Variacion Pedidos YoY
- % Variacion Ticket Promedio YoY
- % Variacion Ganancia Neta YoY
- % Variacion Promedio Costo YoY
- % Variacion Promedio Precio YoY

### _medidas_productos 

- Total SKU
- Ganancia Neta por Unidad
- Productos Rentables
- Productos No Rentables
- Concentracion Top 5

---

## 📊 Estructura del Dashboard

El reporte se organiza en cuatro vistas principales:

### 1. Vista Ejecutiva

Presenta una visión general de la evolución del negocio y sus principales KPIs.

![Dashboard Ejecutivo](./executive_overview.gif)

### 2. Diagnóstico de Rentabilidad

Profundiza en la evolución de costos, márgenes y principales factores asociados al deterioro de la rentabilidad.

![Dashboard Diagnóstico de Rentabilidad](./profitability_diagnosis.gif)

### 3. Performance de Productos

Permite analizar el desempeño económico de categorías y productos e identificar aquellos que requieren intervención.

![Dashboard Performance de Producto](./product_performance.gif)

### 4. Retención de Clientes

Analiza la evolución de la base de clientes, retención, churn y comportamiento de compra.

![Dashboard Retención de Clientes](./customer_retention.gif)

---

## Validación

Las principales métricas del modelo fueron contrastadas con los resultados obtenidos durante la investigación SQL para garantizar consistencia entre ambas capas.


---

# TechnoShop | Modelado Analítico y Capa Semántica — Power BI

Este directorio contiene el modelo analítico y el reporte interactivo desarrollado en **Power BI** para la explotación de los datos procesados por el pipeline ETL, complementados con la lógica analítica desarrollada durante la investigación SQL.

### Stack técnico: ![Power BI](https://img.shields.io/badge/Power_BI-F2C811?style=flat-square&logo=powerbi&logoColor=black) ![DAX](https://img.shields.io/badge/DAX-Yellow?style=flat-square&logo=powerbi&logoColor=black)

> 📌 Los principales hallazgos estratégicos y conclusiones de negocio obtenidos a partir de este reporte se presentan en el [README principal](../README.md).

---

## 🏗️ Modelo de Datos

El reporte implementa un **Esquema en Estrella (Star Schema)** optimizado para análisis multidimensional. Está compuesto por una tabla de hechos central (`fact_pedidos_final`) conectada a dimensiones descriptivas maestros (`dim_clientes`, `dim_productos`) y una dimensión temporal autocreada (`dim_calendario`).

![Modelo de Datos](./model_view.png)

### Granularidad
La tabla de hechos presenta una **granularidad a nivel de línea transaccional (ítem de pedido)**:

> 💡 **1 fila = 1 producto dentro de un pedido.**

Esta granularidad permite analizar las transacciones desde múltiples niveles de agregación (pedido, cliente, producto, categoría, canal, medio de pago y período temporal). Las métricas económicas no se almacenan como columnas redundantes en disco, sino que se calculan dinámicamente mediante la capa semántica.

---

## 📐 Capa Semántica — Medidas DAX

Sobre el modelo dimensional se construyó una capa semántica organizada en **tablas dedicadas a medidas DAX**, garantizando mantenibilidad, reutilización de código y cálculo dinámico según el contexto de filtro.

### `_medidas_financieras`
- Revenue Bruto
- Descuentos Otorgados
- % Descuento Otorgado
- Revenue Neto
- Ticket Promedio
- Costo Mercaderia
- % Costo Mercaderia
- Ganancia Neta Real
- % Margen Neto Real
- Promedio Costo
- Promedio Precio

### `_medidas_operativas`
- Pedidos Totales
- Pedidos Entregados
- Unidades Entregadas
- Costo Envios Entregados
- % Costo Logistico Entregados
- Perdida Pedidos No Exitosos
- % Perdida Pedidos No Exitosos
- % Costo Logistico
- Pedidos Cancelados
- % Cancelaciones
- Pedidos Devueltos
- % Devoluciones

### `_medidas_clientes`
- % Clientes Activos
- % Clientes Perdidos
- % Clientes por Rango Dinámico
- % Clientes Recurrentes
- % Clientes Retenidos
- % Revenue Alto Valor
- Clientes Activos
- Clientes Alto Valor
- Clientes Compradores Frecuencia
- Clientes Nuevos
- Clientes Perdidos
- Clientes Reactivados
- Clientes Recurrentes
- Clientes Registrados
- Clientes Registrados Acumulados
- Clientes Retenidos
- Dias Desde Ultima Compra
- Ganancia por Cliente
- Pedidos por Cliente
- Revenue Clientes Nuevos
- Revenue Clientes Perdidos
- Revenue Clientes Reactivados
- Revenue Clientes Retenidos
- Revenue por Cliente
- Ticket Promedio por Frecuencia
- Ultima Compra Cliente

### `_medidas_productos`
- Total SKU
- Ganancia Neta por Unidad
- Productos Rentables
- Productos No Rentables
- Concentracion Top 5

### `_medidas_yoy`
- % Variacion Pedidos YoY
- % Variacion Ticket Promedio YoY
- % Variacion Ganancia Neta YoY
- % Variacion Promedio Costo YoY
- % Variacion Promedio Precio YoY

---

## 📊 Estructura del Dashboard

El reporte interactivamente se organiza en **cuatro vistas analíticas**:

### 1. Vista Ejecutiva
Presenta una visión macro de la evolución del negocio, facturación y el estado de los principales KPIs de rendimiento.

![Dashboard Ejecutivo](./executive_overview.gif)

### 2. Diagnóstico de Rentabilidad
Profundiza en el desglose de costos, márgenes netos y la identificación de factores clave asociados al deterioro de la rentabilidad.

![Dashboard Diagnóstico de Rentabilidad](./profitability_diagnosis.gif)

### 3. Performance de Productos
Permite analizar el desempeño económico por categorías y SKUs, identificando productos estrella y aquellos con margen negativo que requieren intervención.

![Dashboard Performance de Producto](./product_performance.gif)

### 4. Retención de Clientes
Analiza la salud de la base de clientes, cohortes de recompra, tasa de churn, reactivación y valor de vida del cliente (LTV).

![Dashboard Retención de Clientes](./customer_retention.gif)

---

## ✅ Validación de Datos

Todas las medidas DAX clave del modelo fueron contrastadas contra las consultas ejecutadas en la etapa de **investigación SQL**, garantizando un 100% de consistencia entre la capa de base de datos y la capa de visualización.











