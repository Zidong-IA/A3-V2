-- Ejecutar en el SQL Editor de Supabase
-- Permite 'recepcion' como handoff_area válido (necesario para escalación de cliente nuevo del Bloque A)

-- 1. Eliminar el CHECK constraint anterior si existe
ALTER TABLE telegram_sessions
    DROP CONSTRAINT IF EXISTS telegram_sessions_handoff_area_check;

-- 2. Recrearlo con 'recepcion' incluido
ALTER TABLE telegram_sessions
    ADD CONSTRAINT telegram_sessions_handoff_area_check
    CHECK (handoff_area IS NULL OR handoff_area IN (
        'contabilidad',
        'operaciones',
        'tecnico',
        'recepcion'
    ));
