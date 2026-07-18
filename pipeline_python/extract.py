import pandas as pd
import logging
import os

logger = logging.getLogger(__name__)

# =============================================================================
# FUNCIONES DE EXTRACCIÓN
# =============================================================================

def _read_csv_safe(filename: str) -> pd.DataFrame | None:
    """
    Lee un archivo CSV de forma segura desde la capa raw y gestiona excepciones de lectura.
    """
    path = os.path.join('data', 'raw', filename)
    
    try:
        df = pd.read_csv(path)
        logger.info(f"Cargado '{filename}' ({len(df)} filas).")
        return df
        
    except FileNotFoundError:
        logger.error(f"No se encontró el archivo en la ruta: {path}")
        return None
        
    except Exception as e:
        logger.error(f"Falla inesperada al procesar el archivo {filename}: {str(e)}")
        return None

def extract_all_data() -> tuple[pd.DataFrame | None, pd.DataFrame | None, pd.DataFrame | None, pd.DataFrame | None]: 
    """
    Extrae y retorna las 4 tablas transaccionales en orden (pedidos, detalle, clientes, productos).
    """
    pedidos_raw = _read_csv_safe('fact_pedidos_raw.csv')
    detalle_raw = _read_csv_safe('fact_detalle_pedidos_raw.csv')
    clientes_raw = _read_csv_safe('dim_clientes_raw.csv')
    productos_raw = _read_csv_safe('dim_productos_raw.csv')

    return pedidos_raw, detalle_raw, clientes_raw, productos_raw