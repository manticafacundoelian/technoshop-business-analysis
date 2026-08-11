import pandas as pd
import logging

logger = logging.getLogger(__name__)

# =============================================================================#
# FUNCIONES AUXILIARES GENERALES                                               #
# =============================================================================#

#===================================================#
# NORMALIZACION DE TEXTO                            #
#===================================================#
def normalize_text_columns(
    df: pd.DataFrame, nombre_tabla: str = ""
) -> pd.DataFrame:
    """
    Estandariza columnas de tipo string eliminando espacios marginales, transformando
    celdas vacías en nulos reales (NA) y aplicando formato según el rol de la
    columna: Upper para identificadores (`_id`) y Title para texto descriptivo general.
    """
    df = df.copy()
    text_cols = df.select_dtypes(include=["object", "string"]).columns

    for col in text_cols:
        col_series = df[col].astype("string")
        before_nulls = col_series.isna().sum()

        # 1. Detectar cuántas celdas cambian al remover espacios en bordes
        stripped_series = col_series.str.strip()
        border_spaces = int(
            ((col_series != stripped_series) & col_series.notna()).sum()
        )

        # 2. Aplicar el strip y convertir cadenas vacías/espacios en NA
        df[col] = stripped_series
        df[col] = df[col].replace(r"^\s*$", pd.NA, regex=True)

        # 3. Aplicar formato según el tipo de columna
        if not col.endswith("_id"):
            df[col] = df[col].str.title()
        else:
            df[col] = df[col].str.upper()

        # 4. Calcular nulos generados a partir de celdas que eran solo espacios
        after_nulls = df[col].isna().sum()
        new_nulls = int(after_nulls - before_nulls)
        
        # --- REPORTE EN LOGS ---
        if border_spaces > 0:
            logger.info(
                f"[CLEAN][NORMALIZE][{nombre_tabla}] Se removieron espacios en"
                f" bordes en {border_spaces} filas en '{col}'."
            )

        if new_nulls > 0:
            logger.warning(
                f"[CLEAN][NORMALIZE][{nombre_tabla}] {new_nulls} nuevos nulos"
                f" generados tras convertir celdas vacías a NA en '{col}'."
            )

    return df

#===================================================#
# LIMPIEZA DE DUPLICADOS                            #
#===================================================#

def clean_table_duplicates(
    df: pd.DataFrame, 
    nombre_tabla: str, 
    pk_subset: list = None, 
    business_subset: list = None
) -> pd.DataFrame:
    """
    Elimina duplicados de forma jerárquica:
    1. Duplicados exactos (todas las columnas).
    2. Colisiones en Clave Primaria (PK).
    3. Duplicados por Clave de Negocio (Business logic).
    """

    total_inicial = len(df)
    
    # 1. Duplicados exactos
    df = df.drop_duplicates(keep='first')
    exactos_eliminados = total_inicial - len(df)
    if exactos_eliminados > 0:
        logger.warning(
            f"[CLEAN][DUPLICATES][EXACT][{nombre_tabla}] Se eliminaron {exactos_eliminados} filas por duplicación exacta (100% idénticas)."
        )
    
    # 2. Duplicados por PK (Identificadores únicos de registro)
    if pk_subset:
        total_antes_pk = len(df)
        df = df.drop_duplicates(subset=pk_subset, keep='first')
        pk_eliminados = total_antes_pk - len(df)
        if pk_eliminados > 0:
            logger.warning(
                f"[CLEAN][DUPLICATES][PK][{nombre_tabla}] Se eliminaron {pk_eliminados} filas por colisión de PK en {pk_subset}."
            )

    # 3. Duplicados por Clave de Negocio (Reglas operativas)
    if business_subset:
        total_antes_biz = len(df)
        df= df.drop_duplicates(subset=business_subset, keep='first')
        biz_eliminados = total_antes_biz - len(df)
        if biz_eliminados > 0:
            logger.warning(
                f"[CLEAN][DUPLICATES][BUSINESS][{nombre_tabla}] Se eliminaron {biz_eliminados} filas por duplicación de negocio en {business_subset}."
            )

    total_final = len(df)
    eliminados_totales = total_inicial - total_final
    
    if eliminados_totales > 0:
        logger.info(
            f"[CLEAN][DUPLICATES][{nombre_tabla}] Limpieza de duplicados finalizada. Filas: {total_inicial} -> {total_final}."
        )
        
    return df

# ===================================================#
# TRATAMIENTO DE NULOS POR ENTIDAD                   #
# ===================================================#

def handle_nulls_productos(productos_df: pd.DataFrame) -> pd.DataFrame:
    """
    Sanea nulos en Productos: descarta sin ID, imputa categóricas 
    y reconstruye nombres faltantes.
    """
    df = productos_df.copy()
    
    # 1. Descarte de registros sin PK
    init_len = len(df)
    df = df.dropna(subset=["producto_id"])
    dropped = init_len - len(df)
    if dropped > 0:
        logger.warning(f"[CLEAN][NULLS][dim_productos] Se descartaron {dropped} productos por falta de 'producto_id'.")
    
    # 2. Imputación de categóricas
    for col in ["categoria", "marca", "gama"]:
        if col in df.columns:
            df[col] = df[col].fillna("Sin Dato")
        
    # 3. Reconstrucción sintética de nombre_producto
    mask_nombre_nulo = df["nombre_producto"].isna()
    if mask_nombre_nulo.any():
        df.loc[mask_nombre_nulo, "nombre_producto"] = (
            "Producto " + df.loc[mask_nombre_nulo, "marca"].astype(str) + 
            " - ID: " + df.loc[mask_nombre_nulo, "producto_id"].astype(str)
        )
        
    logger.info(f"[CLEAN][NULLS][dim_productos] Tratamiento de nulos completado. Filas finales: {len(df)}.")
    return df


def handle_nulls_clientes(clientes_df: pd.DataFrame) -> pd.DataFrame:
    """
    Sanea Clientes: descarta sin ID, imputa categóricas e inyecta 
    el cliente genérico de contingencia (ID: -1).
    """
    df = clientes_df.copy()
    
    # 1. Descarte de registros sin PK
    init_len = len(df)
    df = df.dropna(subset=["cliente_id"])
    dropped = init_len - len(df)
    if dropped > 0:
        logger.warning(f"[CLEAN][NULLS][dim_clientes] Se descartaron {dropped} clientes por falta de 'cliente_id'.")
    
    # 2. Imputación de categóricas
    for col in ["nombre", "apellido", "genero", "ciudad", "provincia", "canal_adquisicion"]:
        if col in df.columns:
            df[col] = df[col].fillna("Sin Dato")
            
    # 3. Registro de contingencia para ventas huérfanas
    if -1 not in df["cliente_id"].values:
        fila_invitado = pd.DataFrame([{
            "cliente_id": -1, "nombre": "Consumidor", "apellido": "Final", 
            "genero": "Sin Dato", "fecha_nacimiento": pd.NaT, "ciudad": "Sin Dato", 
            "provincia": "Sin Dato", "fecha_registro": pd.NaT, "canal_adquisicion": "Sin Dato"
        }])
        df = pd.concat([df, fila_invitado], ignore_index=True)
        
    logger.info(f"[CLEAN][NULLS][dim_clientes] Tratamiento de nulos completado. Filas finales: {len(df)}.")
    return df


def handle_nulls_pedidos(pedidos_df: pd.DataFrame) -> pd.DataFrame:
    """
    Sanea Pedidos: vincula clientes faltantes al ID -1, imputa categóricas 
    y genera columna temporal_anio para cálculos monetarios posteriores.
    """
    df = pedidos_df.copy()
    
    # 1. Descarte de registros sin PK
    init_len = len(df)
    df = df.dropna(subset=["pedido_id"])
    dropped = init_len - len(df)
    if dropped > 0:
        logger.warning(f"[CLEAN][NULLS][fact_pedidos] Se descartaron {dropped} pedidos por falta de 'pedido_id'.")
    
    # 2. Asignación a cliente de contingencia si falta cliente_id
    nulls_cliente = df["cliente_id"].isna().sum()
    if nulls_cliente > 0:
        df["cliente_id"] = df["cliente_id"].fillna(-1).astype(int)
        logger.warning(f"[CLEAN][NULLS][fact_pedidos] Reasignados {nulls_cliente} pedidos sin cliente_id al ID (-1).")
    
    # 3. Categóricas y costos
    for col in ["canal_venta", "medio_pago", "estado_pedido", "tipo_envio"]:
        if col in df.columns:
            df[col] = df[col].fillna("Sin Dato")
            
    if "costo_envio" in df.columns:
        df["costo_envio"] = df["costo_envio"].fillna(0.0)

    # 4. Columna aux temporal para imputaciones económicas en detalle
    df["temporal_anio"] = pd.to_datetime(df["fecha_pedido"], errors="coerce").dt.year
    df["temporal_anio"] = df["temporal_anio"].fillna(2024).astype(int)
    
    logger.info(f"[CLEAN][NULLS][fact_pedidos] Tratamiento de nulos completado. Filas finales: {len(df)}.")
    return df


def handle_nulls_detalle(
    detalle_df: pd.DataFrame, 
    pedidos_clean_df: pd.DataFrame, 
    productos_clean_df: pd.DataFrame
) -> pd.DataFrame:
    """
    Algoritmo de imputación económica e inflacionaria para métricas monetarias.
    Reconstruye precios/costos faltantes mediante medianas históricas por año.
    """
    df = detalle_df.copy()
    
    # 1. Descarte de registros sin IDs clave
    init_len = len(df)
    df = df.dropna(subset=["detalle_id", "pedido_id", "producto_id"])
    dropped = init_len - len(df)
    if dropped > 0:
        logger.warning(f"[CLEAN][NULLS][fact_detalle_pedidos] Se descartaron {dropped} filas por falta de IDs clave.")

    # 2. Valores por defecto básicos
    df["cantidad"] = df["cantidad"].fillna(1)
    df["descuento_aplicado"] = df["descuento_aplicado"].fillna(0.0)

    # 3. Cruce con el año del pedido
    df = df.merge(pedidos_clean_df[["pedido_id", "temporal_anio"]], on="pedido_id", how="left")
    df["temporal_anio"] = df["temporal_anio"].fillna(2024).astype(int)

    # 4. Reparación directa: si hay precio_lista y descuento, calculamos precio_unitario
    mask_precio_null = df["precio_unitario"].isna()
    mask_lista_ok = df["precio_lista"].notna()
    mask_reparacion = mask_precio_null & mask_lista_ok
    
    if mask_reparacion.any():
        df.loc[mask_reparacion, "precio_unitario"] = (
            df.loc[mask_reparacion, "precio_lista"] * (1 - df.loc[mask_reparacion, "descuento_aplicado"])
        ).round(2)

    # 5. Imputación por mediana (Producto + Año)
    cols_monetarias = ["precio_lista", "precio_unitario", "costo_unitario"]
    
    if df[cols_monetarias].isna().any().any():
        meds_prod = df.groupby(["producto_id", "temporal_anio"])[cols_monetarias].transform("median")
        df[cols_monetarias] = df[cols_monetarias].fillna(meds_prod)

    # 6. Imputación de respaldo por mediana (Categoría + Año)
    if df[cols_monetarias].isna().any().any():
        df = df.merge(productos_clean_df[["producto_id", "categoria"]], on="producto_id", how="left")
        df["categoria"] = df["categoria"].fillna("Sin Dato")
        
        meds_cat = df.groupby(["categoria", "temporal_anio"])[cols_monetarias].transform("median")
        df[cols_monetarias] = df[cols_monetarias].fillna(meds_cat)
        df = df.drop(columns=["categoria"])

    # 7. Ajuste final y reporte de descartes irrecuperables
    filas_antes = len(df)
    df = df.dropna(subset=cols_monetarias)
    borrados_final = filas_antes - len(df)
    
    if borrados_final > 0:
        logger.warning(
            f"[CLEAN][NULLS][fact_detalle_pedidos] Se descartaron {borrados_final} filas irrecuperables por falta de precios."
        )

    df["precio_unitario"] = (df["precio_lista"] * (1 - df["descuento_aplicado"])).round(2)

    logger.info(f"[CLEAN][NULLS][fact_detalle_pedidos] Tratamiento de nulos completado. Filas finales: {len(df)}.")
    return df

# ===================================================#
# TRATAMIENTO Y NORMALIZACIÓN DE FECHAS              #
# ===================================================#

def clean_date_columns(
    df: pd.DataFrame, 
    nombre_tabla: str, 
    date_columns: list
) -> pd.DataFrame:
    """
    Parsea columnas a tipo datetime, detecta formatos corruptos y neutraliza 
    fechas incoherentes en el futuro reemplazándolas por NaT.
    """
    df = df.copy()
    now = pd.Timestamp.now()

    for col in date_columns:
        if col not in df.columns:
            continue

        nulos_previos = df[col].isna().sum()

        # Parseo seguro a datetime (lo no válido pasa a NaT)
        df[col] = pd.to_datetime(df[col], errors="coerce")
        
        # Conteo de formatos inválidos
        nulos_posteriores = df[col].isna().sum()
        corruptas = nulos_posteriores - nulos_previos
        if corruptas > 0:
            logger.warning(f"[CLEAN][DATES][{nombre_tabla}] Se detectaron {corruptas} valores con formato de fecha inválido en '{col}'.")

        # Neutralización de fechas futuras
        mask_futuras = df[col] > now
        futuras_count = mask_futuras.sum()
        if futuras_count > 0:
            df.loc[mask_futuras, col] = pd.NaT
            logger.warning(f"[CLEAN][DATES][{nombre_tabla}] Se neutralizaron {futuras_count} fechas futuras en '{col}' (convertidas a NaT).")

    return df

# ====================================================#
# REGLAS DE NEGOCIO                                   #
# ====================================================#

def handle_business_rules_productos(productos_df: pd.DataFrame) -> pd.DataFrame:
    """
    Garantiza la consistencia del catálogo validando que el atributo 'gama' pertenezca 
    a un dominio cerrado predefinido; reasigna cualquier desvío como 'Sin Dato'.
    """
    df = productos_df.copy()
    gamas_validas = ["Alta", "Media", "Baja", "Sin Dato"]
    mask_gama_invalida = ~df["gama"].isin(gamas_validas) & df["gama"].notna()
    if mask_gama_invalida.any():
        logger.warning(f"[CLEAN][BUSINESS RULES][dim_productos] Se reasignaron {mask_gama_invalida.sum()} registros con gama inválida a 'Sin Dato'.")
        df.loc[mask_gama_invalida, "gama"] = "Sin Dato"
    return df

def handle_business_rules_clientes(clientes_df: pd.DataFrame) -> pd.DataFrame:
    """
    Aplica controles cronológicos y biológicos sobre las fechas de los clientes: anula 
    fechas de nacimiento inverosímiles (edades fuera del rango de 0 a 100 años) y rectifica 
    anacronismos donde el registro del usuario sea anterior a su nacimiento.
    """
    df = clientes_df.copy()
    df["fecha_nacimiento"] = pd.to_datetime(df["fecha_nacimiento"], errors="coerce")
    df["fecha_registro"] = pd.to_datetime(df["fecha_registro"], errors="coerce")
    
    anio_actual = pd.Timestamp.now().year
    edades = anio_actual - df["fecha_nacimiento"].dt.year
    mask_edad_imposible = (edades < 0) | (edades > 100)
    if mask_edad_imposible.any():
        logger.warning(f"[CLEAN][BUSINESS RULES][dim_clientes] Se neutralizaron {mask_edad_imposible.sum()} fechas de nacimiento fuera del rango (0-100 años).")
        df.loc[mask_edad_imposible, "fecha_nacimiento"] = pd.NaT
        
    mask_anacronismo = df["fecha_registro"] < df["fecha_nacimiento"]
    if mask_anacronismo.any():
        logger.warning(f"[CLEAN][BUSINESS RULES][dim_clientes] Se corrigieron {mask_anacronismo.sum()} anacronismos en fechas de registro.")
        df.loc[mask_anacronismo, "fecha_registro"] = df.loc[mask_anacronismo, "fecha_nacimiento"]
    return df

def handle_business_rules_pedidos(pedidos_df: pd.DataFrame) -> pd.DataFrame:
    """
    Audita y corrige los costos logísticos forzando la gratuidad reglamentaria (órdenes canceladas 
    o retiros en tienda) e imputando valores faltantes o erróneos mediante la mediana calculada 
    según el año fiscal y la modalidad de entrega.
    """
    df = pedidos_df.copy()
    
    df.loc[df["estado_pedido"] == "Cancelado", "costo_envio"] = 0.0
    df.loc[df["tipo_envio"] == "Retiro En Tienda", "costo_envio"] = 0.0
    
    mask_logistica_rota = (df["tipo_envio"] != "Retiro En Tienda") & \
                          (df["estado_pedido"].isin(["Entregado", "Devuelto"])) & \
                          (df["costo_envio"] <= 0)
                          
    if mask_logistica_rota.any():
        logger.warning(f"[CLEAN][BUSINESS RULES][fact_pedidos] Se reajustó el costo de envío en {mask_logistica_rota.sum()} pedidos entregados/devueltos con costo <= 0.")
        costo_positivo = df["costo_envio"].where(df["costo_envio"] > 0)
        mediana_grupo = df.assign(c=costo_positivo).groupby(["temporal_anio", "tipo_envio"])["c"].transform("median")
        fallback_anio = df.assign(c=costo_positivo).groupby(["temporal_anio"])["c"].transform("median")
        mediana_final = mediana_grupo.fillna(fallback_anio).fillna(1500.0)
        df.loc[mask_logistica_rota, "costo_envio"] = mediana_final[mask_logistica_rota]
        
    return df

def handle_business_rules_detalle(detalle_df: pd.DataFrame, productos_clean_df: pd.DataFrame) -> pd.DataFrame:
    """
    Valida variables operativas y financieras a nivel de línea transaccional: fuerza cantidades mínimas 
    positivas, repara precios o costos erróneos mediante medianas históricas grupales y calcula 
    un indicador analítico estratégico para transacciones con margen de ganancia negativo.
    """
    df = detalle_df.copy()
    df.loc[df["cantidad"] <= 0, "cantidad"] = 1
    
    # Evaluamos e imputamos sobre las variables base (precio_lista y costo_unitario)
    cols_evaluacion = ["precio_lista", "costo_unitario"]
    for col in cols_evaluacion:
        mask_erroneo = df[col] <= 0
        if mask_erroneo.any():
            logger.warning(f"[CLEAN][BUSINESS RULES][fact_detalle_pedidos] Se imputaron valores <= 0 en '{col}' ({mask_erroneo.sum()} filas).")
            valores_positivos = df[col].where(df[col] > 0)
            mediana_prod = df.assign(v=valores_positivos).groupby(["producto_id", "temporal_anio"])["v"].transform("median")
            
            df_m = df.merge(productos_clean_df[["producto_id", "categoria"]], on="producto_id", how="left")
            mediana_cat = df_m.assign(v=valores_positivos).groupby(["categoria", "temporal_anio"])["v"].transform("median")
            
            imputacion_directa = mediana_prod.fillna(mediana_cat).fillna(100.0)
            df.loc[mask_erroneo, col] = imputacion_directa[mask_erroneo]

    df["precio_unitario"] = (df["precio_lista"] * (1 - df["descuento_aplicado"].fillna(0))).round(2)
    df["flag_margen_negativo"] = (df["precio_unitario"] < df["costo_unitario"]).astype(int)
    
    # Limpieza final de la columna auxiliar
    if "temporal_anio" in df.columns:
        df = df.drop(columns=["temporal_anio"])
        
    return df

# =============================================================================
# INTEGRIDAD RELACIONAL
# =============================================================================

def handle_referential_integrity_pedidos(pedidos_df: pd.DataFrame, clientes_clean_df: pd.DataFrame) -> pd.DataFrame:
    """
    Verifica la integridad de las claves foráneas (FK) de clientes en pedidos. Preserva las filas 
    huérfanas vinculándolas al ID de contingencia (-1) para evitar la pérdida de métricas de facturación 
    global en los análisis subsecuentes.
    """
    df = pedidos_df.copy()
    clientes_validos = set(clientes_clean_df["cliente_id"].dropna().unique())
    clientes_validos.add(-1)

    mask_invalid_client = (~df["cliente_id"].isin(clientes_validos)) & df["cliente_id"].notna()
    invalid_client_count = mask_invalid_client.sum()

    if invalid_client_count > 0:
        df.loc[mask_invalid_client, "cliente_id"] = -1
        logger.warning(f"[CLEAN][REFERENTIAL INTEGRITY][fact_pedidos] {invalid_client_count} pedidos con cliente_id inexistente reasignados al ID de contingencia (-1).")

    return df

def handle_referential_integrity_detalle(detalle_df: pd.DataFrame, pedidos_clean_df: pd.DataFrame, productos_clean_df: pd.DataFrame) -> pd.DataFrame:
    """
    Ejecuta políticas estrictas de depuración relacional eliminando permanentemente aquellas 
    líneas transaccionales huérfanas que no posean una orden de compra o un ID de producto válido. 
    Ignoras nulos explícitamente para que sean tratados en su función correspondiente.
    """
    df = detalle_df.copy()
    
    pedidos_validos = set(pedidos_clean_df["pedido_id"].dropna().unique())
    mask_invalid_pedido = (~df["pedido_id"].isin(pedidos_validos)) & df["pedido_id"].notna()
    invalid_pedido_count = mask_invalid_pedido.sum()

    if invalid_pedido_count > 0:
        logger.warning(f"[CLEAN][REFERENTIAL INTEGRITY][fact_detalle_pedidos] Eliminadas {invalid_pedido_count} líneas huérfanas sin pedido padre.")
        df = df[~mask_invalid_pedido]

    productos_validos = set(productos_clean_df["producto_id"].dropna().unique())
    mask_invalid_prod = (~df["producto_id"].isin(productos_validos)) & df["producto_id"].notna()
    invalid_prod_count = mask_invalid_prod.sum()

    if invalid_prod_count > 0:
        logger.warning(f"[CLEAN][REFERENTIAL INTEGRITY][fact_detalle_pedidos] Eliminadas {invalid_prod_count} líneas por producto_id inexistente.")
        df = df[~mask_invalid_prod]

    return df

# =============================================================================
# FUNCIONES ORQUESTADORAS POR TABLA
# =============================================================================

def clean_productos(productos_df: pd.DataFrame) -> pd.DataFrame:
    """
    Orquesta el pipeline secuencial y aislado de calidad para la dimensión Productos.
    """
    df = normalize_text_columns(productos_df, nombre_tabla="dim_productos")
    df = clean_table_duplicates(df, "dim_productos", pk_subset=['producto_id'], business_subset=['nombre_producto', 'categoria', 'marca', 'gama'])
    df = handle_nulls_productos(df)
    df = handle_business_rules_productos(df) 
    return df

def clean_clientes(clientes_df: pd.DataFrame) -> pd.DataFrame:
    """
    Orquesta el pipeline secuencial y aislado de calidad para la dimensión Clientes.
    """
    df = normalize_text_columns(clientes_df, nombre_tabla="dim_clientes")
    df = clean_table_duplicates(df, "dim_clientes", pk_subset=['cliente_id'], business_subset=['nombre', 'apellido', 'fecha_nacimiento'])
    df = clean_date_columns(df, "dim_clientes", date_columns=["fecha_nacimiento", "fecha_registro"])
    df = handle_nulls_clientes(df)
    df = handle_business_rules_clientes(df) 
    return df

def clean_pedidos(pedidos_df: pd.DataFrame, clientes_clean_df: pd.DataFrame) -> pd.DataFrame:
    """
    Orquesta el pipeline secuencial de calidad e integridad relacional para los Hechos de Pedidos.
    """
    df = normalize_text_columns(pedidos_df, nombre_tabla="fact_pedidos")
    df = clean_table_duplicates(df, "fact_pedidos", pk_subset=['pedido_id'], business_subset=['cliente_id', 'fecha_pedido', 'canal_venta'])
    df = clean_date_columns(df, "fact_pedidos", date_columns=["fecha_pedido"])
    df = handle_referential_integrity_pedidos(df, clientes_clean_df)
    df = handle_nulls_pedidos(df)
    df = handle_business_rules_pedidos(df) 
    return df

def clean_detalle(detalle_df: pd.DataFrame, pedidos_clean_df: pd.DataFrame, productos_clean_df: pd.DataFrame) -> pd.DataFrame:
    """
    Orquesta el pipeline secuencial para las líneas transaccionales, aplicando el algoritmo de imputación económica.
    """
    df = normalize_text_columns(detalle_df, nombre_tabla="fact_detalle_pedidos")
    df = clean_table_duplicates(df, "fact_detalle_pedidos", pk_subset=['detalle_id'], business_subset=['pedido_id', 'producto_id'])
    df = handle_referential_integrity_detalle(df, pedidos_clean_df, productos_clean_df)
    df = handle_nulls_detalle(df, pedidos_clean_df, productos_clean_df)
    df = handle_business_rules_detalle(df, productos_clean_df) 
    return df

# =============================================================================
# FUNCIÓN MADRE (MASTER ORCHESTRATOR)
# =============================================================================

def clean_all_data(
    pedidos_raw: pd.DataFrame, 
    detalle_raw: pd.DataFrame, 
    clientes_raw: pd.DataFrame, 
    productos_raw: pd.DataFrame
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Orquestador maestro del módulo de limpieza. Ejecuta de forma ordenada e interdependiente 
    las reglas de negocio e integridad sobre todo el ecosistema de datos crudos de TechnoShop.
    """
    
    productos_clean = clean_productos(productos_raw)
    clientes_clean = clean_clientes(clientes_raw)
    pedidos_clean = clean_pedidos(pedidos_raw, clientes_clean)
    detalle_clean = clean_detalle(detalle_raw, pedidos_clean, productos_clean)

    if "temporal_anio" in pedidos_clean.columns:
        pedidos_clean = pedidos_clean.drop(columns=["temporal_anio"])
        
    return pedidos_clean, detalle_clean, clientes_clean, productos_clean
