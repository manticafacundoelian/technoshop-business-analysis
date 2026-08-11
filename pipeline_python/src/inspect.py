import pandas as pd
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

#====================================================================================================#
#                                FUNCIONES DE INSPECCION (CHECKS)                                    #
#====================================================================================================#

# ----------------------------------------------------------------------------------------------------
# ESPACIOS EN BLANCO
# ----------------------------------------------------------------------------------------------------
def check_whitespace(df: pd.DataFrame, nombre_tabla: str) -> dict:
    """
    Analiza columnas de texto buscando espacios en bordes o campos compuestos solo por espacios.
    """
    result = {}
    text_cols = df.select_dtypes(include=['object', 'string']).columns
    
    for col in text_cols:
        # Espacios al inicio/final en textos que TIENEN contenido
        format_issues = int(df[col].str.contains(r'^\s+\S|\S\s+$', regex=True, na=False).sum())
        # Cadenas compuestas ÚNICAMENTE por espacios
        whitespace_only = int(df[col].str.contains(r'^\s+$', regex=True, na=False).sum())
        
        if format_issues > 0 or whitespace_only > 0:
            result[col] = {
                "format_issues": format_issues,
                "whitespace_only": whitespace_only
            }
            logger.warning(
                f"[INSPECT][WHITESPACE][{nombre_tabla}] Anomalías de espacios en '{col}': "
                f"{format_issues} en bordes, {whitespace_only} solo espacios."
            )
            
    return result

# ----------------------------------------------------------------------------------------------------
# DUPLICADOS
# ----------------------------------------------------------------------------------------------------
def check_table_duplicates(
    df: pd.DataFrame, 
    nombre_tabla: str, 
    pk_subset: list = None, 
    business_subset: list = None
) -> dict:
    """
    Audita duplicados exactos, por Clave Primaria y por Clave de Negocio.
    Devuelve la cantidad de filas sobrantes por cada tipo.
    Los resultados pueden superponerse: una fila duplicada exacta también
    puede ser detectada como duplicado de PK y de negocio.
    """
    result = {}
    
    # 1. Duplicados exactos (toda la fila idéntica)
    exact_dups = int(df.duplicated().sum())
    result["exact_duplicates"] = exact_dups
    if exact_dups > 0:
        logger.warning(f"[INSPECT][EXACT DUPLICATES][{nombre_tabla}] {exact_dups} filas exactamente duplicadas.")

    # 2. Duplicados en Clave Primaria
    if pk_subset:
        pk_dups = int(df.duplicated(subset=pk_subset).sum())
        result["pk_duplicates"] = pk_dups
        if pk_dups > 0:
            logger.warning(f"[INSPECT][PK DUPLICATES][{nombre_tabla}] {pk_dups} registros con ID (PK) duplicado.")

    # 3. Duplicados de Negocio
    if business_subset:
        biz_dups = int(df.duplicated(subset=business_subset).sum())
        result["business_duplicates"] = biz_dups
        if biz_dups > 0:
            logger.warning(f"[INSPECT][BUSINESS DUPLICATES][{nombre_tabla}] {biz_dups} posibles duplicados según clave de negocio.")

    return result


# ----------------------------------------------------------------------------------------------------
# VALORES NULOS
# ----------------------------------------------------------------------------------------------------
def check_nulls(df: pd.DataFrame, nombre_tabla: str) -> dict:
    """
    Detecta y cuenta la presencia de valores nulos por columna.
    """
    result = {}

    nulls = df.isnull().sum()

    for col, cantidad in nulls.items():
        if cantidad > 0:
            result[col] = int(cantidad)

            logger.warning(
                f"[INSPECT][NULLS][{nombre_tabla}] Valores nulos en '{col}': {cantidad}."
            )

    return result


# ----------------------------------------------------------------------------------------------------
# CONSISTENCIA CATEGÓRICA (CASE SENSITIVITY)
# ----------------------------------------------------------------------------------------------------
def check_categorical_consistency(df: pd.DataFrame, nombre_tabla: str, columns: list) -> dict:
    """
    Detecta si una columna tiene variantes de mayúsculas/minúsculas (ej: 'Online' vs 'online').
    """
    result = {}

    for col in columns:
        if col not in df.columns:
            continue

        series_clean = df[col].dropna().astype(str).str.strip()
        if series_clean.empty:
            continue
            
        unique_values = series_clean.unique().tolist()
        lower_values = set(val.lower() for val in unique_values)
        
        has_case_issue = len(unique_values) != len(lower_values)

        if has_case_issue:
            result[col] = {
                "unique_original": len(unique_values),
                "unique_case_insensitive": len(lower_values),
                "has_case_issue": True
            }
            logger.warning(f"[INSPECT][CATEGORICAL CONSISTENCY][{nombre_tabla}] Inconsistencia de mayúsculas/minúsculas en '{col}'.")

    return result

# ----------------------------------------------------------------------------------------------------
# VALIDACIÓN DE FECHAS
# ----------------------------------------------------------------------------------------------------
def check_dates(df: pd.DataFrame, nombre_tabla: str, date_columns: list) -> dict:
    """
    Detecta problemas de formato e inconsistencias temporales en columnas de fecha.
    """
    result = {}

    for col in date_columns:
        if col not in df.columns:
            continue

        series_raw = df[col].dropna()
        if series_raw.empty:
            continue

        # Intentamos parsear a datetime sin alterar la columna original
        series_parsed = pd.to_datetime(series_raw, errors="coerce")

        # 1. Detección de formatos no parseables (convertidos a NaT)
        invalid_format_count = int(series_parsed.isna().sum())

        # 2. Detección de fechas futuras (posteriores a hoy)
        valid_dates = series_parsed.dropna()
        future_dates_count = int((valid_dates > pd.Timestamp.now()).sum())

        if invalid_format_count > 0 or future_dates_count > 0:
            result[col] = {
                "invalid_format_count": invalid_format_count,
                "future_dates_count": future_dates_count
            }
            logger.warning(
                f"[INSPECT][DATES][{nombre_tabla}] Inconsistencias de fecha en '{col}': "
                f"{invalid_format_count} no parseables, {future_dates_count} en el futuro."
            )

    return result

# ----------------------------------------------------------------------------------------------------
# INTEGRIDAD REFERENCIAL (CLAVES FORÁNEAS)
# ----------------------------------------------------------------------------------------------------
def check_referential_integrity(
    pedidos_df: pd.DataFrame, 
    detalle_df: pd.DataFrame, 
    clientes_df: pd.DataFrame, 
    productos_df: pd.DataFrame
) -> dict:
    """
    Verifica que las claves foráneas existan en sus respectivas tablas dimensionales.
    Ignora valores nulos (asume que los nulos se miden en el check de nulos).
    """
    clientes_validos = set(clientes_df["cliente_id"].dropna().unique())
    productos_validos = set(productos_df["producto_id"].dropna().unique())
    pedidos_validos = set(pedidos_df["pedido_id"].dropna().unique())

    # Agregamos .notna() para evaluar SOLO filas donde la FK no es nula pero no existe en la dimensión
    mask_cliente_invalido = (~pedidos_df["cliente_id"].isin(clientes_validos)) & pedidos_df["cliente_id"].notna()
    mask_producto_invalido = (~detalle_df["producto_id"].isin(productos_validos)) & detalle_df["producto_id"].notna()
    mask_pedido_huerfano = (~detalle_df["pedido_id"].isin(pedidos_validos)) & detalle_df["pedido_id"].notna()

    fk_clientes_invalidos = int(mask_cliente_invalido.sum())
    fk_productos_invalidos = int(mask_producto_invalido.sum())
    fk_pedidos_huerfanos = int(mask_pedido_huerfano.sum())

    if fk_clientes_invalidos > 0:
        logger.warning(f"[INSPECT][REFERENTIAL INTEGRITY][fact_pedidos_raw] {fk_clientes_invalidos} pedidos con cliente_id inexistente.")
    if fk_productos_invalidos > 0:
        logger.warning(f"[INSPECT][REFERENTIAL INTEGRITY][fact_detalle_pedidos]{fk_productos_invalidos} detalles con producto_id inexistente.")
    if fk_pedidos_huerfanos > 0:
        logger.warning(f"[INSPECT][REFERENTIAL INTEGRITY][fact_detalle_pedidos] CRÍTICO: {fk_pedidos_huerfanos} detalles sin pedido padre.")

    return {
        "pedidos_sin_cliente": fk_clientes_invalidos,
        "detalles_sin_producto": fk_productos_invalidos,
        "detalles_sin_pedido_padre": fk_pedidos_huerfanos
    }

# ----------------------------------------------------------------------------------------------------
# REGLAS DE NEGOCIO (PEDIDOS)
# ----------------------------------------------------------------------------------------------------
def check_business_rules_pedidos(pedidos_df: pd.DataFrame, nombre_tabla: str) -> dict:
    """
    Valida incoherencias entre estado del pedido, tipo de envío y costos.
    """
    estado = pedidos_df["estado_pedido"].astype(str).str.strip().str.title()
    tipo_envio = pedidos_df["tipo_envio"].astype(str).str.strip().str.title()
    costo_envio = pedidos_df["costo_envio"]

    # Evaluamos solo sobre filas donde el costo Y el tipo de envío no sean nulos
    mask_costo_valido = costo_envio.notna()
    mask_envio_valido = pedidos_df["tipo_envio"].notna()

    cancelados_con_costo = int(((estado == "Cancelado") & (costo_envio > 0) & mask_costo_valido).sum())
    retiro_con_costo = int(((tipo_envio == "Retiro En Tienda") & (costo_envio > 0) & mask_costo_valido & mask_envio_valido).sum())
    
    # Agregamos mask_envio_valido para no asumir que un NaN es un envío a domicilio
    domicilio_sin_costo = int(((tipo_envio != "Retiro En Tienda") & mask_envio_valido & (estado.isin(["Entregado", "Devuelto"])) & (costo_envio <= 0) & mask_costo_valido).sum())

    if cancelados_con_costo > 0:
        logger.warning(f"[INSPECT][BUSINESS RULES][{nombre_tabla}] {cancelados_con_costo} pedidos CANCELADOS tienen costo de envío.")
    if retiro_con_costo > 0:
        logger.warning(f"[INSPECT][BUSINESS RULES][{nombre_tabla}] {retiro_con_costo} RETIROS EN TIENDA tienen costo de envío.")
    if domicilio_sin_costo > 0:
        logger.warning(f"[INSPECT][BUSINESS RULES][{nombre_tabla}] {domicilio_sin_costo} envíos a domicilio registran costo <= 0.")

    return {
        "cancelados_con_costo": cancelados_con_costo,
        "retiros_tienda_con_costo": retiro_con_costo,
        "domicilio_sin_costo": domicilio_sin_costo
    }


# ----------------------------------------------------------------------------------------------------
# REGLAS DE NEGOCIO (DETALLE)
# ----------------------------------------------------------------------------------------------------
def check_business_rules_detalle(detalle_df: pd.DataFrame, nombre_tabla: str) -> dict:
    """
    Valida cantidades, precios/costos y la ecuación matemática de descuentos.
    """
    cant_negativa = int((detalle_df["cantidad"] <= 0).sum())
    cant_extrema = int((detalle_df["cantidad"] > 10).sum())
    precios_invalidos = int(((detalle_df["precio_lista"] <= 0) | (detalle_df["precio_unitario"] <= 0) | (detalle_df["costo_unitario"] <= 0)).sum())
    margen_negativo = int((detalle_df["precio_unitario"] < detalle_df["costo_unitario"]).sum())
    
    # Mascara para evaluar la ecuación de descuento SOLO en filas con precios completos (sin NaNs)
    mask_precios_completos = (
        detalle_df["precio_lista"].notna() & 
        detalle_df["precio_unitario"].notna() & 
        detalle_df["descuento_aplicado"].notna()
    )
    
    df_precios = detalle_df[mask_precios_completos]
    calculo_precio_real = (df_precios["precio_lista"] * (1 - df_precios["descuento_aplicado"])).round(2)
    precio_unitario_redondeado = df_precios["precio_unitario"].round(2)
    inconsistencia_descuento = int((calculo_precio_real != precio_unitario_redondeado).sum())

    if cant_negativa > 0:
        logger.warning(f"[INSPECT][BUSINESS RULES][{nombre_tabla}] {cant_negativa} líneas con cantidad inválida (<= 0).")
    if cant_extrema > 0:
        logger.warning(f"[INSPECT][BUSINESS RULES][{nombre_tabla}] {cant_extrema} líneas con cantidades extremas (> 10).")
    if precios_invalidos > 0:
        logger.warning(f"[INSPECT][BUSINESS RULES][{nombre_tabla}] {precios_invalidos} registros con precios/costos <= 0.")
    if margen_negativo > 0:
        logger.warning(f"[INSPECT][BUSINESS RULES][{nombre_tabla}] {margen_negativo} líneas con MARGEN NEGATIVO.")
    if inconsistencia_descuento > 0:
        logger.warning(f"[INSPECT][BUSINESS RULES][{nombre_tabla}] {inconsistencia_descuento} errores en ecuación de descuento.")

    return {
        "cantidades_invalidas": cant_negativa,
        "cantidades_extremas": cant_extrema,
        "precios_o_costos_invalidos": precios_invalidos,
        "margen_negativo": margen_negativo,
        "descuentos_incoherentes": inconsistencia_descuento
    }


# ----------------------------------------------------------------------------------------------------
# REGLAS DE NEGOCIO (CLIENTES)
# ----------------------------------------------------------------------------------------------------
def check_business_rules_clientes(clientes_df: pd.DataFrame, nombre_tabla: str) -> dict:
    """
    Audita fechas de nacimiento y registro buscando incongruencias temporales o de edad.
    """
    fechas_nac = pd.to_datetime(clientes_df["fecha_nacimiento"], errors='coerce')
    fechas_reg = pd.to_datetime(clientes_df["fecha_registro"], errors='coerce')

    # Usamos pd.Timestamp.now().year para no depender de imports externos
    anio_actual = pd.Timestamp.now().year
    edades = anio_actual - fechas_nac.dt.year

    edad_negativa = int((edades < 0).sum())
    edad_extrema = int((edades > 100).sum())
    menores_de_edad = int((edades < 18).sum()) 
    registro_antes_de_nacer = int((fechas_reg < fechas_nac).sum())

    if edad_negativa > 0:
        logger.warning(f"[INSPECT][BUSINESS RULES][{nombre_tabla}] {edad_negativa} clientes con nacimiento en el futuro.")
    if edad_extrema > 0:
        logger.warning(f"[INSPECT][BUSINESS RULES][{nombre_tabla}] {edad_extrema} clientes con edades extremas (> 100).")
    if menores_de_edad > 0:
        logger.warning(f"[INSPECT][BUSINESS RULES][{nombre_tabla}] {menores_de_edad} clientes son menores de edad.")
    if registro_antes_de_nacer > 0:
        logger.warning(f"[INSPECT][BUSINESS RULES][{nombre_tabla}] {registro_antes_de_nacer} registros previos al nacimiento.")

    return {
        "edad_negativa": edad_negativa,
        "edad_mayor_100": edad_extrema,
        "menores_de_edad": menores_de_edad,
        "registro_previo_nacimiento": registro_antes_de_nacer
    }

# ----------------------------------------------------------------------------------------------------
# REGLAS DE NEGOCIO (PRODUCTOS)
# ----------------------------------------------------------------------------------------------------
def check_business_rules_productos(
    productos_df: pd.DataFrame,
    nombre_tabla: str
) -> dict:
    """
    Valida que la gama de productos pertenezca al dominio permitido.
    """
    gamas_validas = ["alta", "media", "baja"]

    gama_normalizada = (productos_df["gama"].astype("string").str.strip().str.lower())
    mask_gama_invalida = (productos_df["gama"].notna()& ~gama_normalizada.isin(gamas_validas))
    gama_invalida = int(mask_gama_invalida.sum())

    if gama_invalida > 0:
        logger.warning(
            f"[INSPECT][BUSINESS RULES][{nombre_tabla}] "
            f"{gama_invalida} productos con gamas no reconocidas."
        )

    return {
        "gamas_invalidas": gama_invalida
    }

# ===================================================================================================#
#                                ORQUESTADOR PRINCIPAL DEL MÓDULO                                    #
# ===================================================================================================#

def inspect_data(
    pedidos_raw: pd.DataFrame, 
    detalle_raw: pd.DataFrame, 
    clientes_raw: pd.DataFrame, 
    productos_raw: pd.DataFrame
) -> dict:
    """
    Ejecuta la inspección completa y devuelve un resumen limpio con los conteos de errores.
    """
    report = {
        "fact_pedidos": {
            "whitespace": check_whitespace(pedidos_raw, "fact_pedidos"),
            "duplicates": check_table_duplicates(pedidos_raw, "fact_pedidos", pk_subset=['pedido_id'], business_subset=['cliente_id', 'fecha_pedido', 'canal_venta']),
            "nulls": check_nulls(pedidos_raw, "fact_pedidos"),
            "categorical_consistency": check_categorical_consistency(pedidos_raw, "fact_pedidos", ["canal_venta", "medio_pago", "estado_pedido", "tipo_envio"]),
            "dates": check_dates(pedidos_raw, "fact_pedidos", ["fecha_pedido"]),
            "business_rules": check_business_rules_pedidos(pedidos_raw, "fact_pedidos")
        },
        "fact_detalle_pedidos": {
            "whitespace": check_whitespace(detalle_raw, "fact_detalle_pedidos"),
            "duplicates": check_table_duplicates(detalle_raw, "fact_detalle_pedidos", pk_subset=['detalle_id'], business_subset=['pedido_id', 'producto_id']),
            "nulls": check_nulls(detalle_raw, "fact_detalle_pedidos"),
            "categorical_consistency": check_categorical_consistency(detalle_raw, "fact_detalle_pedidos", []),
            "dates": check_dates(detalle_raw, "fact_detalle_pedidos", []),
            "business_rules": check_business_rules_detalle(detalle_raw, "fact_detalle_pedidos")
        },
        "dim_clientes": {
            "whitespace": check_whitespace(clientes_raw, "dim_clientes"),
            "duplicates": check_table_duplicates(clientes_raw, "dim_clientes", pk_subset=['cliente_id'], business_subset=['nombre', 'apellido', 'fecha_nacimiento']),
            "nulls": check_nulls(clientes_raw, "dim_clientes"),
            "categorical_consistency": check_categorical_consistency(clientes_raw, "dim_clientes", ["genero", "ciudad", "provincia", "canal_adquisicion"]),
            "dates": check_dates(clientes_raw, "dim_clientes", ["fecha_nacimiento", "fecha_registro"]),
            "business_rules": check_business_rules_clientes(clientes_raw, "dim_clientes")
        },
        "dim_productos": {
            "whitespace": check_whitespace(productos_raw, "dim_productos"),
            "duplicates": check_table_duplicates(productos_raw, "dim_productos", pk_subset=['producto_id'], business_subset=['nombre_producto', 'categoria', 'marca', 'gama']),
            "nulls": check_nulls(productos_raw, "dim_productos"),
            "categorical_consistency": check_categorical_consistency(productos_raw, "dim_productos", ["categoria", "marca", "gama"]),
            "dates": check_dates(productos_raw, "dim_productos", []),
            "business_rules": check_business_rules_productos(productos_raw, "dim_productos")
        },
        "relational_integrity": check_referential_integrity(pedidos_raw, detalle_raw, clientes_raw, productos_raw)
    }

    return report
