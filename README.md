# Technoshop Business Analysis
Proyecto de portfolio basado en un dataset sintético que diseñé para simular el comportamiento de una empresa retail con venta de productos de tecnología a través de canales físico y online.

El objetivo del análisis es entender cómo evolucionó el negocio entre 2023 y 2025, respondiendo a cuatro preguntas clave:

1. ¿Qué pasó con el negocio?
2. ¿Por qué cayó la rentabilidad?
3. ¿Dónde conviene intervenir?
4. ¿Qué hacer con la base de clientes?

## Business Context
La empresa presenta una dinámica particular: el volumen de pedidos se mantiene relativamente estable, pero la rentabilidad cae con fuerza entre 2024 y 2025. A través de un enfoque basado en datos, este reporte desarmará los síntomas financieros macro para encontrar las causas raíz operativas y de comportamiento de clientes para poder hacer recomendaciones estratégicas para la toma de decisiones. 

---
## Reporte BI

## Dashboard 1 — Executive Overview — ¿Qué pasó?
-Al cierre del año fiscal 2025, el retail presenta una **paradoja comercial crítica**: la fuerza operativa y la tracción del mercado se mantienen saludables, registrando un incremento del **+3.07% en pedidos entregados** (1,434 vs. 1,478 órdenes). Sin embargo, el negocio experimenta una destrucción masiva de valor: **la Ganancia Neta se derrumbó un -57.11%** (de $169,390 a $72,654) y el **Margen Neto Real se redujo a la mitad** (de 31.90% a 16.90%). 
-Además se observa tambien un **traslado de la operación del Canal Fisico al Online** con una **caída del Ticket Promedio de 21.47%**.




---

## 🔍 2. Análisis Detallado por Capas (Storytelling del Reporte)

### 📈 Fase 1: Dashboard Ejecutivo (El Síntoma Macro)
Esta primera capa expone el comportamiento general de la organización, identificando la contracción de los ingresos y detectando los primeros desvíos geográficos y de canal.
*   **Contracción del Carrito:** El Ticket Promedio se desplomó un **-21.47%** (de $370 a $291), revelando que los clientes gastan significativamente menos en cada transacción.
*   **Pérdida de Estacionalidad:** Históricamente, los meses de diciembre (Fiestas) inyectaban picos masivos de Revenue y estabilidad de margen. En 2025, aunque la facturación sube por estacionalidad, el porcentaje de margen neto se aplana en su mínimo histórico.
*   **Inversión de Canales:** En 2024, el canal Físico lideraba la rentabilidad ($87K netos / 33.38% margen). En 2025, el canal Online pasa a aportar el doble de ganancia ($47K) debido a una migración masiva de la demanda, mientras el Físico colapsa en eficiencia, cayendo a un 21.27% de margen.

*📸 [INSERTAR CAPTURA DE HOJA 1 - DASHBOARD EJECUTIVO]*

---

### 📉 Fase 2: Diagnóstico de Rentabilidad (La Causa Raíz Financiera)
Al abrir la estructura de costos, se detecta el origen macro de la crisis: una severa **compresión de márgenes por shock de oferta**, agravada por ineficiencias logísticas.
*   **Erosión por Costo de Mercadería (COGS):** La participación del costo de los proveedores sobre las ventas saltó del **66.07% al 78.84%** (+12.77 puntos porcentuales), dejando al retail sin margen de maniobra operativo.
*   **Pérdida de Pricing Power:** En 2024, la empresa aumentó sus precios de venta un +15.01% interanual frente a un costo que solo subió un +2.00%. En 2025, la tendencia se invirtió catastróficamente: **los costos de proveedores explotaron un +45.08% (YoY)** y el retail, para no destruir la demanda, solo pudo ajustar precios un **+17.39%**. El gráfico de líneas expone el cierre drástico de esta brecha.
*   **La Trampa Logística del Canal Online:** El crecimiento del canal Online triplicó su facturación ($313K), pero disparó el costo de envíos global del negocio del **2.03% al 4.25%** (+109% de incremento en gasto logístico), canibalizando la utilidad neta de la empresa.

*📸 [INSERTAR CAPTURA DE HOJA 2 - DIAGNÓSTICO DE RENTABILIDAD]*

---

### 📦 Fase 3: Performance de Productos (El Impacto en el Portafolio)
Esta pantalla audita el catálogo analizando la relación entre volumen e ingresos, demostrando que el daño del shock de costos fue asimétrico.
*   **Colapso de las Locomotoras de Alto Ticket:** Las categorías centrales del retail (*Computación, Telefonía y TV/Video*) sufrieron un golpe letal. Sus costos de mercadería tocaron un crítico **83% - 88%**, empujando sus márgenes netos por debajo del umbral del 10% (Rojo Semántico). Computación se desfondó de $52K de ganancia a solo $11K.
*   **Accesorios como el "Salvavidas" Financiero:** El gráfico de cintas (*Ribbon Chart*) revela cómo la categoría *Accesorios* escaló desde los puestos bajos en 2023 hasta adueñarse del **primer lugar en contribución de ganancias en 2025 ($22,092)**. Al partir de un colchón de margen original muy alto (48% en 2024), logró absorber el shock de costos mejor que las notebooks.
*   **Ineficiencia en Productos "Hormiga":** El ranking *Bottom 5* y el *Scatter Chart* exponen que productos masivos pero baratos (como el *Organizador de Cables* o *Limpiador de Pantallas*) operan con **ganancia neta negativa**. Al despacharse de forma individual por el canal online, la tarifa base fija de envío devora por completo el valor del artículo.

*📸 [INSERTAR CAPTURA DE HOJA 3 - PERFORMANCE DE PRODUCTOS]*

---

### 👥 Fase 4: Retención de Clientes (La Consecuencia en el Consumidor)
La mutación del portafolio hacia productos más baratos afectó directamente la fidelidad de la base, transformando al retail en un modelo dependiente de compras esporádicas.
*   **Efecto "Balde Pinchado" (Churn Máximo):** El negocio experimenta una contracción neta de clientes activos (530 a 472). **La Tasa de Pérdida o Churn trepó al 50.94% (Rojo Semántico 🔴)**, superando por primera vez a la Tasa de Retención (49.06%).
*   **La Fuga de Clientes Tecnológicos:** La matriz demuestra que el colapso de márgenes en *Computación* provocó una fuga masiva de su comunidad de usuarios, registrando un alarmante **84.62% de clientes perdidos** (69 bajas vs. 16 retenidos).
*   **La Trampa del "One-Shot" y el Valor del Cliente Retenido:** El 40.68% de los usuarios realiza **una sola compra** y no regresa (asociado a la compra de un accesorio online barato). Sin embargo, la analítica avanzada demuestra que los Clientes Retenidos representan solo el 44.49% de las personas pero inyectan el **68.77% del Revenue total ($295K)**, demostrando que la lealtad sostiene la caja grande del negocio.

*📸 [INSERTAR CAPTURA DE HOJA 4 - RETENCIÓN DE CLIENTES]*

---

## 📋 3. Plan de Recomendaciones Estratégicas (Por Prioridad)

### 🚨 PRIORIDAD ALTA: Detener la hemorragia de margen (Corto Plazo)
1.  **Reestructuración de Contratos de Compras (Tecnología):** Es urgente renegociar los precios de lista con los proveedores de *Computación y TV* o diversificar la matriz de distribución. Operar con un COGS del 88% vuelve inviable la categoría.
2.  **Eliminar el Envío Gratis Incondicional en el Canal Online:** Restringir el envío gratuito en la categoría *Accesorios*. Implementar un **monto mínimo de compra en el carrito** para forzar la venta cruzada y diluir el impacto de la tarifa base de logística.

### ⚠️ PRIORIDAD MEDIA: Blindar la base de clientes valiosa (Mediano Plazo)
3.  **Plan de Fidelización y Retención para Segmento VIP:** Diseñar campañas de marketing dirigidas exclusivamente a rescatar a los clientes de la categoría *Computación* y proteger a los 97 *Clientes de Alto Valor* restantes, quienes generan el 73% del revenue.
4.  **Estrategia de Cross-Selling Automatizada:** Configurar algoritmos de recomendación en la web para que a los compradores de *Accesorios* de bajo margen se les ofrezcan productos complementarios de alta eficiencia (como *Audio*, que retiene un 28.20% de margen y crece en volumen).

### 📉 PRIORIDAD BAJA: Optimización de Estructuras (Largo Plazo)
5.  **Auditoría y Reconversión del Canal Físico:** Dado que el canal físico redujo su ganancia neta a un tercio y el online concentra el grueso del Revenue ($313K), se sugiere evaluar el cierre de tiendas físicas ineficientes o su reconversión en centros de despacho logísticos (*Dark Stores*) para abaratar los costos de envío.

---

## 🛠️ 4. Stack Técnico y Arquitectura del Modelo
*   **Herramienta de Visualización:** Power BI Desktop.
*   **Modelado de Datos:** Esquema en Estrella (*Star Schema*) vinculando tablas de hechos (`fact_pedidos`) con dimensiones (`dim_productos`, `dim_clientes`, `dim_calendario`).
*   **Origen de Datos:** Dataset sintético de Retail Omnicanal enfocado en simular shocks de mercado y dinámicas de portafolio complejas.
*   **Buenas Prácticas Aplicadas:** Consistencia semántica de colores (Gris para costos, Violeta para márgenes/ganancias), desvinculación selectiva de interacciones para análisis de tendencias históricas, eliminación de doble eje Y y ordenación dinámica de matrices por relevancia de volumen financiero.

---

## 🧮 5. Ingeniería de Datos (DAX Snippets Destacados)

Para garantizar un modelo seguro, escalable y libre de errores como `Infinity` o `NaN`, se aplicó lógica de variables y funciones nativas avanzadas:

### A. Rentabilidad por Unidad (KPI Cruzado de Eficiencia)
```dax
Rentabilidad por Unidad = 
DIVIDE(
    [Ganancia Neta Real], 
    [Pedidos Entregados], 
    0
)
```

### B. Conteo de Clientes Retenidos (Intersección de Conjuntos de Usuarios)
```dax
Clientes Retenidos = 
VAR AnioSeleccionado = IF(HASONEVALUE(dim_calendario[Año]), SELECTEDVALUE(dim_calendario[Año]), MAX(dim_calendario[Año]))
VAR ClientesAnioAnterior = 
    CALCULATETABLE(
        VALUES(fact_pedidos_final[cliente_id]),
        dim_calendario[Año] = AnioSeleccionado - 1,
        fact_pedidos_final[estado_pedido] = "Entregado"
    )
VAR ClientesAnioActual = 
    CALCULATETABLE(
        VALUES(fact_pedidos_final[cliente_id]),
        dim_calendario[Año] = AnioSeleccionado,
        fact_pedidos_final[estado_pedido] = "Entregado"
    )
RETURN
COUNTROWS(
    INTERSECT(ClientesAnioAnterior, ClientesAnioActual)
)
```
