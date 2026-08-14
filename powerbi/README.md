# TechnoShop | Modelo Semántico y Reporte — Power BI

Este directorio contiene el modelo semántico y el reporte interactivo desarrollado en Power BI sobre los datos procesados por el pipeline ETL.

### Stack técnico: ![Power BI](https://img.shields.io/badge/Power_BI-F2C811?style=flat-square&logo=powerbi&logoColor=black) ![DAX](https://img.shields.io/badge/DAX-Yellow?style=flat-square&logo=powerbi&logoColor=black)

---

> 📌 Los principales hallazgos y conclusiones de negocio obtenidos a partir de este reporte se presentan en el [README principal](../README.md).

---

## Modelo de Datos

El reporte implementa un **modelo dimensional basado en un Esquema en Estrella (Star Schema)**, compuesto por una tabla de hechos `fact_pedidos_final` y las dimensiones maestras `dim_clientes`, `dim_productos` y `dim_calendario`.  

![Modelo de Datos](./model_view.png)

## Granularidad

La tabla de hechos conserva una **granularidad a nivel de línea transaccional (ítem de pedido)**:

> **1 fila = 1 producto dentro de un pedido.**

---

## Capa Semántica — Medidas DAX

Sobre el modelo dimensional se construyó una capa semántica mediante **medidas DAX**. Estas medidas centralizan la lógica de cálculo de los principales indicadores, favoreciendo su mantenibilidad y reutilización, y permitiendo cálculos dinámicos según el contexto de filtro.

Entre las principales métricas implementadas se encuentran:

#### `_medidas_financieras`
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

#### `_medidas_operativas`
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

#### `_medidas_clientes`
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

#### `_medidas_productos`
- Total SKU
- Ganancia Neta por Unidad
- Productos Rentables
- Productos No Rentables
- Concentracion Top 5

#### `_medidas_yoy`
- % Variacion Pedidos YoY
- % Variacion Ticket Promedio YoY
- % Variacion Ganancia Neta YoY
- % Variacion Promedio Costo YoY
- % Variacion Promedio Precio YoY

---

## Estructura del Dashboard

El reporte interactivo se organiza en cuatro vistas analíticas:

### 1. Vista Ejecutiva - ¿Qué pasó con el negocio?
Presenta una visión macro de la evolución del negocio, facturación y el estado de los principales KPIs de rendimiento.

![Dashboard Ejecutivo](./vista_ejecutiva.gif)

### 2. Diagnóstico de Rentabilidad - ¿Por qué cayó la rentabilidad?
Profundiza en el desglose de costos, márgenes netos y la identificación de factores clave asociados al deterioro de la rentabilidad.

![Dashboard Diagnóstico de Rentabilidad](./diagnostico_rentabilidad.gif)

### 3. Performance de Productos - ¿Dónde conviene intervenir?
Permite analizar el desempeño económico por categorías y SKUs, identificando productos estrella y aquellos con margen negativo que requieren intervención.

![Dashboard Performance de Producto](./performance_productos.gif)

### 4. Retención de Clientes - ¿Qué hacer con la base de clientes?
Analiza la salud de la base de clientes, cohortes de recompra, tasa de churn, reactivación.

![Dashboard Retención de Clientes](./retencion_clientes.gif)

---

## Validación de Datos

Las principales medidas DAX del modelo fueron contrastadas con las consultas equivalentes desarrolladas durante la investigación SQL, verificando la consistencia de los resultados entre SQL y Power BI.













