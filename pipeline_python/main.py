import logging
import json
import os
from src.extract import extract_all_data
from src.inspect import inspect_data
from src.clean import clean_all_data
from src.transform import transform_analytics_data  
from src.load import load_processed_data        

# Configuración centralizada de logging para el orquestador
logging.basicConfig(
    level=logging.INFO, 
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger(__name__)

def execute_pipeline() -> None:
    """
    Orquesta y ejecuta secuencialmente el pipeline de datos de TechnoShop.
    
    Flujo de ejecución:
    1. Extracción de datos crudos (raw).
    2. Inspección preliminar y reporte de calidad.
    3. Limpieza y normalización (con guardado local de backups limpios).
    4. Transformación analítica para el modelo de datos final.
    5. Carga de los datos procesados al destino.
    """
    
    logger.info("--- INICIANDO PIPELINE DE DATOS TECHNOSHOP ---")

    # 1. Extracción
    logger.info("Fase 1: Extrayendo datos raw...")
    pedidos_raw, detalle_raw, clientes_raw, productos_raw = extract_all_data()
    
    # 2. Inspección
    logger.info("Fase 2: Inspeccionando calidad de los datos...")
    quality_report = inspect_data(pedidos_raw, detalle_raw, clientes_raw, productos_raw)
    
    print("\n" + "="*50)
    print("REPORTE DE CALIDAD DE DATOS (RAW)")
    print("="*50)
    print(json.dumps(quality_report, indent=4, sort_keys=True, default=str))
    print("="*50 + "\n")

    # 3. Limpieza
    logger.info("Fase 3: Ejecutando limpieza y normalización...")
    pedidos_clean, detalle_clean, clientes_clean, productos_clean = clean_all_data(
        pedidos_raw, detalle_raw, clientes_raw, productos_raw
    )

    clean_dir = os.path.join('data', 'clean')
    os.makedirs(clean_dir, exist_ok=True)
    
    clean_datasets = {
        'fact_pedidos_clean.csv': pedidos_clean,
        'fact_detalle_pedidos_clean.csv': detalle_clean,
        'dim_clientes_clean.csv': clientes_clean,
        'dim_productos_clean.csv': productos_clean
    }
    
    for filename, df in clean_datasets.items():
        df.to_csv(os.path.join(clean_dir, filename), index=False, encoding='utf-8')

    # 4. Transformación
    logger.info("Fase 4: Aplicando transformaciones analíticas...")
    fact_pedidos_final, dim_clientes_final, dim_productos_final = transform_analytics_data(
        pedidos_clean, detalle_clean, clientes_clean, productos_clean
    )
    
    # 5. Carga
    logger.info("Fase 5: Cargando datos procesados...")
    load_processed_data(fact_pedidos_final, dim_clientes_final, dim_productos_final)
    
    logger.info("--- PIPELINE EJECUTADO CON ÉXITO ---")

if __name__ == "__main__":
    execute_pipeline()