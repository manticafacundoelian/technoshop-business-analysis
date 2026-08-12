# Technoshop | Análisis de Negocio End-to-End

### Introducción:  
Este proyecto abarca el ciclo completo de un proceso de analítica de datos: desde la construcción de un **pipeline ETL modular en Python**, pasando por la **investigación analítica en SQL**, hasta la elaboración de un **dashboard interactivo en Power BI**, a partir del cual se obtienen conclusiones y recomendaciones estratégicas.  

Para priorizar la perspectiva de negocio, este README presenta primero los hallazgos, el impacto y las recomendaciones, y posteriormente la arquitectura técnica que permitió obtenerlos.

### Objetivo: 
Identificar las causas raíz de la caída de rentabilidad de una empresa de retail tecnológico entre 2023 y 2025 y elaborar recomendaciones estratégicas basadas en evidencia para apoyar la toma de decisiones.

### Stack Técnico Principal:  
![Python](https://img.shields.io/badge/python-3670A0?style=flat-square&logo=python&logoColor=ffdd54) ![Pandas](https://img.shields.io/badge/pandas-%23150458.svg?style=flat-square&logo=pandas&logoColor=white) ![NumPy](https://img.shields.io/badge/numpy-013243?style=flat-square&logo=numpy&logoColor=white) ![SQL](https://img.shields.io/badge/sql-%2300758F.svg?style=flat-square&logo=sqlite&logoColor=white) ![Power BI](https://img.shields.io/badge/Power_BI-F2C811?style=flat-square&logo=powerbi&logoColor=black)  

---

## Problema de Negocio

Si bien el volumen de pedidos se mantiene relativamente estable, el negocio experimenta una fuerte destrucción de valor: la **Ganancia Neta** se derrumbó un **-57.13%**.  

## Storytelling de Negocio — Hallazgos del Análisis en Power BI
<details>
<summary><b>1. Vista Ejecutiva — ¿Qué pasó con el negocio? (Clic para expandir)</b></summary><br>

Al cierre del año fiscal 2025, el volumen operativo general se mantiene relativamente estable, con un incremento del **+3,07%** en los pedidos entregados (**1.478 vs. 1.434** del período anterior). Sin embargo, la **Ganancia Neta** global se derrumbó un **-57,13%**, pasando de **$169.402 a $72.627**, mientras que el **Margen Neto** se redujo casi a la mitad, cerrando en **16,90%**.

Este deterioro presenta **dinámicas opuestas entre canales**:

* El **Canal Físico** sufrió una contracción del **-71,69% en su Ganancia Neta** (**$87.136 vs. $24.667**), acompañada por una fuerte pérdida de escala: sus **pedidos cayeron de 641 a 422 (-34,32%)** y su **Ticket Promedio se redujo un -32,49%**, hasta **$275**.

* En contraste, la demanda migró masivamente hacia el **Canal Online**, que actuó como motor de volumen al expandir sus órdenes de **793 a 1.056 (+33,42%)**. Sin embargo, este crecimiento no se tradujo en mayor rentabilidad: su **Ganancia Neta también cayó un -41,70%**, pasando de **$82.265 a $47.959**, aun con un Ticket Promedio superior (**$297**).

En conjunto, los resultados muestran que **el crecimiento del volumen Online no fue suficiente para compensar la destrucción de rentabilidad en ambos canales**. Esto indica que el deterioro del negocio no responde únicamente a una contracción de la demanda, sino a una **pérdida de rentabilidad por operación**, cuya causa debe analizarse en la estructura de costos y márgenes.


![Dashboard Ejecutivo](./powerbi/executive_overview.gif)
</details>

<details>
<summary><b>2. Diagnóstico de Rentabilidad — ¿Por qué cayó la rentabilidad? (Clic para expandir)</b></summary><br>
  
La rentabilidad global fue fuertemente erosionada por un deterioro estructural de la relación precio–costo, acompañado por un incremento del costo logístico del canal digital.

* **Deterioro de la relación precio–costo:** El **% Costo de Mercadería** sobre el Revenue Neto aumentó del **66,07% al 78,85% (+12,78 p.p.)** entre 2024 y 2025. El deterioro se replica prácticamente por igual en ambos canales: **Físico (66,61% → 78,74%)** y **Online (65,54% → 78,89%)**. La investigación precio–costo muestra el origen del problema: mientras el **precio unitario promedio aumentó un +17,39%**, el **costo unitario promedio creció un +45,08%**, comprimiendo significativamente el spread entre precio y costo. Este deterioro constituye el **principal factor identificado detrás de la contracción del margen**.

* **Presión logística sobre el canal Online:** El **% Costo Logístico** consolidado aumentó del **1,98% al 4,13%**. El impacto se concentra en el canal Online, donde pasó del **3,90% al 5,66%**. Si bien el canal absorbió el crecimiento de la demanda y elevó su Revenue Neto un **+16,18%**, su Ganancia Neta cayó un **-41,70%** y su Margen Neto se redujo del **30,46% al 15,28%**. La logística, por tanto, actúa como un **factor adicional de erosión del margen**, pero no explica por sí sola el deterioro estructural observado en ambos canales.


![Dashboard Diagnostico de Rentabilidad](./powerbi/profitability_diagnosis.gif)
</details>

<details>
<summary><b>3. Performance de Productos — ¿Dónde conviene intervenir? (Clic para expandir)</b></summary><br>

* **Crisis en Categorías Core:** Las categorías de alto ticket (*Computación*, *Telefonía* y *TV/Video*) sufrieron un colapso en su rentabilidad, cerrando todas **por debajo de la media global (16.90%)**. Si bien en la vista consolidada defienden márgenes positivos bajos, la presión inflacionaria de los proveedores reduce severamente su colchón de ganancia, destacando *TV/Video* con apenas un **8.29% de margen neto** dentro del canal digital.
* **Mitigación y Dispersión en Accesorios:** La categoría *Accesorios* es el principal pulmón financiero del negocio en el entorno digital, aportando **$12,915 en Ganancia Neta** con un sólido **27.66% de margen** y **1,300 unidades vendidas**. Sin embargo, el reporte revela una **alta variación interna**: mientras algunos artículos sostienen el negocio, la categoría concentra la mayor cantidad de productos con margen negativo debido a debido a la insuficiente brecha entre precio de venta y costo total en determinados productos.
* **Efecto Envío Fijo (Canal Online):** Al analizar de forma aislada la operación digital, el tablero enciende las alarmas al registrar **5 Productos No Rentables**. El gráfico de dispersión (*Mix de Catálogo*) muestra de forma explícita cómo múltiples artículos masivos de bajo precio cruzan la barrera del 0% hacia terreno negativo. Al auditar el *Top 5 con Menor Ganancia*, se identifica la fuga de valor liderada por el *Organizador de Cables* **(-$92 de pérdida)**, *Limpiador de Pantallas* **(-$64 de pérdida)** y *Chromecast Google TV* **(-$22 de pérdida)**, confirmando que la estructura de fletes se suma al costo del producto llevando el margen de los productos económicos a negativo.

![Dashboard Performance de Producto](./powerbi/product_performance.gif)
</details>

<details>
<summary><b>4. Retención de Clientes — ¿Qué hacer con la base de clientes? (Clic para expandir)</b></summary><br>

* **Contracción de la base:** Los **Clientes Activos** disminuyeron de **530 a 472**, impulsados por una **Tasa de Churn (Pérdida)** que trepó al **50.94%**, superando por primera vez a la Tasa de Retención.
* **Dependencia de la retención:** Durante 2025, los **Clientes Retenidos** aumentaron su peso en la base (del **45.28% al 55.08%**), aportando el **68.77%** del *revenue* total. En contraste, la adquisición de **Clientes Nuevos** muestra una caída consecutiva año a año.
* **Fuga de Revenue por Categoría:** *Computación* y *TV/Video* registran la mayor pérdida de clientes (**84.62% y 80.60%** respectivamente), consolidándose como las categorías con mayor impacto en el costo de oportunidad del negocio.
* **Relación entre frecuencia y valor:** Los clientes con mayor frecuencia de compra registran también el **Ticket Promedio** más alto, métrica que mostró un incremento saludable durante 2025.

![Dashboard Retención Clientes](./powerbi/customer_retention.gif)
</details>

*Ver modelado y análisis en Power BI:* [`/powerbi`](./powerbi/README.md)

## Recomendaciones Estratégicas 

* **Prioridad Alta (Corto Plazo):** 
  * Reestructurar contratos con proveedores de *Computación* y *TV/Video* ya que los costos actuales cercanos al **88%** comprometen severamente la rentabilidad de estas categorías.
  * Implementar un **monto mínimo de compra** en el *canal online* para diluir el impacto del envío fijo en productos de ticket bajo (*Accesorios*).
* **Prioridad Media (Mediano Plazo):** 
  * Lanzar planes de fidelización enfocados en la base de **Clientes Retenidos**, ya que operan como el motor principal del negocio (aportan el **68.77%** del *revenue*).
  * **Acción inmediata:** Blindar a los **97 Clientes de Alto Valor** que concentran el **73% de la facturación**. 
  * Reactivar de forma controlada la captación de clientes nuevos para revertir la tendencia a la baja interanual.
  * Automatizar estrategias de *cross-selling* desde productos de bajo margen hacia categorías eficientes como *Audio* (**28.20% de margen**).
* **Prioridad Baja (Largo Plazo):** 
  * Evaluar la reconversión de tiendas físicas ineficientes en centros de despacho logísticos, dado que el *canal físico* redujo su ganancia neta a menos de un tercio y el *online* ya concentra el grueso del revenue (**$313K**).

---

## ⚙️ Ingeniería de Datos y Arquitectura

<details>
<summary><b>🐍 Pipeline ETL modular (Python + Pandas)</b></summary><br>

Pipeline ETL desarrollado con **Python + Pandas** para transformar los archivos CSV de origen en datasets limpios, consistentes y estructurados, preparados para su posterior análisis en SQL y Power BI.

El pipeline integra las tablas de **pedidos** y **detalle de pedidos** para generar una tabla transaccional consolidada con **granularidad a nivel de línea de producto**, acompañada por las dimensiones de **clientes** y **productos**. Esta etapa define la estructura y granularidad de los datos que serán utilizados posteriormente en las capas analíticas.

El proceso incorpora:

- **Auditoría de calidad:** controles técnicos, reglas de negocio e integridad referencial.
- **Limpieza y normalización:** tratamiento de valores inválidos, nulos, duplicados y formatos inconsistentes.
- **Transformación:** integración de entidades y aplicación de reglas de negocio, incluyendo el prorrateo de costos de envío.
- **Estructuración:** generación de datasets transaccionales y dimensionales preparados para su explotación analítica.
- **Trazabilidad:** registro de hallazgos y acciones mediante logs.
- **Persistencia:** generación de datasets Clean y Processed para las etapas posteriores.

![Estructura del Pipeline](./pipeline_python/pipeline_estructure.png)

*Ver documentación y estructura del pipeline:* [`/pipeline_python`](./pipeline_python/README.md)
</details>

<details>
<summary><b>🛢️ Investigación analítica (SQL)</b></summary><br>

Sobre la tabla transaccional generada por el pipeline se construyó la **View analítica `fact_pedidos_analitica`**, utilizada para centralizar la lógica de negocio y generar métricas derivadas a nivel de línea, entre ellas:

- `revenue_bruto_linea`
- `revenue_neto_linea`
- `costo_mercaderia_linea`
- `ganancia_neta_linea`

Al tratarse de una **View**, esta capa permite enriquecer analíticamente los datos sin modificar físicamente las tablas procesadas por el pipeline.

A partir de esta capa se desarrolló una investigación SQL progresiva para diagnosticar las causas de la caída de rentabilidad:

**Evolución del negocio → Costos → Pricing → Mix → Canal → Producto**

El análisis permitió identificar como principales señales de deterioro:

- aumento del peso del **costo de mercadería**;
- contracción del **spread precio–costo**;
- cambios en el **mix de ventas**;
- incremento del **costo logístico**, particularmente en el canal Online.

### Técnicas SQL aplicadas

- **CTEs (`WITH`)** para estructurar consultas complejas por etapas.
- **Window Functions** (`LAG`, `ROW_NUMBER`) para variaciones interanuales y rankings.
- **JOINs** entre tablas de hechos y dimensiones.
- **Agregaciones y métricas derivadas** para Revenue, costos, margen, mix y rentabilidad.
- **Análisis de participación** sobre unidades y Revenue.
- **Segmentación temporal, por categoría, producto y canal.**
- **Validación cruzada de métricas** entre SQL y Power BI para garantizar consistencia del modelo analítico.

*Ver investigación y consultas SQL:* [`/sql_queries`](./sql_queries/README.md)


</details>

<details>
<summary><b>📐 Modelado Analítico y Capa Semántica (Power BI)</b></summary><br>

El reporte implementa un **Esquema en Estrella (Star Schema)**, utilizando la tabla transaccional generada por el pipeline como tabla de hechos y conectándola con las dimensiones correspondientes.

- **Tabla de hechos:** `fact_pedidos_final`
- **Dimensión:** `dim_clientes`
- **Dimensión:** `dim_productos`
- **Dimensión:** `dim_calendario`

La tabla de hechos mantiene una **granularidad de línea de producto**, mientras que las dimensiones aportan el contexto necesario para el análisis por cliente, producto y período.

Sobre este modelo se construye la **capa semántica mediante medidas DAX**, donde se implementan los principales KPIs y métricas de negocio:

- **Revenue Neto**
- **Ganancia Neta**
- **Costo de Mercadería**
- **Margen Neto**
- **Ticket Promedio**
- **Retención y Churn**
- **Métricas de crecimiento y variación interanual**

Esta separación permite mantener las tablas transaccionales y dimensionales como base estructural del modelo, mientras que la lógica de cálculo de los indicadores se concentra en la capa semántica de Power BI.

![Vista de Modelo](./powerbi/model_view.png)
</details>
