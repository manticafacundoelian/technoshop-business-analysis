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

## 📐 Capa analítica — View `fact_pedidos_analitica`

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

### 4. Análisis del Mix de Ventas — ¿La composición del catálogo alteró la rentabilidad ponderada?
Evaluación del market share interno de cada categoría analizando variaciones cruzadas de posicionamiento en unidades físicas, facturación y su impacto directo en el margen neto final.
*   **Enfoque Técnico:** Construcción de un pipeline relacional mediante tres CTEs anidados (`categoria_anual` ➔ `totales` ➔ `mix`) para calcular cuotas relativas, complementado con técnicas avanzadas de **pivoteo dinámico por agregación condicional (`MAX(CASE WHEN`)** para aislar deltas interanuales en puntos porcentuales (p.p.).
*   **Insight de Negocio:** La categoría *Accesorios* expandió agresivamente su share operativo al saltar del **73.76% al 79.89% de las unidades totales** (+6.13 p.p.), desplazando a categorías core de alto valor como *Computación* y *Telefonía*. Si bien esta sustitución explica mecánicamente la caída del ingreso medio por unidad vendida (`delta_revenue_por_unidad`), la consulta demuestra que el problema real es estructural y no solo de mezcla: **todas las categorías experimentaron una fuerte compresión individual en sus deltas de margen (`delta_margen_pp`)**, inhabilitando el mix de productos como justificación única de la crisis.
*   📄 *Consulta SQL:* [`04_mix_categorias.sql`](./04_mix_categorias.sql)

### 5. Análisis de Canales y Distribución — ¿El crecimiento Online agravó la presión sobre el margen?
Segmentación analítica bivariada para evaluar la performance transaccional y el impacto de los costos de envío cruzando el desempeño de los canales Físico y Online.
*   **Enfoque Técnico:** Uso combinado de agregaciones condicionales y funciones de ventana con partición temporal (**`SUM() OVER (PARTITION BY anio)`**) para calcular la cuota de mercado por canal (*Share de Revenue*), integrado con una matriz final de pivoteo para calcular tasas de variación horizontal interanual (`var_revenue_yoy_pct`).
*   **Insight de Negocio:** El canal Online experimentó una migración masiva de la demanda, escalando del **50.86% al 73.01% del share de facturación** global (+22.15 p.p.). Sin embargo, esta expansión de volumen incrementó la presión sobre el margen debido a que el costo de envío sobre ventas en el canal digital aumentó del **3.90% al 5.66%**. La consulta confirma que la logística actuó como un fuerte catalizador de la caída de rentabilidad, pero no como la causa raíz única, dado que el canal Físico también sufrió una severa contracción en su delta de margen (`delta_margen_pp`).
*   📄 *Consulta SQL:* [`05_canal_online_vs_fisico.sql`](./05_canal_online_vs_fisico.sql)

### 6. Auditoría de SKUs Críticos — ¿Dónde se debe intervenir quirúrgicamente?
Identificación atómica de los productos específicos que lideran la destrucción de valor monetario interanual para priorizar acciones de saneamiento en el catálogo.
*   **Enfoque Técnico:** Implementación de un **Self-Join indexado y condicional** sobre un CTE intermedio (`producto_anual`) para alinear métricas anuales cruzadas, ordenando los resultados de forma ascendente para aislar de manera exacta las mayores caídas en valor absoluto (`delta_ganancia`).
*   **Insight de Negocio:** La consulta expone una alarmante dispersión interna en el catálogo. Identifica críticamente una lista de **5 productos con margen neto negativo inferior al 0% en la operación digital**, liderados por el *Organizador de Cables* (-$92) y el *Limpiador de Pantallas* (-$64). El hallazgo comprueba que, bajo el esquema actual de costos, el impacto del costo de envío fijo convierte automáticamente a los artículos de bajo valor unitario en operaciones deficitarias para la compañía, independientemente del volumen vendido.
*   📄 *Consulta SQL:* [`06_productos_prioritarios.sql`](./06_productos_prioritarios.sql)

---

## 🛠️ Técnicas y Funciones SQL Explotadas

*   **Common Table Expressions (CTEs):** Segmentación de consultas complejas en capas lógicas modulares y legibles.
*   **Analíticas de Ventana (`LAG`, `ROW_NUMBER`):** Auditoría secuencial YoY e identificación precisa de posiciones extremas en rankings.
*   **Álgebra de Joins Controlada:** Integraciones relacionales estrictas entre hechos lógicos y tablas dimensionales maestras.
*   **Agregaciones Financieras Avanzadas:** Funciones numéricas combinadas para derivar variables complejas de participación, márgenes y spreads indexados.

