import pandas as pd
import logging
import re
from datetime import datetime

logger = logging.getLogger(__name__)

def build_metric(count: int, total: int) -> dict:
    """
    Calcula el porcentaje de impacto de un problema y le asigna una severidad.
    """
    pct = count / total if total > 0 else 0

    if pct == 0:
        severity = "ok"
    elif pct < 0.01:
        severity = "low"
    elif pct < 0.05:
        severity = "medium"
    else:
        severity = "high"

    return {
        "count": int(count),
        "pct": round(pct, 4),
        "severity": severity
    }

#====================================================================================================#
#                     FUNCIONES AUXILIARES DE INSPECCION (CHECKS)                                    #
#====================================================================================================#

#================================================================#
#                    CAPA DE INTEGRIDAD TÉCNICA                  #
#================================================================#

#===================================================#
# FUNCION ESPACIOS EN BLANCO                        #
#===================================================#

def check_whitespace(df: pd.DataFrame, nombre_tabla: str) -> dict:
    """
    Analiza columnas de texto buscando espacios al inicio/final o campos vacíos.
    """
    result = {}
    total = len(df)
    
    text_cols = df.select_dtypes(include=['object', 'string']).columns
    
    for col in text_cols:
        format_issues = df[col].str.contains(r'^\s+|\s+$', regex=True, na=False).sum()
        whitespace_only = df[col].str.contains(r'^\s+$', regex=True, na=False).sum()
        
        if format_issues > 0 or whitespace_only > 0:
            result[col] = {
                "format_issues": build_metric(format_issues, total),
                "whitespace_only": build_metric(whitespace_only, total)
            }
            logger.warning(
                f"[{nombre_tabla}] Anomalías de espacios en '{col}': "
                f"{format_issues} extra, {whitespace_only} solo espacios."
            )
            
    return result

#===================================================#
# FUNCION DUPLICADOS                                #
#===================================================#

def check_table_duplicates(
    df: pd.DataFrame, 
    nombre_tabla: str, 
    pk_subset: list = None, 
    business_subset: list = None, 
    normalize: bool = False
) -> dict:
    """
    Audita duplicados en 3 capas independientes, porque cada una detecta un
    problema distinto y ninguna reemplaza a las otras:
 
    1. Exactos: fila idéntica en todas sus columnas (el caso más obvio).
    2. Clave primaria (pk_subset): mismo ID repetido. Se separa el subconjunto
       "pk_semantic_only" (mismo ID pero con datos distintos) porque ese caso
       es más grave que un duplicado exacto: indica una colisión real de
       identidad, no una simple repetición de carga.
    3. Negocio (business_subset): mismo evento de negocio bajo IDs distintos
       (ej. mismo cliente/fecha/monto con dos pedido_id diferentes), que las
       dos capas anteriores no pueden detectar por sí solas.
 
    El flag `normalize` decide si la comparación de texto ignora mayúsculas
    y espacios antes de buscar duplicados. Se buscan duplicados crudos y normalizados.
    """
    type_label = "NORMALIZADO" if normalize else "RAW"
    result = {}
    total = len(df)
    
    if total == 0:
        return result

    df_analysis = df.copy()
    
    if normalize:
        text_cols = df_analysis.select_dtypes(include=['object', 'string']).columns
        for col in text_cols:
            df_analysis[col] = df_analysis[col].astype(str).str.strip().str.lower()

    # Capa 1: Duplicados exactos
    exact_dups = df_analysis.duplicated().sum()
    result["exact_duplicates"] = build_metric(exact_dups, total)
    
    if exact_dups > 0:
        logger.warning(f"[{nombre_tabla}][{type_label}] {exact_dups} filas exactamente duplicadas.")

    # Capa 2: Integridad de Clave Primaria
    if pk_subset:
        total_pk_dups = df_analysis.duplicated(subset=pk_subset).sum()
        pk_semantic_only = total_pk_dups - exact_dups
        
        result["pk_duplicates_total"] = build_metric(total_pk_dups, total)
        result["pk_semantic_only"] = build_metric(pk_semantic_only, total)
        
        if total_pk_dups > 0:
            logger.warning(
                f"[{nombre_tabla}][{type_label}] {total_pk_dups} IDs duplicados "
                f"({pk_semantic_only} colisiones reales con datos distintos)."
            )

    # Capa 3: Duplicados de Negocio
    if business_subset:
        total_biz_dups = df_analysis.duplicated(subset=business_subset).sum()
        biz_semantic_only = total_biz_dups - exact_dups
        
        result["business_duplicates_total"] = build_metric(total_biz_dups, total)
        result["business_semantic_only"] = build_metric(biz_semantic_only, total)
        
        if total_biz_dups > 0:
            logger.warning(
                f"[{nombre_tabla}][{type_label}] {total_biz_dups} duplicados semánticos "
                f"({biz_semantic_only} con distinto ID)."
            )

    return result

#===================================================#
# FUNCION NULOS                                     #
#===================================================#

def check_nulls(df: pd.DataFrame, nombre_tabla: str) -> dict:
    """
    Detecta y cuantifica la presencia de valores nulos o faltantes.
    """
    result = {}
    total = len(df)
    nulls = df.isnull().sum()
    nulls = nulls[nulls > 0]

    if not nulls.empty:
        result = {col: build_metric(count, total) for col, count in nulls.to_dict().items()}
        null_summary = {col: int(count) for col, count in nulls.to_dict().items()}
        logger.warning(f"[{nombre_tabla}] Nulos detectados: {null_summary}")

    return result

#===================================================#
# FUNCION CONSISTENCIA DE CASE (CATEGÓRICOS)        #
#===================================================#

def check_categorical_consistency(df: pd.DataFrame, nombre_tabla: str, columns: list) -> dict:
    """
    Detecta si una misma columna categórica tiene el mismo valor escrito con
    distinto casing (ej. "Online" y "online" conviviendo como si fueran
    categorías distintas). Compara la cantidad de valores únicos "tal cual"
    contra la cantidad de únicos "en minúscula": si difieren, hay variantes
    de mayúsculas que un merge o un GROUP BY tratarían como categorías
    separadas sin que nadie lo note a simple vista.
    """
    result = {}

    for col in columns:
        if col not in df.columns:
            logger.warning(f"[{nombre_tabla}] Columna '{col}' no existe para validación categórica.")
            continue

        series_clean = df[col].dropna().astype(str)
        if series_clean.empty:
            continue
            
        value_counts = series_clean.value_counts()
        unique_values = value_counts.index.tolist()
        
        lower_seen = set()
        has_case_issue = False
        for val in unique_values:
            val_lower = val.lower()
            if val_lower in lower_seen:
                has_case_issue = True
            lower_seen.add(val_lower)

        dominant_value = value_counts.idxmax()
        dominant_freq = int(value_counts.max()) 

        result[col] = {
            "n_unique": len(unique_values),
            "unique_values_sample": sorted(unique_values)[:20],
            "case_insensitive_unique": len(lower_seen),
            "case_variants_detected": has_case_issue,
            "dominant_value": dominant_value,
            "dominant_freq": dominant_freq
        }

        if has_case_issue:
            logger.warning(f"[{nombre_tabla}] Inconsistencia de mayúsculas/minúsculas en '{col}'.")

    return result

#================================================================#
#                    CAPA DE REGLAS DE NEGOCIO                   #
#================================================================#

# REGLAS DE NEGOCIO PEDIDOS 
def check_business_rules_pedidos(pedidos_df: pd.DataFrame) -> dict:
    """
    Valida combinaciones de estado/envío/costo que no deberían darse juntas
    en un negocio bien registrado:
      - Un pedido Cancelado no debería tener costo de envío (nunca se despachó).
      - Un Retiro en Tienda no debería tener costo de envío (no hay logística).
      - Un envío a domicilio de un pedido Entregado o Devuelto sí debería
        tener costo de envío > 0; si registra 0, probablemente el dato se
        perdió o no se cargó, no que el envío haya sido gratis.
    """
    total = len(pedidos_df)
    error_estado = pedidos_df["estado_pedido"].astype(str).str.strip().str.title()
    tipo_envio = pedidos_df["tipo_envio"].astype(str).str.strip().str.title()
    costo_envio = pedidos_df["costo_envio"]

    cancelados_con_costo = ((error_estado == "Cancelado") & (costo_envio > 0)).sum()
    retiro_con_costo = ((tipo_envio == "Retiro En Tienda") & (costo_envio > 0)).sum()
    domicilio_sin_costo = ((tipo_envio != "Retiro En Tienda") & (error_estado.isin(["Entregado", "Devuelto"])) & (costo_envio <= 0)).sum()

    if cancelados_con_costo > 0:
        logger.warning(f"[fact_pedidos] {cancelados_con_costo} pedidos CANCELADOS tienen costo de envío.")
    if retiro_con_costo > 0:
        logger.warning(f"[fact_pedidos] {retiro_con_costo} RETIROS EN TIENDA tienen costo de envío.")
    if domicilio_sin_costo > 0:
        logger.warning(f"[fact_pedidos] {domicilio_sin_costo} envíos a domicilio registran costo 0.")

    return {
        "envios_y_estados": {
            "cancelados_con_costo_erroneo": build_metric(cancelados_con_costo, total),
            "retiros_tienda_con_costo_erroneo": build_metric(retiro_con_costo, total),
            "domicilio_con_costo_omitido": build_metric(domicilio_sin_costo, total)
        }
    }

# REGLAS DE NEGOCIO DETALLE
def check_business_rules_detalle(detalle_df: pd.DataFrame) -> dict:
    """
    Valida cantidades, precios/costos y la ecuación de descuento del detalle.
    El chequeo de descuento recalcula precio_lista * (1 - descuento_aplicado)
    y lo compara contra precio_unitario ya cargado: si no coinciden (más allá
    del redondeo a 2 decimales), el descuento registrado no es el que
    realmente se aplicó al precio final, señal de un error de carga o de
    cálculo en el origen de los datos, no una simple diferencia de redondeo.
    """
    total = len(detalle_df)
    cant_negativa = (detalle_df["cantidad"] <= 0).sum()
    cant_extrema = (detalle_df["cantidad"] > 10).sum()
    precios_invalidos = ((detalle_df["precio_lista"] <= 0) | (detalle_df["precio_unitario"] <= 0) | (detalle_df["costo_unitario"] <= 0)).sum()
    margen_negativo = (detalle_df["precio_unitario"] < detalle_df["costo_unitario"]).sum()
    
    calculo_precio_real = (detalle_df["precio_lista"] * (1 - detalle_df["descuento_aplicado"])).round(2)
    precio_unitario_redondeado = detalle_df["precio_unitario"].round(2)
    inconsistencia_descuento = (calculo_precio_real != precio_unitario_redondeado).sum()

    if cant_negativa > 0:
        logger.warning(f"[fact_detalle_pedidos] {cant_negativa} líneas con cantidad inválida (<= 0).")
    if cant_extrema > 0:
        logger.warning(f"[fact_detalle_pedidos] {cant_extrema} líneas con cantidades extremas (> 10).")
    if precios_invalidos > 0:
        logger.warning(f"[fact_detalle_pedidos] {precios_invalidos} registros con precios/costos <= 0.")
    if margen_negativo > 0:
        logger.warning(f"[fact_detalle_pedidos] {margen_negativo} líneas con MARGEN NEGATIVO.")
    if inconsistencia_descuento > 0:
        logger.warning(f"[fact_detalle_pedidos] {inconsistencia_descuento} errores en ecuación de descuento.")

    return {
        "cantidades": {
            "invalidas_menor_cero": build_metric(cant_negativa, total),
            "extremas_mayor_diez": build_metric(cant_extrema, total)
        },
        "precios_y_costos": {
            "valores_menor_o_igual_cero": build_metric(precios_invalidos, total),
            "calculo_descuento_incoherente": build_metric(inconsistencia_descuento, total)
        },
        "margen_negativo_unitario": build_metric(margen_negativo, total)
    }

# REGLAS DE NEGOCIO CLIENTES
def check_business_rules_clientes(clientes_df: pd.DataFrame) -> dict:
    """
    Audita fechas de clientes buscando tanto errores de formato (fechas que
    no parsean) como inconsistencias lógicas: nacimiento en el futuro, edades
    imposibles (>100), registro anterior al propio nacimiento, o clientes
    menores de edad (esto último se reporta como dato a revisar, no
    necesariamente un error del dataset, según la política comercial vigente).
    """
    total = len(clientes_df)
    fechas_nac = pd.to_datetime(clientes_df["fecha_nacimiento"], errors='coerce')
    fechas_reg = pd.to_datetime(clientes_df["fecha_registro"], errors='coerce')

    fechas_nac_invalidas = fechas_nac.isna().sum()
    fechas_reg_invalidas = fechas_reg.isna().sum()

    anio_actual = datetime.now().year
    edades = anio_actual - fechas_nac.dt.year

    edad_negativa = (edades < 0).sum()
    edad_extrema = (edades > 100).sum()
    menores_de_edad = (edades < 18).sum() 
    registro_antes_de_nacer = (fechas_reg < fechas_nac).sum()

    if fechas_nac_invalidas > 0 or fechas_reg_invalidas > 0:
        logger.warning(f"[dim_clientes] Fechas corruptas (Nac: {fechas_nac_invalidas}, Reg: {fechas_reg_invalidas}).")
    if edad_negativa > 0:
        logger.warning(f"[dim_clientes] {edad_negativa} clientes con nacimiento en el futuro.")
    if edad_extrema > 0:
        logger.warning(f"[dim_clientes] {edad_extrema} clientes con edades extremas (> 100).")
    if menores_de_edad > 0:
        logger.warning(f"[dim_clientes] {menores_de_edad} clientes son menores de edad.")
    if registro_antes_de_nacer > 0:
        logger.warning(f"[dim_clientes] {registro_antes_de_nacer} registros previos al nacimiento.")

    return {
        "integridad_fechas": {
            "nacimiento_invalido_o_nulo": build_metric(fechas_nac_invalidas, total),
            "registro_invalido_o_nulo": build_metric(fechas_reg_invalidas, total)
        },
        "edad_actual": {
            "negativas_comerciales": build_metric(edad_negativa, total),
            "mayores_de_100_anios": build_metric(edad_extrema, total),
            "menores_de_18_anios": build_metric(menores_de_edad, total)
        },
        "consistencia_temporal": {
            "registro_previo_a_nacimiento": build_metric(registro_antes_de_nacer, total)
        }
    }

# REGLAS DE NEGOCIO PRODUCTOS
def check_business_rules_productos(productos_df: pd.DataFrame) -> dict:
    """
    Valida que la columna 'gama' solo contenga los valores del dominio cerrado (alta/media/baja).
    """
    total = len(productos_df)
    gamas_validas = ["alta", "media", "baja"]
    gama_invalida = (~productos_df["gama"].astype(str).str.lower().isin(gamas_validas)).sum()

    if gama_invalida > 0:
        logger.warning(f"[dim_productos] {gama_invalida} productos con gamas no reconocidas.")

    return {
        "consistencia_catalogo": {
            "gamas_fuera_de_estandar": build_metric(gama_invalida, total)
        }
    }

#================================================================#
#                  CAPA DE INTEGRIDAD RELACIONAL                 #
#================================================================#

def check_referential_integrity(
    pedidos_df: pd.DataFrame, 
    detalle_df: pd.DataFrame, 
    clientes_df: pd.DataFrame, 
    productos_df: pd.DataFrame
) -> dict:
    """
    Audita, de solo lectura, que las claves foráneas de pedidos y detalle
    apunten a filas que realmente existen en sus dimensiones/tabla padre.
    No corrige nada: el objetivo es dimensionar el problema antes de decidir,
    en una etapa posterior del pipeline, si esos registros se preservan,
    se descartan o se marcan.
 
    El caso "detalles_huerfanos_sin_pedido_padre" se loguea como CRÍTICO y no
    solo como advertencia porque, a diferencia de un cliente o producto
    inexistente (que aún así corresponde a una venta real), una línea de
    detalle sin pedido padre no tiene forma de asociarse a ninguna
    transacción válida: es un registro sin fecha, canal ni estado propios.
    """
    total_pedidos = len(pedidos_df)
    total_detalles = len(detalle_df)

    clientes_validos = set(clientes_df["cliente_id"].dropna().unique())
    productos_validos = set(productos_df["producto_id"].dropna().unique())
    pedidos_validos = set(pedidos_df["pedido_id"].dropna().unique())

    fk_clientes_invalidos = (~pedidos_df["cliente_id"].isin(clientes_validos)).sum()
    fk_productos_invalidos = (~detalle_df["producto_id"].isin(productos_validos)).sum()
    fk_pedidos_en_detalle_invalidos = (~detalle_df["pedido_id"].isin(pedidos_validos)).sum()

    if fk_clientes_invalidos > 0:
        logger.warning(f"[Integridad FK] {fk_clientes_invalidos} pedidos con cliente_id inexistente.")
    if fk_productos_invalidos > 0:
        logger.warning(f"[Integridad FK] {fk_productos_invalidos} detalles con producto_id inexistente.")
    if fk_pedidos_en_detalle_invalidos > 0:
        logger.warning(f"[Integridad FK] CRÍTICO: {fk_pedidos_en_detalle_invalidos} detalles sin pedido padre.")

    return {
        "pedidos_con_cliente_invalido": build_metric(fk_clientes_invalidos, total_pedidos),
        "detalles_con_producto_invalido": build_metric(fk_productos_invalidos, total_detalles),
        "detalles_huerfanos_sin_pedido_padre": build_metric(fk_pedidos_en_detalle_invalidos, total_detalles)
    }

# =============================================================================#
#                     ORQUESTADOR PRINCIPAL DEL MÓDULO
# =============================================================================#

def inspect_data(
    pedidos_raw: pd.DataFrame, 
    detalle_raw: pd.DataFrame, 
    clientes_raw: pd.DataFrame, 
    productos_raw: pd.DataFrame
) -> dict:
    """
    Ejecuta la auditoría integral de datos.
    """
    report = {
        "fact_pedidos": {},
        "fact_detalle_pedidos": {},
        "dim_clientes": {},
        "dim_productos": {},
        "business_rules": {}
    }
    
    # 1. Espacios en blanco
    report["fact_pedidos"]["whitespace"] = check_whitespace(pedidos_raw, "fact_pedidos")
    report["fact_detalle_pedidos"]["whitespace"] = check_whitespace(detalle_raw, "fact_detalle_pedidos")
    report["dim_clientes"]["whitespace"] = check_whitespace(clientes_raw, "dim_clientes")
    report["dim_productos"]["whitespace"] = check_whitespace(productos_raw, "dim_productos")

    # 2. Duplicados 
    pk_pedidos = ['pedido_id']
    pk_detalle = ['pedido_id', 'producto_id']
    pk_clientes = ['cliente_id']
    pk_productos = ['producto_id']
    
    subset_clientes_negocio = ['nombre', 'apellido', 'fecha_nacimiento']
    subset_productos_negocio = ['nombre_producto', 'categoria', 'marca', 'gama']

    report["fact_pedidos"]["duplicates_raw"] = check_table_duplicates(pedidos_raw, "fact_pedidos", pk_subset=pk_pedidos, normalize=False)
    report["fact_pedidos"]["duplicates_normalized"] = check_table_duplicates(pedidos_raw, "fact_pedidos", pk_subset=pk_pedidos, normalize=True)
    report["fact_detalle_pedidos"]["duplicates_raw"] = check_table_duplicates(detalle_raw, "fact_detalle_pedidos", pk_subset=pk_detalle, normalize=False)
    report["fact_detalle_pedidos"]["duplicates_normalized"] = check_table_duplicates(detalle_raw, "fact_detalle_pedidos", pk_subset=pk_detalle, normalize=True)
    report["dim_clientes"]["duplicates_raw"] = check_table_duplicates(clientes_raw, "dim_clientes", pk_subset=pk_clientes, business_subset=subset_clientes_negocio, normalize=False)
    report["dim_clientes"]["duplicates_normalized"] = check_table_duplicates(clientes_raw, "dim_clientes", pk_subset=pk_clientes, business_subset=subset_clientes_negocio, normalize=True)
    report["dim_productos"]["duplicates_raw"] = check_table_duplicates(productos_raw, "dim_productos", pk_subset=pk_productos, business_subset=subset_productos_negocio, normalize=False)
    report["dim_productos"]["duplicates_normalized"] = check_table_duplicates(productos_raw, "dim_productos", pk_subset=pk_productos, business_subset=subset_productos_negocio, normalize=True)
    
    # 3. Nulos
    report["fact_pedidos"]["nulls"] = check_nulls(pedidos_raw, "fact_pedidos")
    report["fact_detalle_pedidos"]["nulls"] = check_nulls(detalle_raw, "fact_detalle_pedidos")
    report["dim_clientes"]["nulls"] = check_nulls(clientes_raw, "dim_clientes")
    report["dim_productos"]["nulls"] = check_nulls(productos_raw, "dim_productos")

    # 4. Consistencia Categórica 
    report["fact_pedidos"]["categorical_consistency"] = check_categorical_consistency(pedidos_raw, "fact_pedidos", ["canal_venta", "medio_pago", "estado_pedido", "tipo_envio"])
    report["fact_detalle_pedidos"]["categorical_consistency"] = {}
    report["dim_clientes"]["categorical_consistency"] = check_categorical_consistency(clientes_raw, "dim_clientes", ["genero", "ciudad", "provincia", "canal_adquisicion"])
    report["dim_productos"]["categorical_consistency"] = check_categorical_consistency(productos_raw, "dim_productos", ["categoria", "marca", "gama"])
    
    # 5. Reglas de Negocio
    report["business_rules"]["fact_pedidos"] = check_business_rules_pedidos(pedidos_raw)
    report["business_rules"]["fact_detalle_pedidos"] = check_business_rules_detalle(detalle_raw)
    report["business_rules"]["dim_clientes"] = check_business_rules_clientes(clientes_raw)
    report["business_rules"]["dim_productos"] = check_business_rules_productos(productos_raw)

    # 6. Integridad Relacional
    report["relational_integrity"] = check_referential_integrity(pedidos_raw, detalle_raw, clientes_raw, productos_raw)

    return report