# Power BI — Modelo Analítico y Dashboard

Este directorio contiene el modelo analítico y el reporte desarrollado en **Power BI** para la explotación de los datos procesados por el pipeline ETL y enriquecidos mediante la capa analítica SQL.

El reporte implementa un **Esquema en Estrella (Star Schema)** y una capa semántica basada en **medidas DAX**, orientada al análisis de ventas, rentabilidad, productos, canales y comportamiento de clientes.

> 📌 Los principales hallazgos y conclusiones de negocio obtenidos a partir del reporte se presentan en el [README principal](../README.md).

---

## 📐 Modelo de Datos

El modelo utiliza una estructura dimensional compuesta por una tabla de hechos y dimensiones descriptivas.

![Modelo de Datos](./model_view.png)

### ⭐ Tabla de hechos

**`fact_pedidos_final`**

La tabla de hechos presenta una **granularidad a nivel de línea de producto**:

> **1 fila = 1 producto dentro de un pedido.**

Esta granularidad permite analizar las transacciones desde distintos niveles de agregación, como pedido, cliente, producto, categoría, canal y período.

Entre los principales atributos utilizados se encuentran:

- Identificador del pedido.
- Identificador del cliente.
- Identificador del producto.
- Fecha del pedido.
- Cantidad.
- Precio unitario.
- Descuento.
- Costo de mercadería.
- Costo de envío prorrateado.
- Canal de venta.
- Estado del pedido.
- Otros atributos transaccionales necesarios para el análisis.

Las métricas económicas derivadas no se almacenan necesariamente como columnas físicas en esta tabla, sino que se calculan posteriormente mediante la capa semántica de Power BI.

### 👤 `dim_clientes`

Contiene los atributos descriptivos necesarios para analizar el comportamiento de los clientes.

Permite segmentar el análisis por variables como:

- Cliente.
- Ubicación.
- Segmentos de clientes.
- Características demográficas disponibles.
- Otras dimensiones descriptivas.

### 📦 `dim_productos`

Contiene la información descriptiva del catálogo.

Permite analizar:

- Producto.
- Categoría.
- Precio de lista.
- Costos.
- Clasificación de productos.
- Otras características del catálogo.

### 📅 `dim_calendario`

Dimensión temporal utilizada para los análisis de evolución y comparación entre períodos.

Permite trabajar con:

- Año.
- Mes.
- Trimestre.
- Períodos comparables.
- Variaciones interanuales (YoY).

La utilización de una dimensión calendario independiente permite centralizar la lógica temporal y mantener consistencia en las medidas DAX.

---

## 🔗 Relaciones del Modelo

El modelo sigue una estructura de tipo **Star Schema**, donde la tabla de hechos ocupa el centro y las dimensiones proporcionan el contexto analítico.

```text
                    dim_clientes
                         │
                         │
                         ▼
                    ┌─────────────┐
                    │             │
                    │ fact_pedidos│
                    │    _final   │
                    │             │
                    └─────────────┘
                         ▲
                         │
             ┌───────────┴───────────┐
             │                       │
             │                       │
      dim_productos          dim_calendario

[Descargar / abrir el archivo Power BI](./Technoshop.pbix)
