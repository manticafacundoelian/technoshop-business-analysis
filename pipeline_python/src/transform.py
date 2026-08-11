import logging
import pandas as pd

logger = logging.getLogger(__name__)


def transform_analytics_data(
    pedidos_clean: pd.DataFrame,
    detalle_clean: pd.DataFrame,
    clientes_clean: pd.DataFrame,
    productos_clean: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
  """Consolida la capa de hechos (fact) unificando pedidos y detalle,

  calculando el prorrateo del costo de envío por ítem y estructurando el
  modelo dimensional final.
  """
  df_detalles = detalle_clean.copy()

  # 1. Contar cuántos ítems tiene cada pedido para prorratear el envío
  df_detalles["items_por_pedido"] = df_detalles.groupby("pedido_id")[
      "pedido_id"
  ].transform("count")

  # 2. Selección de atributos de cabecera y fusión (Inner Join)
  columnas_pedidos_interes = [
      "pedido_id",
      "cliente_id",
      "fecha_pedido",
      "canal_venta",
      "medio_pago",
      "tipo_envio",
      "estado_pedido",
      "costo_envio",
  ]

  len_detalles_inicio = len(df_detalles)

  fact_consolidada = pd.merge(
      df_detalles,
      pedidos_clean[columnas_pedidos_interes],
      on="pedido_id",
      how="inner",
  )

  # Control de integridad: avisa si algún detalle perdió su cabecera en la limpieza de pedidos
  descartados_merge = len_detalles_inicio - len(fact_consolidada)
  if descartados_merge > 0:
      logger.warning(
          f"[TRANSFORM][MERGE][fact_pedidos_final] Se omitieron"
          f" {descartados_merge} líneas de detalle que no tenían cabecera de"
          " pedido válida."
      )

  # 3. Prorrateo del costo de envío por línea
  fact_consolidada["costo_envio_linea"] = (
      fact_consolidada["costo_envio"] / fact_consolidada["items_por_pedido"]
  ).round(2)

  # 4. Ordenamiento cronológico y selección de la estructura final
  fact_consolidada = fact_consolidada.sort_values(
      by="fecha_pedido"
  ).reset_index(drop=True)

  columnas_requeridas = [
      "detalle_id",
      "pedido_id",
      "producto_id",
      "cantidad",
      "precio_lista",
      "precio_unitario",
      "costo_unitario",
      "descuento_aplicado",
      "cliente_id",
      "fecha_pedido",
      "canal_venta",
      "medio_pago",
      "tipo_envio",
      "estado_pedido",
      "costo_envio_linea",
  ]

  fact_consolidada = fact_consolidada[columnas_requeridas]

  logger.info(
      f"[TRANSFORM][COMPLETE][fact_pedidos_final] Consolidación de hechos"
      f" finalizada. Registros finales: {len(fact_consolidada)}."
  )

  return fact_consolidada, clientes_clean, productos_clean
