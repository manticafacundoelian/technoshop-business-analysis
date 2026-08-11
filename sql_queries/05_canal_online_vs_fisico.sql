-- 05 | Evolución del canal online vs. físico
-- Objetivo: analizar el cambio en la composición de revenue por canal
-- y su relación con los costos de envío y el margen neto entre 2024 y 2025.

WITH canal_anual AS (
    SELECT
        anio,
        canal_venta,

        ROUND(SUM(revenue_neto_linea), 2) AS revenue_neto,
        ROUND(SUM(costo_envio_entregados_linea), 2) AS costo_envio_entregados,
        ROUND(SUM(perdida_no_exitosa_linea), 2) AS perdida_no_exitosa,
        ROUND(SUM(ganancia_neta_real_linea), 2) AS ganancia_neta_real,

        ROUND(
            100.0 * SUM(costo_envio_entregados_linea)
            / NULLIF(SUM(revenue_neto_linea), 0),
            2
        ) AS costo_envio_sobre_revenue_pct,

        ROUND(
            100.0 * SUM(ganancia_neta_real_linea)
            / NULLIF(SUM(revenue_neto_linea), 0),
            2
        ) AS margen_neto_pct

    FROM fact_pedidos_analitica

    WHERE anio IN (2024, 2025)

    GROUP BY
        anio,
        canal_venta
),
mix_canal AS (
    SELECT
        anio,
        canal_venta,
        revenue_neto,
        costo_envio_entregados,
        perdida_no_exitosa,
        ganancia_neta_real,
        costo_envio_sobre_revenue_pct,
        margen_neto_pct,

        ROUND(
            100.0 * revenue_neto
            / NULLIF(
                SUM(revenue_neto) OVER (PARTITION BY anio),
                0
            ),
            2
        ) AS share_revenue_pct

    FROM canal_anual
)
SELECT
    canal_venta,

    MAX(CASE WHEN anio = 2024 THEN share_revenue_pct END) AS share_revenue_2024,
    MAX(CASE WHEN anio = 2025 THEN share_revenue_pct END) AS share_revenue_2025,

    ROUND(
        MAX(CASE WHEN anio = 2025 THEN share_revenue_pct END)
        - MAX(CASE WHEN anio = 2024 THEN share_revenue_pct END),
        2
    ) AS delta_share_revenue_pp,

    MAX(CASE WHEN anio = 2024 THEN costo_envio_sobre_revenue_pct END) AS costo_envio_pct_2024,
    MAX(CASE WHEN anio = 2025 THEN costo_envio_sobre_revenue_pct END) AS costo_envio_pct_2025,

    ROUND(
        MAX(CASE WHEN anio = 2025 THEN costo_envio_sobre_revenue_pct END)
        - MAX(CASE WHEN anio = 2024 THEN costo_envio_sobre_revenue_pct END),
        2
    ) AS delta_costo_envio_pp,

    MAX(CASE WHEN anio = 2024 THEN margen_neto_pct END) AS margen_2024,
    MAX(CASE WHEN anio = 2025 THEN margen_neto_pct END) AS margen_2025,

    ROUND(
        MAX(CASE WHEN anio = 2025 THEN margen_neto_pct END)
        - MAX(CASE WHEN anio = 2024 THEN margen_neto_pct END),
        2
    ) AS delta_margen_pp,

    MAX(CASE WHEN anio = 2024 THEN revenue_neto END) AS revenue_2024,
    MAX(CASE WHEN anio = 2025 THEN revenue_neto END) AS revenue_2025,

    ROUND(
        100.0 * (
            MAX(CASE WHEN anio = 2025 THEN revenue_neto END)
            - MAX(CASE WHEN anio = 2024 THEN revenue_neto END)
        )
        / NULLIF(
            MAX(CASE WHEN anio = 2024 THEN revenue_neto END),
            0
        ),
        2
    ) AS var_revenue_yoy_pct

FROM mix_canal
GROUP BY canal_venta
ORDER BY share_revenue_2025 DESC;