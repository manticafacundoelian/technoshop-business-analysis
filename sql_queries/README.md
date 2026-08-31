# 🛢️ TechnoShop | Investigación Analítica Avanzada en SQL

Este módulo contiene el repositorio de scripts lógicos y consultas estructuradas en SQL diseñadas para diagnosticar la evolución de la rentabilidad de TechnoShop, aislar los componentes de fuga de valor y determinar los factores macro y micro detrás de la contracción del margen neto.

### Stack Técnico Principal: ![SQL](https://img.shields.io/badge/SQL-003B57?style=flat-square&logo=sqlite&logoColor=white) ![SQLite](https://img.shields.io/badge/SQLite-003B57?style=flat-square&logo=sqlite&logoColor=white) 

---

## 🗺️ Framework Secuencial de Investigación

El proceso analítico se diseñó bajo una metodología iterativa y progresiva. Cada consulta actúa como un nivel de granularidad más profundo que responde a una hipótesis de negocio e inicializa la etapa siguiente:

```text
📊 Evolución del Negocio  ➔  📉 Drivers de Costo  ➔  🏷️ Estrategia de Pricing
                                                               │
┌──────────────────────────────────────────────────────────────┘
▼
📦 Mix de Categorías       ➔  🚚 Logística y Canales ➔  🎯 SKUs y Productos Críticos
```

---

## 📂 Arquitectura del Repositorio

*   **`00_view_fact_pedidos_analitica.sql`** — Capa analítica intermedia y centralización de la lógica de negocio.
*   **`01_evolucion_negocio.sql`** — Análisis macro y auditoría de variaciones interanuales (YoY).
*   **`02_drivers_costo.sql`** — Descomposición vertical y participación de la estructura de costos sobre el revenue.
*   **`03_precio_vs_costo.sql`** — Evaluación del spread marginal e impacto de las estrategias de pricing unitario.
*   **`04_mix_categorias.sql`** — Análisis del mix de cartera y efectos de sustitución de volumen ponderado.
*   **`05_canal_online_vs_fisico.sql`** — Evaluación cruzada de performance transaccional y presión de costos de última milla.
*   **`06_productos_prioritarios.sql`** — Identificación analítica de SKUs críticos para priorización de intervención comercial.

---

## Capa analítica — View `fact_pedidos_analitica`

Como paso previo a la fase de investigación, se construyó una **Vista Analítica** sobre la tabla optimizada `fact_pedidos_final`. Este componente actúa como una capa de transformación lógica reutilizable encargada de centralizar las reglas financieras del negocio.

La View:

*   **Gating Transaccional:** Homogeneiza el universo de análisis aislando las órdenes efectivamente entregadas de los estados de cancelación o devolución.
*   **Cálculo Atómico de Métricas:** Consolida a nivel de línea las variables base para reportabilidad: **Revenue Bruto, Descuentos Otorgados, Revenue Neto, Costo de Mercadería, Costo de Envío y Ganancia Neta Real**.
*   **Single Source of Truth:** Centraliza las ecuaciones eliminando redundancias de código en los scripts secundarios y blindando la consistencia métrica.

📄 *Ver definición de la vista:* [`00_view_fact_pedidos_analitica.sql`](./00_view_fact_pedidos_analitica.sql)

---

## 🔎 Ejecución de la Investigación de Rentabilidad

### 1. Diagnóstico Ejecutivo — ¿Qué pasó macroeconómicamente con el negocio?
Análisis temporal interanual enfocado en el volumen operativo, ingresos netos, rentabilidad real y ticket medio por orden.
*   **Enfoque Técnico:** Implementación de funciones de desfase **`LAG()`** para auditorías de variación interanual (YoY).
*   **Insight de Negocio:** Al cierre de 2025, a pesar de una expansión del **+3.07%** en órdenes entregadas (1,478 vs. 1,434), el Revenue Neto se contrajo un **-19.07%** y la Ganancia Neta Real colapsó un **-57.13%**, reduciendo el margen neto general del **31.90% al 16.90%**.
*   📄 *Consulta SQL:* [`01_evolucion_negocio.sql`](./01_evolucion_negocio.sql)

### 2. Descomposición de Costos — ¿Qué elementos pulverizaron el resultado operativo?
Evaluación de la estructura interna del P&L analizando la participación de cada costo sobre el ingreso neto final.
*   **Enfoque Técnico:** Implementación de Análisis Vertical combinado con variaciones interanuales (YoY) mediante **`LAG()`** sobre múltiples métricas monetarias en simultáneo.
*   **Insight de Negocio:** El **Costo de Mercadería absorbió el margen al escalar del 66.07% al 78.85% del Revenue Neto** (+12.78 p.p.), mientras que el costo de envío sobre ventas se duplicó, pasando del **1.98% al 4.13%**. El resto de las pérdidas operativas se mantuvieron en niveles mínimos.
*   📄 *Consulta SQL:* [`02_drivers_costo.sql`](./02_drivers_costo.sql)

### 3. Estrategia de Pricing — ¿Los precios acompañaron la aceleración de los costos?
Auditoría del comportamiento indexado de precios frente a costos a nivel unitario de producto para evaluar la elasticidad y la contracción del spread.
*   **Enfoque Técnico:** Implementación de un modelo de doble agregación anidada mediante CTEs para aislar el promedio macro por producto, mitigando sesgos por distorsión de volumen masivo (Análisis No Ponderado).
*   **Insight de Negocio:** Entre 2024 y 2025, el precio promedio por producto aumentó un **+17.39%**, mientras que el costo promedio se disparó un **+45.10%**. Esta asimetría redujo el spread promedio precio-costo en un **-35%**, confirmando una deficiente política de fijación de precios frente al avance de los costos de los proveedores.
*   📄 *Consulta SQL:* [`03_precio_vs_costo.sql`](./03_precio_vs_costo.sql)

### 4. Mix de ventas — ¿Cambió la composición de los productos vendidos?

Análisis de participación de unidades y Revenue por categoría, comparando 2024 vs. 2025 y complementando el análisis con Revenue por unidad y Margen Neto.

**Hallazgo:** la participación de Accesorios pasó de **73,76% a 79,89% de las unidades**, mientras Computación y Telefonía perdieron participación. El cambio de mix explica la reducción del valor promedio ponderado por unidad, pero no explica por sí solo la caída del margen, ya que todas las categorías deterioraron su rentabilidad.

📄 *Consulta SQL:* [`04_mix_categorias.sql`](./04_mix_categorias.sql)

### 5. Canal y logística — ¿El crecimiento Online agravó la presión sobre el margen?

Comparación de Revenue, participación del canal, costos logísticos y margen entre los canales Físico y Online.

**Hallazgo:** Online pasó de representar **50,86% a 73,01% del Revenue**, mientras el costo de envío sobre Revenue aumentó de **3,90% a 5,66%**. Sin embargo, el margen también cayó en el canal Físico, por lo que la logística constituye un factor adicional y no la causa estructural principal.

📄 *Consulta SQL:* [`05_canal_online_vs_fisico.sql`](./05_canal_online_vs_fisico.sql)

### 6. Productos prioritarios — ¿Dónde conviene intervenir?

Comparación interanual del Revenue, Ganancia Neta y Margen por producto para identificar los principales deterioros de rentabilidad y priorizar acciones comerciales.

**Hallazgo:** pendiente de completar.

📄 *Consulta SQL:* [`06_productos_prioritarios.sql`](./06_productos_prioritarios.sql)

---

## 🛠️ Técnicas SQL aplicadas

- **CTEs (`WITH`)** para estructurar consultas complejas por etapas.
- **Window Functions** (`LAG`, `ROW_NUMBER`) para variaciones interanuales y rankings.
- **JOINs** entre tablas de hechos y dimensiones.
- **Agregaciones y métricas derivadas** para Revenue, costos, margen, mix y rentabilidad.
- **Análisis de participación** sobre unidades y Revenue.
- **Segmentación temporal, por categoría, producto y canal.**

