import pandas as pd
import logging
import os

logger = logging.getLogger(__name__)

# ====================================================
# FUNCION HELPER 
# ====================================================

def _read_csv_safe(filename: str) -> pd.DataFrame | None:
    """
    Construye la ruta relativa, lee los archivos CSV de la carpeta raw y 
    captura fallos de infraestructura y reporta métricas de volumen inicial.
    """
    path = os.path.join('data', 'raw', filename)
    
    try:
        df = pd.read_csv(path)
        logger.info(f"[EXTRACT] Cargado '{filename}' ({len(df)} filas).")
        return df
        
    except FileNotFoundError:
        logger.error(f"[EXTRACT] No se encontró el archivo en la ruta: {path}")
        return None
        
    except Exception as e:
        logger.error(f"[EXTRACT] Falla inesperada al procesar el archivo {filename}: {str(e)}")
        return None

# ====================================================
# FUNCION PRINCIPAL
# ====================================================

def extract_all_data() -> tuple[pd.DataFrame | None, pd.DataFrame | None, pd.DataFrame | None, pd.DataFrame | None]: 
    """
    Extrae y retorna las tablas de hechos y dimensiones garantizando el orden posicional
    requerido por los siguientes eslabones del pipeline.
    """
    pedidos_raw = _read_csv_safe('fact_pedidos_raw.csv')
    detalle_raw = _read_csv_safe('fact_detalle_pedidos_raw.csv')
    clientes_raw = _read_csv_safe('dim_clientes_raw.csv')
    productos_raw = _read_csv_safe('dim_productos_raw.csv')

    return pedidos_raw, detalle_raw, clientes_raw, productos_raw
