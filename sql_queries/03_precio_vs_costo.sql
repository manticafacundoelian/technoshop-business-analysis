-- 03 | Evolución de precios vs. costos
-- Objetivo: comparar la evolución anual del precio y costo promedio
-- por producto e identificar cambios en pricing, presión de costos
-- y evolución del spread precio-costo.

WITH producto_anual AS (
    SELECT
        anio,
        producto_id,
        AVG(precio_lista) AS precio_prom_producto,
        AVG(costo_unitario) AS costo_prom_producto
    FROM fact_pedidos_analitica
    WHERE estado_pedido = 'Entregado'
    GROUP BY anio, producto_id
),
resumen_anual AS (
    SELECT
        anio,
        ROUND(AVG(precio_prom_producto), 2) AS precio_promedio_por_producto,
        ROUND(AVG(costo_prom_producto), 2) AS costo_promedio_por_producto,
        ROUND(
            AVG(precio_prom_producto) - AVG(costo_prom_producto),
            2
        ) AS spread_precio_costo
    FROM producto_anual
    GROUP BY anio
)
SELECT
    anio,
    precio_promedio_por_producto,
    costo_promedio_por_producto,
    spread_precio_costo,

    ROUND(
        precio_promedio_por_producto
        - LAG(precio_promedio_por_producto) OVER (ORDER BY anio),
        2
    ) AS var_precio_abs,

    ROUND(
        100.0 * (
            precio_promedio_por_producto
            - LAG(precio_promedio_por_producto) OVER (ORDER BY anio)
        ) / NULLIF(
            LAG(precio_promedio_por_producto) OVER (ORDER BY anio),
            0
        ),
        2
    ) AS var_precio_pct,

    ROUND(
        costo_promedio_por_producto
        - LAG(costo_promedio_por_producto) OVER (ORDER BY anio),
        2
    ) AS var_costo_abs,

    ROUND(
        100.0 * (
            costo_promedio_por_producto
            - LAG(costo_promedio_por_producto) OVER (ORDER BY anio)
        ) / NULLIF(
            LAG(costo_promedio_por_producto) OVER (ORDER BY anio),
            0
        ),
        2
    ) AS var_costo_pct,

    ROUND(
        spread_precio_costo
        - LAG(spread_precio_costo) OVER (ORDER BY anio),
        2
    ) AS var_spread_abs,

    ROUND(
        100.0 * (
            spread_precio_costo
            - LAG(spread_precio_costo) OVER (ORDER BY anio)
        ) / NULLIF(
            LAG(spread_precio_costo) OVER (ORDER BY anio),
            0
        ),
        2
    ) AS var_spread_pct

FROM resumen_anual
ORDER BY anio;