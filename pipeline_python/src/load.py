import os
import logging
import pandas as pd

logger = logging.getLogger(__name__)


def _save_datasets(datasets: dict, target_dir: str, layer_tag: str) -> None:
    """Función auxiliar privada para iterar, validar y guardar archivos CSV en disco."""
    os.makedirs(target_dir, exist_ok=True)
    
    for filename, df in datasets.items():
        # Control preventivo: Si algún DF llega vacío o None
        if df is None or df.empty:
            logger.warning(
                f"[LOAD][{layer_tag}][{filename}] El DataFrame está vacío o es None. Se omitió el guardado."
            )
            continue
            
        target_path = os.path.join(target_dir, filename)
        df.to_csv(target_path, index=False, encoding="utf-8")
        
        logger.info(
            f"[LOAD][{layer_tag}][{filename}] Archivo guardado correctamente. Filas: {len(df)}."
        )


def save_clean_data(
    clientes_clean: pd.DataFrame,
    productos_clean: pd.DataFrame,
    pedidos_clean: pd.DataFrame,
    detalle_clean: pd.DataFrame
) -> None:
    """Persiste la capa intermedia de datos limpios (Data Staging) en data/clean/."""
    clean_dir = os.path.join("data", "clean")
    
    datasets = {
        "dim_clientes_clean.csv": clientes_clean,
        "dim_productos_clean.csv": productos_clean,
        "fact_pedidos_clean.csv": pedidos_clean,
        "fact_detalle_pedidos_clean.csv": detalle_clean,
    }
    
    _save_datasets(datasets, clean_dir, layer_tag="CLEAN")


def save_processed_data(
    fact_pedidos_final: pd.DataFrame,
    dim_clientes_clean: pd.DataFrame,
    dim_productos_clean: pd.DataFrame
) -> None:
    """Persiste el modelo dimensional final en data/processed/."""
    processed_dir = os.path.join("data", "processed")
    
    datasets = {
        "fact_pedidos_final.csv": fact_pedidos_final,
        "dim_clientes.csv": dim_clientes_clean,
        "dim_productos.csv": dim_productos_clean,
    }
    
    _save_datasets(datasets, processed_dir, layer_tag="PROCESSED")
