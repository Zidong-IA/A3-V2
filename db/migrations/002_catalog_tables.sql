-- Ejecutar en el SQL Editor de Supabase
-- Tabla de perfiles diagnósticos del catálogo A3

CREATE TABLE IF NOT EXISTS catalog_profiles (
    code        text PRIMARY KEY,
    name        text NOT NULL,
    category    text NOT NULL,
    species     text NOT NULL DEFAULT 'ambos',  -- 'canino' | 'felino' | 'ambos'
    description text,
    price       integer NOT NULL,
    is_active   boolean DEFAULT true
);

CREATE INDEX IF NOT EXISTS idx_catalog_profiles_category ON catalog_profiles (category);
CREATE INDEX IF NOT EXISTS idx_catalog_profiles_species  ON catalog_profiles (species);
