-- ============================================================
-- SCRIPT DE CREACIÓN: MODELO DIMENSIONAL EN ESTRELLA
-- Proyecto: Mercados La Colina S.A.
-- Motor: PostgreSQL
-- ============================================================

-- 1. Limpieza previa (Drop tables) para evitar errores si el modelo ya existe
DROP TABLE IF EXISTS hecho_inventario CASCADE;
DROP TABLE IF EXISTS dim_tienda CASCADE;
DROP TABLE IF EXISTS dim_canal CASCADE;
DROP TABLE IF EXISTS dim_promocion CASCADE;
DROP TABLE IF EXISTS dim_producto CASCADE;
DROP TABLE IF EXISTS dim_tiempo CASCADE;

-- ============================================================
-- 2. CREACIÓN DE TABLAS DE DIMENSIONES
-- ============================================================

CREATE TABLE dim_tienda (
    id_tienda SERIAL PRIMARY KEY,
    nombre_tienda CHARACTER VARYING(50)
);

CREATE TABLE dim_canal (
    id_canal SERIAL PRIMARY KEY,
    nombre_canal CHARACTER VARYING(50)
);

CREATE TABLE dim_promocion (
    id_promocion SERIAL PRIMARY KEY,
    tipo_promocion CHARACTER VARYING(50)
);

CREATE TABLE dim_producto (
    id_producto SERIAL PRIMARY KEY,
    familia_producto CHARACTER VARYING(50),
    clasificacion_abc CHARACTER VARYING(5)
);

CREATE TABLE dim_tiempo (
    id_tiempo SERIAL PRIMARY KEY,
    fecha_inicio_semana DATE,
    anio INTEGER,
    mes INTEGER,
    semana_anio INTEGER
);

-- ============================================================
-- 3. CREACIÓN DE LA TABLA DE HECHOS
-- ============================================================

CREATE TABLE hecho_inventario (
    id_hecho SERIAL PRIMARY KEY,
    id_producto_tienda_semana CHARACTER VARYING(20),
    
    -- Llaves foráneas
    id_tienda INTEGER REFERENCES dim_tienda(id_tienda),
    id_canal INTEGER REFERENCES dim_canal(id_canal),
    id_promocion INTEGER REFERENCES dim_promocion(id_promocion),
    id_producto INTEGER REFERENCES dim_producto(id_producto),
    id_tiempo INTEGER REFERENCES dim_tiempo(id_tiempo),
    
    -- Métricas operativas
    ventas_unidades INTEGER,
    dias_cobertura INTEGER,
    inventario_inicial INTEGER,
    dias_retraso_proveedor INTEGER,
    quiebre_stock INTEGER,
    
    -- Trazabilidad y Linaje
    sistema_origen CHARACTER VARYING(20),
    fecha_carga DATE,

    -- ========================================================
    -- CONSTRAINTS Y POLÍTICAS DE GOBIERNO (Guardrails)
    -- ========================================================
    -- POL-CAL-01: quiebre_stock es estrictamente binario
    CONSTRAINT chk_quiebre_stock CHECK (quiebre_stock IN (0, 1)),
    
    -- Rango operativo lógico de ventas
    CONSTRAINT chk_ventas_unidades CHECK (ventas_unidades >= 0),
    
    -- Rango de retraso de proveedor 
    CONSTRAINT chk_dias_retraso CHECK (dias_retraso_proveedor >= 0)
);