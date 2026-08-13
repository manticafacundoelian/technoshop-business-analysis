# TechnoShop | Investigación analítica — SQL

Esta carpeta contiene las consultas SQL utilizadas para investigar la evolución de la rentabilidad de TechnoShop y determinar los principales factores asociados a su deterioro.

### Stack técnico: ![SQL](https://img.shields.io/badge/SQL-003B57?style=flat-square&logo=sqlite&logoColor=white) ![SQLite](https://img.shields.io/badge/SQLite-003B57?style=flat-square&logo=sqlite&logoColor=white) 

---

## Flujo de investigación

La investigación sigue una secuencia progresiva, donde cada etapa profundiza el diagnóstico de la anterior:

**Evolución del negocio → Costos → Pricing → Mix → Canal → Producto**

---

## Estructura

- `00_view_fact_pedidos_analitica.sql` — Capa analítica y lógica de negocio reutilizable.
- `01_evolucion_negocio.sql` — Diagnóstico general de la evolución del negocio.
- `02_drivers_costo.sql` — Descomposición de los componentes de rentabilidad.
- `03_precio_vs_costo.sql` — Evolución del precio, costo y spread.
- `04_mix_categorias.sql` — Cambios en la composición de ventas.
- `05_canal_online_vs_fisico.sql` — Análisis de canales y presión logística.
- `06_productos_prioritarios.sql` — Identificación de productos con deterioro de rentabilidad.

---

## Capa analítica — View `fact_pedidos_analitica`

Antes de desarrollar las consultas de investigación se construyó una **View analítica** sobre `fact_pedidos_final`. Su objetivo es centralizar la lógica de negocio y métricas de rentabilidad utilizadas por los análisis posteriores.

La View:

- Filtra y clasifica la información según el **estado del pedido**, diferenciando pedidos entregados de cancelados y devueltos.
- Calcula métricas de línea reutilizables como **Revenue Bruto, Descuentos, Revenue Neto, Costo de Mercadería, Costo de Envío y Ganancia Neta Real**.
- Centraliza las reglas de cálculo para mantener consistencia entre las distintas consultas.
- Reduce la repetición de lógica en las consultas posteriores y facilita la construcción de análisis más complejos.


*Consulta SQL:* [`00_view_fact_pedidos_analitica.sql`](./00_view_fact_pedidos_analitica.sql)

---

## Investigación de rentabilidad

Con los datos procesados por el pipeline, el análisis se estructuró como una investigación progresiva, donde cada consulta responde una pregunta de negocio y habilita la siguiente.

### 1. Diagnóstico ejecutivo — ¿Qué pasó con el negocio?

Análisis anual de pedidos, Revenue Neto, Ganancia Neta Real, Margen Neto y Ticket Promedio, incorporando variaciones interanuales mediante `LAG()`.

**Hallazgo:** en 2025 los pedidos entregados crecieron un **+3,07%**, mientras el Revenue Neto cayó **-19,07%**, la Ganancia Neta Real **-57,13%** y el Margen Neto pasó de **31,90% a 16,90%**.

*Consulta SQL:* [`01_evolucion_negocio.sql`](./01_evolucion_negocio.sql)

### 2. Descomposición de rentabilidad — ¿Qué componentes deterioraron el resultado?

Desagregación de Revenue Neto, Costo de Mercadería, Costos de Envío, Pérdidas por pedidos no exitosos y Ganancia Neta Real, analizando tanto sus valores absolutos como su participación sobre el Revenue.

**Hallazgo:** el Costo de Mercadería pasó de representar el **66,07% al 78,85% del Revenue Neto**, mientras el costo logístico sobre Revenue aumentó del **1,98% al 4,13%**.

*Consulta SQL:* [`02_drivers_costo.sql`](./02_drivers_costo.sql)

### 3. Pricing — ¿Los precios acompañaron la evolución de los costos?

Comparación interanual del precio y costo promedio por producto, evitando que el volumen de ventas distorsione la evaluación de la estrategia de pricing.

**Hallazgo:** entre 2024 y 2025 el precio promedio por producto aumentó **+17,39%**, mientras el costo promedio aumentó **+45,10%**, reduciendo el spread promedio precio–costo en **35%**.

*Consulta SQL:* [`03_precio_vs_costo.sql`](./03_precio_vs_costo.sql)

### 4. Mix de ventas — ¿Cambió la composición de los productos vendidos?

Análisis de participación de unidades y Revenue por categoría, comparando 2024 vs. 2025 y complementando el análisis con Revenue por unidad y Margen Neto.

**Hallazgo:** la participación de Accesorios pasó de **73,76% a 79,89% de las unidades**, mientras Computación y Telefonía perdieron participación. El cambio de mix explica la reducción del valor promedio ponderado por unidad, pero no explica por sí solo la caída del margen, ya que todas las categorías deterioraron su rentabilidad.

*Consulta SQL:* [`04_mix_categorias.sql`](./04_mix_categorias.sql)

### 5. Canal y logística — ¿El crecimiento Online agravó la presión sobre el margen?

Comparación de Revenue, participación del canal, costos logísticos y margen entre los canales Físico y Online.

**Hallazgo:** Online pasó de representar **50,86% a 73,01% del Revenue**, mientras el costo de envío sobre Revenue aumentó de **3,90% a 5,66%**. Sin embargo, el margen también cayó en el canal Físico, por lo que la logística constituye un factor adicional y no la causa estructural principal.

*Consulta SQL:* [`05_canal_online_vs_fisico.sql`](./05_canal_online_vs_fisico.sql)

### 6. Productos prioritarios — ¿Dónde conviene intervenir?

Comparación interanual del Revenue, Ganancia Neta y Margen por producto para identificar los principales deterioros de rentabilidad y priorizar acciones comerciales.

**Hallazgo:** pendiente de completar.

*Consulta SQL:* [`06_productos_prioritarios.sql`](./06_productos_prioritarios.sql)

---

## 🛠️ Técnicas SQL aplicadas

- **CTEs (`WITH`)** para estructurar consultas complejas por etapas.
- **Window Functions** (`LAG`, `ROW_NUMBER`) para variaciones interanuales y rankings.
- **JOINs** entre tablas de hechos y dimensiones.
- **Agregaciones y métricas derivadas** para Revenue, costos, margen, mix y rentabilidad.
- **Análisis de participación** sobre unidades y Revenue.
- **Segmentación temporal, por categoría, producto y canal.**

