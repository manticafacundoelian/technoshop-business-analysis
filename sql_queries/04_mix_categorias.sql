-- 04 | Evolución del mix por categoría
-- Objetivo: analizar cómo cambió la composición de las ventas por categoría
-- y su impacto en revenue por unidad y margen neto entre 2024 y 2025.

WITH categoria_anual AS (
    SELECT
        f.anio,
        p.categoria,

        SUM(CASE WHEN f.estado_pedido = 'Entregado' THEN f.cantidad ELSE 0 END) AS unidades,
        ROUND(SUM(CASE WHEN f.estado_pedido = 'Entregado' THEN f.revenue_neto_linea ELSE 0 END), 2) AS revenue_neto,
        ROUND(SUM(f.ganancia_neta_real_linea), 2) AS ganancia_neta_real
    FROM fact_pedidos_analitica f
    JOIN dim_productos p
        ON f.producto_id = p.producto_id
    WHERE f.anio IN (2024, 2025)
    GROUP BY f.anio, p.categoria
),
totales AS (
    SELECT
        anio,
        SUM(unidades) AS total_unidades,
        SUM(revenue_neto) AS total_revenue
    FROM categoria_anual
    GROUP BY anio
),
mix AS (
    SELECT
        c.anio,
        c.categoria,
        c.unidades,
        c.revenue_neto,
        c.ganancia_neta_real,
        ROUND(100.0 * c.unidades / NULLIF(t.total_unidades, 0), 2) AS share_unidades_pct,
        ROUND(100.0 * c.revenue_neto / NULLIF(t.total_revenue, 0), 2) AS share_revenue_pct,
        ROUND(100.0 * c.ganancia_neta_real / NULLIF(c.revenue_neto, 0), 2) AS margen_pct,
        ROUND(c.revenue_neto / NULLIF(c.unidades, 0), 2) AS revenue_por_unidad
    FROM categoria_anual c
    JOIN totales t
        ON c.anio = t.anio
)
SELECT
    categoria,

    MAX(CASE WHEN anio = 2024 THEN share_unidades_pct END) AS mix_unidades_2024,
    MAX(CASE WHEN anio = 2025 THEN share_unidades_pct END) AS mix_unidades_2025,
    ROUND(
        MAX(CASE WHEN anio = 2025 THEN share_unidades_pct END)
        - MAX(CASE WHEN anio = 2024 THEN share_unidades_pct END),
        2
    ) AS delta_mix_unidades_pp,

    MAX(CASE WHEN anio = 2024 THEN share_revenue_pct END) AS mix_revenue_2024,
    MAX(CASE WHEN anio = 2025 THEN share_revenue_pct END) AS mix_revenue_2025,
    ROUND(
        MAX(CASE WHEN anio = 2025 THEN share_revenue_pct END)
        - MAX(CASE WHEN anio = 2024 THEN share_revenue_pct END),
        2
    ) AS delta_mix_revenue_pp,

    MAX(CASE WHEN anio = 2024 THEN revenue_por_unidad END) AS revenue_por_unidad_2024,
    MAX(CASE WHEN anio = 2025 THEN revenue_por_unidad END) AS revenue_por_unidad_2025,
    ROUND(
        MAX(CASE WHEN anio = 2025 THEN revenue_por_unidad END)
        - MAX(CASE WHEN anio = 2024 THEN revenue_por_unidad END),
        2
    ) AS delta_revenue_por_unidad,

    MAX(CASE WHEN anio = 2024 THEN margen_pct END) AS margen_2024,
    MAX(CASE WHEN anio = 2025 THEN margen_pct END) AS margen_2025,
    ROUND(
        MAX(CASE WHEN anio = 2025 THEN margen_pct END)
        - MAX(CASE WHEN anio = 2024 THEN margen_pct END),
        2
    ) AS delta_margen_pp

FROM mix
GROUP BY categoria
ORDER BY delta_mix_unidades_pp DESC;