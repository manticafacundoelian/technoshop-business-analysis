# TechnoShop | Modelado Analítico y Capa Semántica — Power BI

Este directorio contiene el modelo analítico y el reporte interactivo desarrollado en **Power BI** para la explotación de los datos procesados por el pipeline ETL, complementados con la lógica analítica desarrollada durante la investigación SQL.

El reporte implementa un modelo **dimensional basado en un Esquema en Estrella (Star Schema)** y una capa semántica construida mediante **medidas DAX**, orientada al análisis de ventas, rentabilidad, productos, canales y comportamiento de clientes.

### Stack técnico: ![Power BI](https://img.shields.io/badge/Power_BI-F2C811?style=flat-square&logo=powerbi&logoColor=black) ![DAX](https://img.shields.io/badge/DAX-Yellow?style=flat-square&logo=powerbi&logoColor=black)

---

> 📌 Los principales hallazgos y conclusiones de negocio obtenidos a partir de este reporte se presentan en el [README principal](../README.md).

---

## Modelo de Datos

El reporte implementa un **modelo dimensional basado en un Esquema en Estrella (Star Schema)**, compuesto por una tabla de hechos `fact_pedidos_final` y las dimensiones maestras `dim_clientes`, `dim_productos` y `dim_calendario`.
![Modelo de Datos](./model_view.png)

## Granularidad
La tabla de hechos presenta una **granularidad a nivel de línea transaccional (ítem de pedido)**:

> **1 fila = 1 producto dentro de un pedido.**

Esta granularidad permite analizar las transacciones desde múltiples niveles de agregación. 

Las métricas económicas derivadas no se almacenan necesariamente como columnas físicas en esta tabla; los principales indicadores de negocio se calculan dinámicamente mediante medidas DAX en la capa semántica de Power BI.

---

## Capa Semántica — Medidas DAX

Sobre el modelo dimensional se construyó una capa semántica mediante **medidas DAX**, que  permiten centralizar la lógica de cálculo de los principales indicadores favoreciendo la mantenibilidad, reutilización de la lógica y cálculo dinámico según el contexto de filtro.

Entre las principales métricas implementadas se encuentran:

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

## Estructura del Dashboard

El reporte interactivamente se organiza en **cuatro vistas analíticas**:

### 1. Vista Ejecutiva - ¿Qué pasó con el negocio?
Presenta una visión macro de la evolución del negocio, facturación y el estado de los principales KPIs de rendimiento.

![Dashboard Ejecutivo](./executive_overview.gif)

### 2. Diagnóstico de Rentabilidad - ¿Por qué cayó la rentabilidad?
Profundiza en el desglose de costos, márgenes netos y la identificación de factores clave asociados al deterioro de la rentabilidad.

![Dashboard Diagnóstico de Rentabilidad](./profitability_diagnosis.gif)

### 3. Performance de Productos - ¿Dónde conviene intervenir?
Permite analizar el desempeño económico por categorías y SKUs, identificando productos estrella y aquellos con margen negativo que requieren intervención.

![Dashboard Performance de Producto](./product_performance.gif)

### 4. Retención de Clientes - ¿Qué hacer con la base de clientes?
Analiza la salud de la base de clientes, cohortes de recompra, tasa de churn, reactivación y valor de vida del cliente (LTV).

![Dashboard Retención de Clientes](./customer_retention.gif)

---

## Validación de Datos

Las principales medidas DAX del modelo fueron contrastadas con las consultas equivalentes desarrolladas durante la etapa de investigación SQL, verificando la consistencia de los resultados entre la capa analítica y la capa de visualización.

Esta validación permitió comprobar la consistencia de los resultados considerando la granularidad transaccional, los filtros aplicados y la lógica de cálculo utilizada en cada capa.











