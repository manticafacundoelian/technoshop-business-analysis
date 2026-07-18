import pandas as pd
import logging
import os

logger = logging.getLogger(__name__)

def load_processed_data(
    fact_pedidos_final: pd.DataFrame, 
    dim_clientes_clean: pd.DataFrame, 
    dim_productos_clean: pd.DataFrame
) -> None:
    """Persiste el modelo de datos final transformado en la capa de almacenamiento local."""
    output_dir = os.path.join('data', 'processed')
    os.makedirs(output_dir, exist_ok=True)
    
    datasets = {
        'fact_pedidos_final.csv': fact_pedidos_final,
        'dim_clientes.csv': dim_clientes_clean,
        'dim_productos.csv': dim_productos_clean
    }

    for filename, df in datasets.items():
        target_path = os.path.join(output_dir, filename)
        df.to_csv(target_path, index=False, encoding='utf-8')
        logger.info(f"Archivo guardado: '{filename}' | Volumen: {len(df)} filas.")