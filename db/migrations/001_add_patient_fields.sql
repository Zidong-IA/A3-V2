-- Ejecutar en el SQL Editor de Supabase
-- Agrega campos de paciente a la tabla requests

ALTER TABLE requests
    ADD COLUMN IF NOT EXISTS species     text,
    ADD COLUMN IF NOT EXISTS patient_age text,
    ADD COLUMN IF NOT EXISTS owner_name  text;
