# Prompt: Debug del agente conversacional

Usar cuando el bot responde de forma incorrecta o inesperada.

## Pasos de diagnóstico

1. **¿Qué mensaje envió el usuario?** — copiar el texto exacto
2. **¿Qué respondió el bot?** — copiar la respuesta
3. **¿Qué debería haber respondido?** — describir la respuesta esperada

## Preguntas clave para el diagnóstico

- ¿Está en la fase correcta? Revisar `telegram_sessions.phase_current` en Supabase
- ¿Los `captured_fields` tienen los datos que ya se dieron? Revisar el JSON en BD
- ¿El JSON que devolvió OpenAI es válido? Revisar logs de `app/services/ai.py`
- ¿El schema de OpenAI tiene el campo necesario? Verificar `app/schema.py`
- ¿La regla de negocio aplica? Verificar `app/rules.py` con los datos del caso

## Queries útiles en Supabase

```sql
-- Estado actual de sesión de un chat
SELECT * FROM telegram_sessions WHERE external_chat_id = '123456789';

-- Últimos mensajes de una sesión
SELECT * FROM conversation_messages
WHERE external_chat_id = '123456789'
ORDER BY created_at DESC
LIMIT 10;

-- Solicitudes recientes de un cliente
SELECT * FROM requests
WHERE client_id = 'uuid-del-cliente'
ORDER BY requested_at DESC
LIMIT 5;

-- Eventos de auditoría de una solicitud
SELECT * FROM request_events
WHERE request_id = 'uuid-de-la-solicitud'
ORDER BY created_at;
```

## Cómo simular un turno localmente

```python
from app.agent import process_turn
reply = process_turn(chat_id="test_123", user_message="Necesito un retiro")
print(reply)
```

## Checklist de fixes comunes

- [ ] ¿El bot preguntó algo que ya sabía? → Verificar `captured_fields` en sesión
- [ ] ¿El bot no escaló cuando debía? → Revisar detección de `accounting`/`new_client` en prompt
- [ ] ¿La fecha de recogida es incorrecta? → Revisar `rules.py` y timezone
- [ ] ¿El bot no encontró al cliente? → Verificar búsqueda en `clients` por nombre/NIT
- [ ] ¿No se asignó motorizado? → Verificar `client_courier_assignment` para ese `client_id`
