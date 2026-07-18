import pandas as pd
import logging

logger = logging.getLogger(__name__)

# =============================================================================#
# FUNCIONES AUXILIARES GENERALES                                               #
# =============================================================================#

#===================================================#
# NORMALIZACION DE TEXTO                            #
#===================================================#
def normalize_text_columns(df: pd.DataFrame) -> pd.DataFrame: 
    """
    Estandariza columnas de tipo string eliminando espacios marginales, transformando 
    celdas vacías en nulos reales (NA) y aplicando formato según el rol de la columna:
    Upper para identificadores (`_id`) y Title para texto descriptivo general.
    """
    df = df.copy()
    text_cols = df.select_dtypes(include=["object", "string"]).columns

    for col in text_cols:
        before_nulls = df[col].isna().sum()

        df[col] = df[col].astype("string")
        df[col] = df[col].str.strip()
        df[col] = df[col].replace(r'^\s*$', pd.NA, regex=True)

        if not col.endswith("_id"):
            df[col] = df[col].str.title()
        else:
            df[col] = df[col].str.upper()

        after_nulls = df[col].isna().sum()
        new_nulls = after_nulls - before_nulls

        if new_nulls > 0:
            logger.warning(f"[{col}] {new_nulls} nuevos nulos generados tras limpiar celdas vacías.")

    return df

#===================================================#
# LIMPIEZA DE DUPLICADOS                            #
#===================================================#

def clean_table_duplicates(df: pd.DataFrame, nombre_tabla: str, pk_subset: list = None) -> pd.DataFrame:
    """
    Elimina duplicados de forma jerárquica: primero remueve registros idénticos 
    en todas sus columnas y, opcionalmente, resuelve colisiones críticas en el 
    subconjunto que compone la Clave Primaria (PK) preservando la primera ocurrencia.
    """
    total_inicial = len(df)
    df_clean = df.drop_duplicates(keep='first')
    
    if pk_subset:
        total_antes_pk = len(df_clean)
        df_clean = df_clean.drop_duplicates(subset=pk_subset, keep='first')
        colisiones = total_antes_pk - len(df_clean)
        
        if colisiones > 0:
            logger.warning(f"[{nombre_tabla}] Se eliminaron {colisiones} filas por colisión de ID en {pk_subset}.")
            
    total_final = len(df_clean)
    eliminados = total_inicial - total_final
    
    if eliminados > 0:
        logger.info(f"[{nombre_tabla}] Duplicados eliminados. Reducción: {total_inicial} -> {total_final} filas.")
        
    return df_clean

# ===================================================#
# TRATAMIENTO DE NULOS POR ENTIDAD                   #
# ===================================================#

def handle_nulls_productos(productos_df: pd.DataFrame) -> pd.DataFrame:
    """
    Sanea nulos en la dimensión productos: descarta registros sin identificador base, 
    imputa categorías ausentes con etiquetas por defecto y reconstruye dinámicamente 
    el nombre del producto combinando su marca e ID si el original no existe.
    """
    df = productos_df.copy()
    df = df.dropna(subset=["producto_id"])
    
    for col in ["categoria", "marca", "gama"]:
        df[col] = df[col].fillna("Sin Dato")
        
    mask_nombre_nulo = df["nombre_producto"].isna()
    if mask_nombre_nulo.any():
        df.loc[mask_nombre_nulo, "nombre_producto"] = (
            "Producto " + df.loc[mask_nombre_nulo, "marca"] + " - ID: " + df.loc[mask_nombre_nulo, "producto_id"].astype(str)
        )
    return df

def handle_nulls_clientes(clientes_df: pd.DataFrame) -> pd.DataFrame:
    """
    Sanea la dimensión clientes descartando registros inválidos sin ID e inyecta 
    un registro genérico de contingencia (ID: -1) que actuará como fallback para 
    transacciones huérfanas o de usuarios tipo Consumidor Final.
    """
    df = clientes_df.copy()
    df = df.dropna(subset=["cliente_id"])
    
    for col in ["nombre", "apellido", "genero", "ciudad", "provincia", "canal_adquisicion"]:
        df[col] = df[col].fillna("Sin Dato")
        
    if -1 not in df["cliente_id"].values:
        fila_invitado = pd.DataFrame([{
            "cliente_id": -1, "nombre": "Consumidor", "apellido": "Final", 
            "genero": "Sin Dato", "fecha_nacimiento": pd.NaT, "ciudad": "Sin Dato", 
            "provincia": "Sin Dato", "fecha_registro": pd.NaT, "canal_adquisicion": "Sin Dato"
        }])
        df = pd.concat([df, fila_invitado], ignore_index=True)
    return df

def handle_nulls_pedidos(pedidos_df: pd.DataFrame) -> pd.DataFrame:
    """
    Sanea la tabla de hechos de pedidos: asegura el enlace al cliente genérico de contingencia, 
    imputa constantes descriptivas a variables transaccionales y extrae un índice temporal anual 
    requerido para los procesos posteriores de imputación económica.
    """
    df = pedidos_df.copy()
    df = df.dropna(subset=["pedido_id"])
    df["cliente_id"] = df["cliente_id"].fillna(-1).astype(int)
    
    for col in ["canal_venta", "medio_pago", "estado_pedido", "tipo_envio"]:
        df[col] = df[col].fillna("Sin Dato")
    df["costo_envio"] = df["costo_envio"].fillna(0.0)

    df["temporal_anio"] = pd.to_datetime(df["fecha_pedido"], errors="coerce").dt.year
    df["temporal_anio"] = df["temporal_anio"].fillna(2024).astype(int)
    return df

def handle_nulls_detalle(detalle_df: pd.DataFrame, pedidos_clean_df: pd.DataFrame, productos_clean_df: pd.DataFrame) -> pd.DataFrame:
    """
    Algoritmo de imputación económica e inflacionaria para métricas monetarias en transacciones. 
    Resuelve vacíos cruzando precios de lista con tasas de descuento y, en su defecto, aplica 
    imputaciones basadas en la mediana histórica del producto o su categoría calculada por año.
    """
    df = detalle_df.copy()
    df = df.dropna(subset=["detalle_id", "pedido_id", "producto_id"])
    df["cantidad"] = df["cantidad"].fillna(1)

    df = df.merge(pedidos_clean_df[["pedido_id", "temporal_anio"]], on="pedido_id", how="left")
    df["temporal_anio"] = df["temporal_anio"].fillna(2024).astype(int)

    mask_precio_null = df["precio_unitario"].isna()
    mask_lista_ok = df["precio_lista"].notna() & df["descuento_aplicado"].notna()
    mask_reparacion_directa = mask_precio_null & mask_lista_ok
    
    if mask_reparacion_directa.any():
        df.loc[mask_reparacion_directa, "precio_unitario"] = (
            df.loc[mask_reparacion_directa, "precio_lista"] * 
            (1 - df.loc[mask_reparacion_directa, "descuento_aplicado"])
        ).round(2)

    medianas_producto_anio = df.groupby(["producto_id", "temporal_anio"])[["precio_lista", "precio_unitario", "costo_unitario"]].transform("median")
    df["precio_lista"] = df["precio_lista"].fillna(medianas_producto_anio["precio_lista"])
    df["precio_unitario"] = df["precio_unitario"].fillna(medianas_producto_anio["precio_unitario"])
    df["costo_unitario"] = df["costo_unitario"].fillna(medianas_producto_anio["costo_unitario"])

    if df[["precio_lista", "precio_unitario", "costo_unitario"]].isna().any().any():
        df = df.merge(productos_clean_df[["producto_id", "categoria"]], on="producto_id", how="left")
        df["categoria"] = df["categoria"].fillna("Sin Dato")
        
        medianas_cat_anio = df.groupby(["categoria", "temporal_anio"])[["precio_lista", "precio_unitario", "costo_unitario"]].transform("median")
        df["precio_lista"] = df["precio_lista"].fillna(medianas_cat_anio["precio_lista"])
        df["precio_unitario"] = df["precio_unitario"].fillna(medianas_cat_anio["precio_unitario"])
        df["costo_unitario"] = df["costo_unitario"].fillna(medianas_cat_anio["costo_unitario"])
        df = df.drop(columns=["categoria"])

    df = df.dropna(subset=["precio_lista", "precio_unitario", "costo_unitario"])
    df["precio_unitario"] = (df["precio_lista"] * (1 - df["descuento_aplicado"].fillna(0))).round(2)
    df = df.drop(columns=["temporal_anio"])
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
    
    anio_actual = 2026
    edades = anio_actual - df["fecha_nacimiento"].dt.year
    mask_edad_imposible = (edades < 0) | (edades > 100)
    if mask_edad_imposible.any():
        df.loc[mask_edad_imposible, "fecha_nacimiento"] = pd.NaT
        
    mask_anacronismo = df["fecha_registro"] < df["fecha_nacimiento"]
    if mask_anacronismo.any():
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
        costo_positivo = df["costo_envio"].where(df["costo_envio"] > 0)
        mediana_grupo = df.assign(c=costo_positivo).groupby(["temporal_anio", "tipo_envio"])["c"].transform("median")
        fallback_anio = df.assign(c=costo_positivo).groupby(["temporal_anio"])["c"].transform("median")
        mediana_final = mediana_grupo.fillna(fallback_anio).fillna(1500.0)
        df.loc[mask_logistica_rota, "costo_envio"] = mediana_final[mask_logistica_rota]
        
    return df

def handle_business_rules_detalle(detalle_df: pd.DataFrame, pedidos_clean_df: pd.DataFrame, productos_clean_df: pd.DataFrame) -> pd.DataFrame:
    """
    Valida variables operativas y financieras a nivel de línea transaccional: fuerza cantidades mínimas 
    positivas, repara precios o costos erróneos mediante medianas históricas grupales y calcula 
    un indicador analítico estratégico para transacciones con margen de ganancia negativo.
    """
    df = detalle_df.copy()
    df.loc[df["cantidad"] <= 0, "cantidad"] = 1
    
    df = df.merge(pedidos_clean_df[["pedido_id", "temporal_anio"]], on="pedido_id", how="left")
    df["temporal_anio"] = df["temporal_anio"].fillna(2024).astype(int)
    
    cols_economicas = ["precio_lista", "precio_unitario", "costo_unitario"]
    for col in cols_economicas:
        mask_erroneo = df[col] <= 0
        if mask_erroneo.any():
            valores_positivos = df[col].where(df[col] > 0)
            mediana_prod = df.assign(v=valores_positivos).groupby(["producto_id", "temporal_anio"])["v"].transform("median")
            
            df_m = df.merge(productos_clean_df[["producto_id", "categoria"]], on="producto_id", how="left")
            mediana_cat = df_m.assign(v=valores_positivos).groupby(["categoria", "temporal_anio"])["v"].transform("median")
            
            imputacion_directa = mediana_prod.fillna(mediana_cat).fillna(100.0)
            df.loc[mask_erroneo, col] = imputacion_directa[mask_erroneo]

    df["precio_unitario"] = (df["precio_lista"] * (1 - df["descuento_aplicado"].fillna(0))).round(2)
    df["flag_margen_negativo"] = (df["precio_unitario"] < df["costo_unitario"]).astype(int)
    df = df.drop(columns=["temporal_anio"])
    return df

# =============================================================================
# INTEGRIDAD RELACIONAL
# =============================================================================

def handle_referential_integrity_pedidos(pedidos_df: pd.DataFrame, clientes_clean_df: pd.DataFrame) -> pd.DataFrame:
    """
    Verifica la integridad de las claves foráneas (FK) de clientes en pedidos. Preserva las filas 
    huérfanas vinculándolas al ID de contingencia para evitar la pérdida de métricas de facturación 
    global en los análisis subsecuentes.
    """
    df = pedidos_df.copy()
    clientes_validos = set(clientes_clean_df["cliente_id"].dropna().unique())
    clientes_validos.add(-1)

    mask_invalid_client = (~df["cliente_id"].isin(clientes_validos)) & df["cliente_id"].notna()
    invalid_client_count = mask_invalid_client.sum()

    if invalid_client_count > 0:
        logger.warning(f"[fact_pedidos] {invalid_client_count} pedidos con cliente_id inexistente (se preservan por facturación).")

    return df

def handle_referential_integrity_detalle(detalle_df: pd.DataFrame, pedidos_clean_df: pd.DataFrame, productos_clean_df: pd.DataFrame) -> pd.DataFrame:
    """
    Ejecuta políticas estrictas de depuración relacional eliminando permanentemente aquellas 
    líneas transaccionales huérfanas que no posean una orden de compra o un ID de producto válido.
    """
    df = detalle_df.copy()
    
    pedidos_validos = set(pedidos_clean_df["pedido_id"].dropna().unique())
    mask_invalid_pedido = ~df["pedido_id"].isin(pedidos_validos)
    invalid_pedido_count = mask_invalid_pedido.sum()

    if invalid_pedido_count > 0:
        logger.warning(f"[fact_detalle_pedidos] Eliminadas {invalid_pedido_count} líneas huérfanas sin pedido padre.")
        df = df[~mask_invalid_pedido]

    productos_validos = set(productos_clean_df["producto_id"].dropna().unique())
    mask_invalid_prod = ~df["producto_id"].isin(productos_validos)
    invalid_prod_count = mask_invalid_prod.sum()

    if invalid_prod_count > 0:
        logger.warning(f"[fact_detalle_pedidos] Eliminadas {invalid_prod_count} líneas por producto_id inexistente.")
        df = df[~mask_invalid_prod]

    return df

# =============================================================================
# FUNCIONES ORQUESTADORAS POR TABLA
# =============================================================================

def clean_productos(productos_df: pd.DataFrame) -> pd.DataFrame:
    """
    Orquesta el pipeline secuencial y aislado de calidad para la dimensión Productos.
    """
    df = normalize_text_columns(productos_df)
    df = clean_table_duplicates(df, "dim_productos", pk_subset=['producto_id'])
    df = handle_nulls_productos(df)
    df = handle_business_rules_productos(df)
    return df

def clean_clientes(clientes_df: pd.DataFrame) -> pd.DataFrame:
    """
    Orquesta el pipeline secuencial y aislado de calidad para la dimensión Clientes.
    """
    df = normalize_text_columns(clientes_df)
    df = clean_table_duplicates(df, "dim_clientes", pk_subset=['cliente_id'])
    df = handle_nulls_clientes(df)
    df = handle_business_rules_clientes(df)
    return df

def clean_pedidos(pedidos_df: pd.DataFrame, clientes_clean_df: pd.DataFrame) -> pd.DataFrame:
    """
    Orquesta el pipeline secuencial de calidad e integridad relacional para los Hechos de Pedidos.
    """
    df = normalize_text_columns(pedidos_df)
    df = clean_table_duplicates(df, "fact_pedidos", pk_subset=['pedido_id'])
    df = handle_referential_integrity_pedidos(df, clientes_clean_df)
    df = handle_nulls_pedidos(df)
    df = handle_business_rules_pedidos(df)
    return df

def clean_detalle(detalle_df: pd.DataFrame, pedidos_clean_df: pd.DataFrame, productos_clean_df: pd.DataFrame) -> pd.DataFrame:
    """
    Orquesta el pipeline secuencial para las líneas transaccionales, aplicando el algoritmo de imputación económica.
    """
    df = normalize_text_columns(detalle_df)
    df = clean_table_duplicates(df, "fact_detalle_pedidos", pk_subset=['pedido_id', 'producto_id'])
    df = handle_referential_integrity_detalle(df, pedidos_clean_df, productos_clean_df)
    df = handle_nulls_detalle(df, pedidos_clean_df, productos_clean_df)
    df = handle_business_rules_detalle(df, pedidos_clean_df, productos_clean_df)
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