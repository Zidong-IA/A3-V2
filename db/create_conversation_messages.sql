-- Ejecutar en el SQL Editor de Supabase
-- Tabla para historial de conversaciones del agente

CREATE TABLE IF NOT EXISTS conversation_messages (
    id uuid DEFAULT gen_random_uuid() PRIMARY KEY,
    external_chat_id text NOT NULL REFERENCES telegram_sessions(external_chat_id) ON DELETE CASCADE,
    role text NOT NULL CHECK (role IN ('user', 'bot')),
    content text NOT NULL,
    created_at timestamptz DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_conv_messages_chat_created
    ON conversation_messages (external_chat_id, created_at DESC);
