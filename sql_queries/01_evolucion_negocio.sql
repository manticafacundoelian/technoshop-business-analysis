-- 01 | Evolución del negocio
-- Objetivo: medir la evolución interanual de pedidos, revenue, ganancia, margen neto y ticket promedio.

WITH reporte_anual AS (
  SELECT 
    anio,
    SUM(revenue_neto_linea) AS revenue_neto,
    SUM(ganancia_neta_real_linea) AS ganancia_neta_real,
    COUNT(DISTINCT CASE WHEN estado_pedido = 'Entregado' THEN pedido_id END) AS pedidos_entregados,
    ROUND(SUM(revenue_neto_linea) / NULLIF(COUNT(DISTINCT CASE WHEN estado_pedido = 'Entregado' THEN pedido_id END), 0), 2) AS ticket_promedio,
    ROUND(100.0 * SUM(ganancia_neta_real_linea) / NULLIF(SUM(revenue_neto_linea), 0), 2) AS margen_neto_pct
  FROM fact_pedidos_analitica
  GROUP BY anio
)
SELECT
  anio,
  pedidos_entregados,
  ROUND(100.0 * (pedidos_entregados - LAG(pedidos_entregados) OVER (ORDER BY anio)) / NULLIF(LAG(pedidos_entregados) OVER (ORDER BY anio), 0), 2) AS var_pedidos_yoy_pct,
  revenue_neto,
  ROUND(100.0 * (revenue_neto - LAG(revenue_neto) OVER (ORDER BY anio)) / NULLIF(LAG(revenue_neto) OVER (ORDER BY anio), 0), 2) AS var_revenue_yoy_pct,
  ganancia_neta_real,
  ROUND(100.0 * (ganancia_neta_real - LAG(ganancia_neta_real) OVER (ORDER BY anio)) / NULLIF(LAG(ganancia_neta_real) OVER (ORDER BY anio), 0), 2) AS var_ganancia_yoy_pct,
  margen_neto_pct,
  ROUND(margen_neto_pct - LAG(margen_neto_pct) OVER (ORDER BY anio), 2) AS var_margen_pp,
  ticket_promedio,
  ROUND(100.0 * (ticket_promedio - LAG(ticket_promedio) OVER (ORDER BY anio)) / NULLIF(LAG(ticket_promedio) OVER (ORDER BY anio), 0), 2) AS var_ticket_yoy_pct
FROM reporte_anual
ORDER BY anio;