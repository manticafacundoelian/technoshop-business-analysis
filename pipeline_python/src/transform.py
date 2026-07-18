import pandas as pd
import logging

logger = logging.getLogger(__name__)

def transform_analytics_data(
    pedidos_clean: pd.DataFrame, 
    detalle_clean: pd.DataFrame, 
    clientes_clean: pd.DataFrame, 
    productos_clean: pd.DataFrame
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Consolida las tablas de hechos calculando el costo de envío prorrateado."""
    
    # 1. Contar cuántos productos distintos tiene cada pedido para el prorrateo
    df_detalles = detalle_clean.copy()
    df_detalles['items_por_pedido'] = df_detalles.groupby('pedido_id')['pedido_id'].transform('count')

    # 2. Unir las tablas de hechos
    columnas_pedidos_interes = [
        'pedido_id', 'cliente_id', 'fecha_pedido', 'canal_venta', 
        'medio_pago', 'tipo_envio', 'estado_pedido', 'costo_envio'
    ]
    
    fact_consolidada = pd.merge(
        df_detalles, 
        pedidos_clean[columnas_pedidos_interes], 
        on='pedido_id', 
        how='inner'
    )
    logger.info(f"Fusionadas tablas de hechos. Registros resultantes: {len(fact_consolidada)}")

    # 3. Calcular prorrateo
    fact_consolidada['costo_envio_linea'] = (
        fact_consolidada['costo_envio'] / fact_consolidada['items_por_pedido']
    ).round(2)
    logger.info("Costo de envío prorrateado por línea.")

    # 4. Ordenamiento y Filtro estricto
    fact_consolidada = fact_consolidada.sort_values(by='fecha_pedido').reset_index(drop=True)

    columnas_requeridas = [
        'detalle_id', 'pedido_id', 'producto_id', 'cantidad', 'precio_lista', 
        'precio_unitario', 'costo_unitario', 'descuento_aplicado', 'cliente_id', 
        'fecha_pedido', 'canal_venta', 'medio_pago', 'tipo_envio', 'estado_pedido', 
        'costo_envio_linea'
    ]
    
    fact_consolidada = fact_consolidada[columnas_requeridas]
    
    return fact_consolidada, clientes_clean, productos_clean