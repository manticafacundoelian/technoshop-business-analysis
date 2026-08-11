-- 00 | View analítica de pedidos
-- Objetivo: centralizar la lógica de negocio y preparar la tabla de hechos
-- para simplificar las consultas analíticas posteriores.

CREATE VIEW fact_pedidos_analitica AS
SELECT
    detalle_id,
    pedido_id,
    producto_id,
    cliente_id,
    fecha_pedido,
    CAST(strftime('%Y', fecha_pedido) AS INTEGER) AS anio,
    CAST(strftime('%m', fecha_pedido) AS INTEGER) AS mes,
    canal_venta,
    medio_pago,
    tipo_envio,
    estado_pedido,
    cantidad,
    precio_lista,
    precio_unitario,
    costo_unitario,
    descuento_aplicado,
    costo_envio_linea,
    CASE
        WHEN estado_pedido = 'Entregado' THEN cantidad * precio_lista
        ELSE 0
    END AS revenue_bruto_linea,
    CASE
        WHEN estado_pedido = 'Entregado' THEN cantidad * precio_lista * descuento_aplicado
        ELSE 0
    END AS descuento_linea,
    CASE
        WHEN estado_pedido = 'Entregado' THEN cantidad * precio_unitario
        ELSE 0
    END AS revenue_neto_linea,
    CASE
        WHEN estado_pedido = 'Entregado' THEN cantidad * costo_unitario
        ELSE 0
    END AS costo_mercaderia_linea,
    CASE
        WHEN estado_pedido = 'Entregado' THEN cantidad * precio_unitario - cantidad * costo_unitario - costo_envio_linea
        ELSE 0
    END AS ganancia_neta_linea,
    CASE
        WHEN estado_pedido = 'Entregado' THEN costo_envio_linea
        ELSE 0
    END AS costo_envio_entregados_linea,
    
    CASE
        WHEN estado_pedido IN ('Cancelado','Devuelto') THEN costo_envio_linea
        ELSE 0
    END AS perdida_no_exitosa_linea, 
   
    CASE
        WHEN estado_pedido = 'Entregado' THEN cantidad * precio_unitario - cantidad * costo_unitario - costo_envio_linea
        WHEN estado_pedido IN ('Cancelado','Devuelto') THEN -costo_envio_linea
        ELSE 0
    END AS ganancia_neta_real_linea 

FROM fact_pedidos_final;



