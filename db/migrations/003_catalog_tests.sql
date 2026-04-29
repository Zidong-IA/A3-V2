-- Ejecutar en el SQL Editor de Supabase
-- Tabla de análisis INDIVIDUALES del catálogo A3 (para armado de perfiles personalizados)

CREATE TABLE IF NOT EXISTS catalog_tests (
    code        text PRIMARY KEY,
    name        text NOT NULL,
    category    text NOT NULL,
    species     text NOT NULL DEFAULT 'ambos',  -- 'canino' | 'felino' | 'ambos'
    sample      text,                            -- transporte/tipo de muestra
    price       integer NOT NULL,
    is_active   boolean DEFAULT true
);

CREATE INDEX IF NOT EXISTS idx_catalog_tests_category ON catalog_tests (category);
CREATE INDEX IF NOT EXISTS idx_catalog_tests_species  ON catalog_tests (species);
