# Technoshop | Análisis de Negocio End-to-End

**Introducción:** Este proyecto abarca el ciclo completo de un proceso de analítica de datos. Siguiendo el flujo técnico habitual, comprende el desarrollo de un **pipeline ETL modular en Python**, la construcción de **consultas analíticas en SQL (SQLite)** y la elaboración de un **dashboard interactivo en Power BI**, a partir del cual se obtienen conclusiones y recomendaciones estratégicas.

Con fines de comunicación, este README invierte deliberadamente ese orden para priorizar lo más relevante para el lector: primero presenta los hallazgos y el impacto de negocio, y luego describe la arquitectura técnica que permitió obtenerlos.

**Objetivo:** Identificar las causas raíz de la caída de rentabilidad de una empresa de retail tecnológico entre 2023 y 2025 y elaborar recomendaciones estratégicas basadas en evidencia para apoyar la toma de decisiones.

**Stack Técnico Principal:**
![Python](https://img.shields.io/badge/python-3670A0?style=flat-square&logo=python&logoColor=ffdd54) ![Pandas](https://img.shields.io/badge/pandas-%23150458.svg?style=flat-square&logo=pandas&logoColor=white) ![SQL](https://img.shields.io/badge/sql-%2300758F.svg?style=flat-square&logo=sqlite&logoColor=white) ![Power BI](https://img.shields.io/badge/Power_BI-F2C811?style=flat-square&logo=powerbi&logoColor=black)  

---

## 📈 Crisis e Impacto Financiero

El volumen de pedidos se mantiene estable (**+3.07%**), pero el negocio experimenta una fuerte destrucción de valor: la **Ganancia Neta** se derrumbó un **-57.11%** debido a *shocks* de costos de proveedores (**+45.08%** YoY) y costos logísticos del *canal online* que canibalizan el margen de productos masivos.

### Análisis detallado (Reporte Power BI):

<details>
<summary><b>1. Vista Ejecutiva — ¿Qué pasó con el negocio? (Clic para ver)</b></summary><br>

* Al cierre del año fiscal 2025, la fuerza operativa se mantiene saludable, registrando un incremento del **+3.07%** en pedidos entregados (**1,434** vs. **1,478** órdenes).  
* La **Ganancia Neta** se derrumbó un **-57.11%** (de $169,390 a $72,654) y el **Margen Neto Real** se redujo a la mitad (de **31.90%** a **16.90%**).  
* Se observa un traslado de la operación del *canal físico* al *online* con una caída del **Ticket Promedio** de **21.47%**.

![Dashboard Ejecutivo](./powerbi/executive_overview.gif)
</details>

<details>
<summary><b>2. Diagnóstico de Rentabilidad — ¿Por qué cayó la rentabilidad? (Clic para ver)</b></summary><br>

* La participación del **Costo de Mercadería** saltó del **66.07%** al **78.84%** (**+12.77** p.p.), aplastando el margen de ganancia para 2025.  
* En 2025 la tendencia de precios se invirtió: los costos de proveedores explotaron un **+45.08%** (YoY) y el *retail* solo pudo ajustar precios un **+17.39%** para no destruir la demanda.  
* El crecimiento del *canal online* triplicó su facturación (**$313K**), pero disparó el costo de envíos global del negocio del **2.03%** al **4.25%**, canibalizando la utilidad neta.

![Dashboard Diagnostico de Rentabilidad](./powerbi/profitability_diagnosis.gif)
</details>

<details>
<summary><b>3. Performance de Productos — ¿Dónde conviene intervenir? (Clic para ver)</b></summary><br>

* El **Costo de la Mercadería** de categorías de alto *ticket* (*Computación*, *Telefonía* y *TV/Video*) empujó sus márgenes netos por debajo de la media (incluso a margen negativo), convirtiéndose en los principales causantes de la crisis.
* La categoría *Accesorios* escaló al primer lugar en contribución de ganancias en 2025 (**$22,092**) gracias a un colchón de margen original más alto y un incremento en unidades vendidas. 
* Los productos masivos pero baratos (como *Organizador de Cables* o *Limpiador de Pantallas*) operan con ganancia neta negativa en el *canal online*, debido a que el envío fijo devora el margen.

![Dashboard Performance de Producto](./powerbi/product_performance.gif)
</details>

<details>
<summary><b>4. Retención de Clientes — ¿Qué hacer con la base de clientes? (Clic para ver)</b></summary><br>

* El negocio experimenta una contracción de **Clientes Activos** (de **530** a **472**) y la **Tasa de Pérdida** (*churn*) trepó al **50.94%**, superando por primera vez a la **Tasa de Retención**.  
* Para 2025 el porcentaje de **Clientes Retenidos** aumenta su proporción en la base (del **45.28%** al **68.77%**) y aportan el **68.77%** del *revenue*. Los **Clientes Nuevos** caen todos los años.  
* *Computación* y *TV/Video* son las categorías que más clientes pierden (**84.62%** y **80.60%** respectivamente), representando el mayor *revenue* potencial perdido.
* Los clientes con más frecuencia de compra son también los de mayor **Ticket Promedio**, y estos aumentaron para 2025.

![Dashboard Retención Clientes](./powerbi/customer_retention.gif)
</details>

---

## 🎯 Recomendaciones Estratégicas 

* **Prioridad alta (Corto plazo):** Reestructurar contratos con proveedores de *Computación* y *TV/Video* (costos actuales del **88%** vuelven inviable la categoría) e implementar un monto mínimo de compra *online* para diluir el impacto del envío fijo en *Accesorios*.
* **Prioridad media (Mediano plazo):** Lanzar planes de fidelización enfocados en la base de **Clientes Retenidos**, ya que operan como el motor principal del negocio (aportando el **68.77%** del *revenue* y registrando la mayor frecuencia de compra y **Ticket Promedio**). Dentro de esta estrategia, la acción inmediata es blindar a los **97** *Clientes de Alto Valor* que concentran el **73%** de la facturación. Una vez asegurada esta retención, se recomienda reactivar la captación de clientes nuevos para revertir su tendencia a la baja interanual que amenaza la salud del negocio a largo plazo. Asimismo, se sugiere automatizar estrategias de *cross-selling* hacia categorías eficientes como *Audio* (**28.20%** de margen).
* **Prioridad baja (Largo plazo):** Evaluar la reconversión de tiendas físicas ineficientes en centros de despacho logísticos, dado que el *canal físico* redujo su ganancia neta a un tercio y el *online* concentra el grueso del *revenue* (**$313K**).

---

## ⚙️ Ingeniería de Datos y Arquitectura

<details>
<summary><b>🐍 Pipeline ETL modular (Python + Pandas)</b></summary>
<br>

Para garantizar la calidad de los datos y la consistencia del análisis antes de ser consumidos por el modelo de BI, desarrollé un *pipeline* automatizado, modular y escalable.  

#### Características del pipeline

- **Arquitectura modular y escalable:** cada etapa del proceso se encuentra desacoplada en módulos independientes y organizada mediante funciones auxiliares y orquestadores por entidad.
- **Trazabilidad:** todas las anomalías detectadas y las acciones de limpieza se registran mediante logs estandarizados con información sobre el origen del problema.
- **Reporte estructurado:** la auditoría genera automáticamente un reporte consolidado en formato JSON con los principales hallazgos de calidad de datos.
- **Separación de responsabilidades:** las tareas de extracción, auditoría, limpieza, transformación y carga permanecen aisladas, facilitando el mantenimiento y la extensión del pipeline.

<br>

![Estructura del Pipeline](./pipeline_python/pipeline_estructure.png)  

#### Detalle de los módulos Principales del Pipeline:

<details>
<summary><b>├──🔍 <code>inspect.py</code> — Auditoría de Calidad de Datos (Data Quality Assessment)</b></summary>

<br>

Realiza una auditoría integral de calidad de los datos antes de iniciar el proceso de limpieza. Todos los hallazgos se registran mediante logs en terminal y se consolidan en un reporte estructurado en formato JSON.

<br>

<b>Controles implementados</b>

<br>

<b>Calidad técnica</b>

<ul>
  <li>Espacios en blanco en los bordes de los textos y registros compuestos únicamente por espacios.</li>
  <li>Valores nulos.</li>
  <li>Consistencia de mayúsculas y minúsculas en variables categóricas.</li>
  <li>Duplicados exactos.</li>
  <li>Duplicados de claves primarias (<code>PK</code>).</li>
  <li>Duplicados de negocio (por subconjuntos de columnas).</li>
  <li>Valores de fecha con formato inválido o no parseables.</li>
</ul>

<b>Reglas de negocio</b>

<ul>
  <li>Validaciones específicas para cada entidad, como costos superiores al precio de venta, fechas cronológicamente inconsistentes, estados inválidos y valores fuera de los dominios permitidos.</li>
</ul>

<b>Integridad referencial</b>

<ul>
  <li>Verificación de que todas las claves foráneas (<code>FK</code>) existan en sus correspondientes tablas de dimensión (<code>PK</code>).</li>
</ul>

</details>

<details>
<summary><b>├──🧼 <code>clean.py</code> — Limpieza, Normalización e Integridad de Datos</b></summary>

<br>

Implementa la etapa de limpieza mediante funciones modulares y orquestadores específicos para cada tabla. El módulo corrige, imputa, neutraliza o descarta anomalías según su naturaleza, preservando la trazabilidad mediante logs estandarizados.

<br>

<b>Acciones implementadas</b>

<br>

<b>Calidad técnica</b>

<ul>
  <li>Elimina espacios en blanco en los bordes de las columnas de texto.</li>
  <li>Convierte cadenas vacías o compuestas solo por espacios en valores nulos reales (<code>NA</code>).</li>
  <li>Normaliza el formato de texto mediante <code>Title Case</code> para columnas descriptivas y mayúsculas para identificadores terminados en <code>_id</code>.</li>
  <li>Elimina duplicados exactos, colisiones de clave primaria y duplicados definidos por claves de negocio, conservando la primera ocurrencia.</li>
  <li>Convierte columnas de fecha a tipo <code>datetime</code> mediante parseo seguro.</li>
  <li>Neutraliza fechas inválidas, no parseables o futuras mediante <code>NaT</code>.</li>
</ul>

<b>Tratamiento de valores nulos</b>

<ul>
  <li>Descarta registros que no poseen claves primarias o identificadores esenciales.</li>
  <li>Imputa variables categóricas faltantes con el valor <code>Sin Dato</code>.</li>
  <li>Reconstruye nombres de productos faltantes mediante una etiqueta sintética basada en marca e identificador.</li>
  <li>Incorpora un cliente de contingencia con ID <code>-1</code> para preservar pedidos sin cliente válido.</li>
  <li>Completa cantidades y descuentos faltantes con valores operativos por defecto.</li>
  <li>Reconstruye precios unitarios cuando existen precio de lista y descuento.</li>
  <li>Imputa precios y costos faltantes mediante medianas históricas por producto y año, utilizando como respaldo la mediana por categoría y año.</li>
  <li>Descarta líneas transaccionales cuyos valores monetarios no pueden ser recuperados.</li>
</ul>

<b>Reglas de negocio por entidad</b>

<ul>
  <li><b>Productos:</b> valida que la gama pertenezca al dominio permitido y reasigna los valores inválidos a <code>Sin Dato</code>.</li>
  <li><b>Clientes:</b> neutraliza fechas de nacimiento que generen edades fuera del rango de 0 a 100 años y corrige registros anteriores al nacimiento.</li>
  <li><b>Pedidos:</b> fuerza costo de envío igual a cero para órdenes canceladas y retiros en tienda, e imputa costos logísticos inválidos mediante medianas por año y modalidad de entrega.</li>
  <li><b>Detalle de pedidos:</b> corrige cantidades no positivas, imputa precios y costos inválidos mediante medianas históricas y recalcula el precio unitario según el descuento aplicado.</li>
  <li>Genera un indicador de margen negativo para identificar líneas en las que el precio de venta resulta inferior al costo unitario.</li>
</ul>

<b>Integridad referencial</b>

<ul>
  <li>Reasigna pedidos con clientes inexistentes al cliente de contingencia <code>-1</code>, evitando perder métricas de facturación.</li>
  <li>Elimina líneas de detalle huérfanas que no poseen un pedido padre válido.</li>
  <li>Elimina líneas asociadas a productos inexistentes en la dimensión de productos.</li>
</ul>

<b>Orquestación</b>

<ul>
  <li>Define funciones orquestadoras independientes para productos, clientes, pedidos y detalle de pedidos.</li>
  <li>Ejecuta la limpieza en un orden controlado para respetar las dependencias entre dimensiones y tablas de hechos.</li>
  <li>Consolida el proceso completo mediante una función maestra que devuelve todas las tablas limpias y listas para la etapa de transformación.</li>
</ul>

</details>

*Código fuente disponible en la carpeta:* [`/pipeline_python`](./pipeline_python)
</details>

<details>
<summary><b>🛢️ Consultas y modelado analítico (SQL)</b></summary><br>

Scripts diseñados para responder eficientemente a las preguntas de negocio mediante consultas estructuradas en base de datos:
* Uso de **CTEs** (*Common Table Expressions*) para segmentar y calcular las tasas de retención y pérdida de clientes por año.
* Implementación de agregaciones y uniones complejas (`JOINs`) para consolidar el comportamiento omnicanal cruzando datos de tiendas físicas y plataformas *online*.

*Scripts disponibles en la carpeta:* `/sql_queries`
</details>

<details>
<summary><b>📐 Modelo de datos (Power BI)</b></summary><br>

El reporte implementa un enfoque de **Esquema en Estrella** (*Star Schema*) óptimo para el rendimiento analítico en DAX:
* **Tabla de hechos:** `fact_pedidos`
* **Tablas de dimensiones:** `dim_productos`, `dim_clientes` y `dim_calendario` (vital para el análisis temporal de variaciones YoY).

![Vista de Modelo](./powerbi/model_view.png)
</details>



