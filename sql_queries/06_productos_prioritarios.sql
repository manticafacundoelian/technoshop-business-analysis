-- 06 | Identificación de productos prioritarios
-- Objetivo: identificar productos con mayor deterioro de ganancia y margen
-- entre 2024 y 2025 para detectar puntos concretos de intervención.

WITH producto_anual AS (
    SELECT
        anio,
        p.categoria,
        p.nombre_producto,

        ROUND(SUM(revenue_neto_linea), 2) AS revenue_neto,
        ROUND(SUM(ganancia_neta_real_linea), 2) AS ganancia_neta_real,

        ROUND(
            100.0 * SUM(ganancia_neta_real_linea)
            / NULLIF(SUM(revenue_neto_linea), 0),
            2
        ) AS margen_neto_pct

    FROM fact_pedidos_analitica f
    JOIN dim_productos p
        ON f.producto_id = p.producto_id

    WHERE anio IN (2024, 2025)

    GROUP BY
        anio,
        p.categoria,
        p.nombre_producto
),
comparacion AS (
    SELECT
        p25.categoria,
        p25.nombre_producto,

        p24.revenue_neto AS revenue_2024,
        p25.revenue_neto AS revenue_2025,

        p24.ganancia_neta_real AS ganancia_2024,
        p25.ganancia_neta_real AS ganancia_2025,

        p24.margen_neto_pct AS margen_2024,
        p25.margen_neto_pct AS margen_2025,

        ROUND(
            p25.ganancia_neta_real - p24.ganancia_neta_real,
            2
        ) AS delta_ganancia,

        ROUND(
            p25.margen_neto_pct - p24.margen_neto_pct,
            2
        ) AS delta_margen_pp

    FROM producto_anual p25
    JOIN producto_anual p24
        ON p25.nombre_producto = p24.nombre_producto
       AND p25.categoria = p24.categoria
       AND p25.anio = 2025
       AND p24.anio = 2024
)
SELECT
    categoria,
    nombre_producto,
    revenue_2024,
    revenue_2025,
    ganancia_2024,
    ganancia_2025,
    delta_ganancia,
    margen_2024,
    margen_2025,
    delta_margen_pp
FROM comparacion
ORDER BY
    delta_ganancia ASC,
    delta_margen_pp ASC;





