# Technoshop | Análisis de Negocio
Proyecto de portfolio basado en un dataset sintético que diseñé para simular el comportamiento de una empresa retail con venta de productos de tecnología a través de canales físico y online.

El objetivo del análisis es entender cómo evolucionó el negocio entre 2023 y 2025, respondiendo a cuatro preguntas clave:

1. ¿Qué pasó con el negocio?
2. ¿Por qué cayó la rentabilidad?
3. ¿Dónde conviene intervenir?
4. ¿Qué hacer con la base de clientes?

## Contexto de Negocio y Objetivo
La empresa presenta una dinámica particular: el volumen de pedidos se mantiene relativamente estable, pero la rentabilidad cae con fuerza entre 2024 y 2025. A través de un enfoque basado en datos, este reporte desarmará los síntomas financieros macro para encontrar las causas raíz operativas y de comportamiento de clientes para poder hacer recomendaciones estratégicas para la toma de decisiones. 

---

## Reporte BI

## Dashboard 1 — Vista Ejecutiva — ¿Qué pasó?
- Al cierre del año fiscal 2025, la fuerza operativa se mantiene saludable, registrando un **incremento del +3.07% en pedidos entregados** (1,434 vs. 1,478 órdenes).  
- Sin embargo, el negocio experimenta una destrucción masiva de valor: **la Ganancia Neta se derrumbó un -57.11%** (de $169,390 a $72,654) y el **Margen Neto Real se redujo a la mitad** (de 31.90% a 16.90%).  
- Además se observa tambien un **traslado de la operación del Canal Fisico al Online** con una **caída del Ticket Promedio de 21.47%**.

![Dashboard Ejecutivo](<./powerbi/executive_overview.gif>)

## Dashboard 2 — Diagnóstico de Rentabilidad — ¿Por qué pasó?
Al analizar la estructura de costos, se detecta el origen macro de la crisis:  
- La participación del **Costo de Mercaderia saltó del 66.07% al 78.84%** (+12.77 puntos porcentuales), aplastando el Margen de Ganancia para 2025.  
- En 2024, la empresa aumentó sus precios de venta un +15.01% interanual frente a un costo que solo subió un +2.00%. En 2025, la tendencia se invirtió: **los costos de proveedores explotaron un +45.08% (YoY)** y el retail, para no destruir la demanda, **solo pudo ajustar precios un +17.39%**.  
- Para 2025 el El crecimiento del canal Online triplicó su facturación ($313K), pero **disparó el costo de envíos global del negocio del 2.03% al 4.25%**, canibalizando la utilidad neta de la empresa.

![Dashboard Diagnostico de Rentabilidad](<./powerbi/profitability_diagnosis.gif>)

## Dashboard 3 — Performance de Productos — ¿Dónde conviene intervenir?
Auditando el catálogo vemos lo siguiente:  
- El **Costo de la Mercaderia de categorías de alto ticket (*Computación, Telefonía y TV/Video*) empujó sus márgenes netos por debajo de la media**, algunos incluso llegando a margen negativo, como vemos en el gráfico de dispersión. Eso sumado a que también perdieron Unidades Vendidas los convierte en los **principales causantes de la crisis** .
- El gráfico de cintas revela cómo la categoría *Accesorios* escaló desde los puestos bajos en 2023 hasta adueñarse del **primer lugar en contribución de ganancias en 2025 ($22,092)** debido a un colchón de margen original más alto que le permitió absorber el shock de costos mejor y a un incremento en unidades vendidas. 
- De todas formas detectamos que **la categoría *Accesorios* contiene los productos de mayor y menor margen**. Productos masivos pero baratos (como el *Organizador de Cables* o *Limpiador de Pantallas*) operan con ganancia neta negativa, más aún en el canal online, debido a que el envio fijo debora el márgen.

![Dashboard Performance de Producto](<./powerbi/product_performance.gif>)

## Dashboard 4 — Retención de Clientes — ¿Qué hacer con la base de clientes?  
- El negocio experimenta una **contracción de Clientes Activos (530 a 472)**.  
- **La Tasa de Pérdida con respecto al año trepó al 50.94%**, superando por primera vez a la Tasa de Retención (49.06%).  
- Así y todo para 2025 el porcentaje de Clientes Retenidos aumenta su proporción en la base de clientes (de 45.28% a 68.77%) y a su vez son los que más porcentaje del Revenue aportan (con un 68.77% para 2025).
- Lamentablemente los Clientes Nuevos caen todos los años.  
- A pesar de ser las categorías que menos trasladaron los costos a los precios, Computación y Tv y Video son las que más clientes pierden, con tasas del 84.62% y el 80.60% respectivamente y también, como vemos en la matriz, los que aportan el mayor revenue potencial perdido.
- Como dato positivo también podemos observar que **los clientes con más frecuencia de compra son también los clientes de mayor Ticket Promedio**, y que estos aumentaron para 2025.
 
![Dashboard Retención Clientes](<./powerbi/customer_retention.gif>)

---

## Plan de Recomendaciones Estratégicas 

### PRIORIDAD ALTA: Detener la hemorragia de margen (Corto Plazo)
1.  **Reestructuración de Contratos de Compras (Tecnología):** Es urgente renegociar los precios de lista con los proveedores de *Computación y TV y Video* ya que operar con un costos del 88% vuelve inviable la categoría.
2.  **Implementar un monto mínimo de compra en el carrito para forzar la venta cruzada y diluir el impacto de la tarifa base de logística que afecta a los *Accesorios*.

### PRIORIDAD MEDIA: Blindar la base de clientes valiosa (Mediano Plazo)
3.  **Plan de Fidelización y Retención**: Diseñar campañas de marketing para retener clientes, ya que son los que más compran y también los que más gastan.
4. **Rescatar a los clientes de la categoría *Computación*.
5. **Proteger a los 97 *Clientes de Alto Valor* restantes**, quienes generan el 73% del revenue.
6. **Estrategia de Cross-Selling Automatizada:** Configurar algoritmos de recomendación en la web para que a los compradores de *Accesorios* de bajo margen se les ofrezcan productos complementarios de alta eficiencia (como *Audio*, que retiene un 28.20% de margen y crece en volumen).

### PRIORIDAD BAJA: Optimización de Estructuras (Largo Plazo)
7. **Auditoría y Reconversión del Canal Físico:** Dado que el canal físico redujo su ganancia neta a un tercio y el online concentra el grueso del Revenue ($313K), se sugiere evaluar el cierre de tiendas físicas ineficientes o su reconversión en centros de despacho logísticos para abaratar los costos de envío.

---

## Stack Técnico y Arquitectura del Modelo
*   **Herramienta de Visualización:** Power BI Desktop.
*   **Modelado de Datos:** Esquema en Estrella (*Star Schema*) vinculando tablas de hechos (`fact_pedidos`) con dimensiones (`dim_productos`, `dim_clientes`, `dim_calendario`).
*   **Origen de Datos:** Dataset sintético de Retail Omnicanal, creado en *Python* y *Faker* enfocado en simular shocks de mercado y dinámicas de portafolio complejas.


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
