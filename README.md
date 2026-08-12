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
  
La rentabilidad global fue fuertemente erosionada en dos frentes:  

* **Deterioro de la relación precio–costo:** El **% Costo de Mercadería** general saltó del **66.07% al 78.85% (+12.78 p.p.)**. Este impacto afectó por igual a la estructura de ambos canales (ambos en torno al 78%), debido a que los costos de proveedores explotaron un **+45.08% (YoY)** y el *retail* solo pudo indexar precios un **+17.39%** para proteger la demanda. Este deterioro constituye el principal factor identificado detrás de la contracción del margen.
* **Fuga Logística Digital:** El **% Costo Logístico** consolidado del negocio aumentó del **1.98% al 4.13% (+2.15 p.p.)**. Al analizar de forma aislada el **Canal Online**, este indicador específico escala hasta el **5.66%**, lo que significa que el canal que sostuvo el volumen del negocio fue también el que absorbió la mayor penalización por costos de envío, reduciendo su propio margen neto (15.28%) y colaborando a la pérdida de margen general.

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

Pipeline ETL desarrollado con **Python + Pandas** para transformar los archivos CSV de origen en datasets limpios y consistentes, listos para su análisis posterior en SQL y Power BI.

El proceso incorpora auditoría de calidad, reglas de negocio, integridad referencial y trazabilidad mediante logs.

![Estructura del Pipeline](./pipeline_python/pipeline_estructure.png)  

*Ver documentación y estructura del pipeline:* [`/pipeline_python`](./pipeline_python/README.md)
</details>

<details>
<summary><b>🛢️ Investigación analítica (SQL)</b></summary><br>

Se construyó una View analítica (fact_pedidos_analitica) sobre la tabla de hechos para centralizar la lógica de negocio y las principales métricas de rentabilidad.

A partir de esta capa se desarrolló una investigación SQL progresiva para diagnosticar la caída de rentabilidad, analizando:

Evolución del negocio → Costos → Pricing → Mix → Canal → Producto

El análisis permitió identificar como principales señales de deterioro el aumento del peso del costo de mercadería, la contracción del spread precio–costo y el cambio en el mix de ventas. También se comprobó que el crecimiento del canal Online y el aumento del costo logístico contribuyen al deterioro, pero no explican por sí solos la caída estructural del margen.


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
<summary><b>📐 Modelo de datos (Power BI)</b></summary><br>

El reporte implementa un enfoque de **Esquema en Estrella** (*Star Schema*) óptimo para el rendimiento analítico en DAX:
* **Tabla de hechos:** `fact_pedidos_final`
* **Tablas de dimensiones:** `dim_productos`, `dim_clientes` y `dim_calendario` (vital para el análisis temporal de variaciones YoY).

![Vista de Modelo](./powerbi/model_view.png)
</details>
