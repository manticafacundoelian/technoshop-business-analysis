import json
import logging
import os

from src.clean import clean_all_data
from src.extract import extract_all_data
from src.inspect import inspect_data
from src.transform import transform_analytics_data
from src.load import save_clean_data, save_processed_data


# Configuración centralizada de logging (solo consola)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


def execute_pipeline() -> None:
    """
    Ejecuta de manera secuencial y centralizada el pipeline de Datos de TechnoShop.
    """

    logger.info("[START] INICIANDO PIPELINE DE DATOS TECHNOSHOP")

    # ------------------------------------------------
    # EXTRACT
    # ------------------------------------------------
    
    logger.info("[EXTRACT] Extrayendo datos raw")

    pedidos_raw, detalle_raw, clientes_raw, productos_raw = extract_all_data()

    logger.info("[EXTRACT] Extracción finalizada con exito.")
    
    # ------------------------------------------------
    # INSPECT
    # ------------------------------------------------
    
    logger.info("[INSPECT] Inspeccionando datos raw")

    quality_report = inspect_data(pedidos_raw, detalle_raw, clientes_raw, productos_raw)

    logger.info("[INSPECT] Inspección finalizada con exito.")

    # ------------------------------------------------
    # CLEAN
    # ------------------------------------------------

    logger.info("[CLEAN] Limpiando datos raw")
    
    pedidos_clean, detalle_clean, clientes_clean, productos_clean = (clean_all_data(pedidos_raw, detalle_raw, clientes_raw, productos_raw))

    logger.info("[CLEAN] Limpieza finalizada con exito.")

    # Guardado local de limpios
    save_clean_data(
            clientes_clean=clientes_clean,
            productos_clean=productos_clean,
            pedidos_clean=pedidos_clean,
            detalle_clean=detalle_clean,
        )

    # ------------------------------------------------
    # TRANSFORM
    # ------------------------------------------------

    logger.info("[TRANSFORM] Transformando datos limpios")
    
    fact_pedidos_final, dim_clientes_final, dim_productos_final = (transform_analytics_data(
        pedidos_clean, detalle_clean, clientes_clean, productos_clean
        )
    )

    logger.info("[TRANSFORM] Transformación finalizada con exito.")

    # ------------------------------------------------
    # LOAD
    # ------------------------------------------------

    logger.info("[LOAD] Cargando datos transformados")

    save_processed_data(
        fact_pedidos_final=fact_pedidos_final,
        dim_clientes_clean=dim_clientes_final,
        dim_productos_clean=dim_productos_final,
    )

    logger.info("[LOAD] Carga de datos transformados finalizada con exito.")
    
    logger.info("[SUCCESS] PIPELINE EJECUTADO CON ÉXITO. DATOS LISTOS PARA ANÁLISIS")

    # ------------------------------------------------
    # Reporte de calidad
    # ------------------------------------------------
    
    logger.info("REPORTE DE CALIDAD DE DATOS (RAW):")
    logger.info(
        "\n" + json.dumps(quality_report, indent=4, sort_keys=True, default=str)
    )


if __name__ == "__main__":
    execute_pipeline()
