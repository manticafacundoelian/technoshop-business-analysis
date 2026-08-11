-- 02 | Drivers de costo y rentabilidad
-- Objetivo: descomponer el deterioro de la rentabilidad para identificar
-- qué componentes de costo explican la caída de la ganancia y del margen neto.

WITH reporte_anual AS (
  SELECT
    anio,
    ROUND(SUM(revenue_neto_linea), 2) AS revenue_neto,
    ROUND(SUM(costo_mercaderia_linea), 2) AS costo_mercaderia,
    ROUND(SUM(costo_envio_entregados_linea), 2) AS costo_envio_entregados,
    ROUND(SUM(perdida_no_exitosa_linea), 2) AS perdida_no_exitosa,
    ROUND(SUM(ganancia_neta_real_linea), 2) AS ganancia_neta_real,
	ROUND(100.0 * SUM(costo_mercaderia_linea) / NULLIF(SUM(revenue_neto_linea), 0), 2) AS costo_mercaderia_sobre_revenue_pct,
    ROUND(100.0 * SUM(costo_envio_entregados_linea) / NULLIF(SUM(revenue_neto_linea), 0), 2) AS costo_envio_sobre_revenue_pct,
    ROUND(100.0 * SUM(perdida_no_exitosa_linea) / NULLIF(SUM(revenue_neto_linea), 0), 2) AS perdida_no_exitosa_sobre_revenue_pct,
    ROUND(100.0 * SUM(ganancia_neta_real_linea) / NULLIF(SUM(revenue_neto_linea), 0), 2) AS margen_neto_pct
  FROM fact_pedidos_analitica
  GROUP BY anio
)
SELECT
  anio,
  revenue_neto,
  ROUND(100.0 * (revenue_neto - LAG(revenue_neto) OVER (ORDER BY anio)) / NULLIF(LAG(revenue_neto) OVER (ORDER BY anio), 0), 2) AS var_revenue_yoy_pct,
  costo_mercaderia,
  ROUND(100.0 * (costo_mercaderia - LAG(costo_mercaderia) OVER (ORDER BY anio)) / NULLIF(LAG(costo_mercaderia) OVER (ORDER BY anio), 0), 2) AS var_costo_mercaderia_yoy_pct,
  costo_mercaderia_sobre_revenue_pct,
  costo_envio_entregados,
  ROUND(100.0 * (costo_envio_entregados - LAG(costo_envio_entregados) OVER (ORDER BY anio)) / NULLIF(LAG(costo_envio_entregados) OVER (ORDER BY anio), 0), 2) AS var_costo_envio_yoy_pct,
  costo_envio_sobre_revenue_pct,
  perdida_no_exitosa,
  ROUND(100.0 * (perdida_no_exitosa - LAG(perdida_no_exitosa) OVER (ORDER BY anio)) / NULLIF(LAG(perdida_no_exitosa) OVER (ORDER BY anio), 0), 2) AS var_perdida_no_exitosa_yoy_pct,
  perdida_no_exitosa_sobre_revenue_pct,
  ganancia_neta_real,
  ROUND(100.0 * (ganancia_neta_real - LAG(ganancia_neta_real) OVER (ORDER BY anio)) / NULLIF(LAG(ganancia_neta_real) OVER (ORDER BY anio), 0), 2) AS var_ganancia_yoy_pct,
  margen_neto_pct,
  ROUND(margen_neto_pct - LAG(margen_neto_pct) OVER (ORDER BY anio), 2) AS var_margen_pp
FROM reporte_anual
ORDER BY anio;