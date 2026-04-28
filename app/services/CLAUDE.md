# Módulo: app/services/

## Responsabilidad

Clientes de servicios externos. Cada archivo habla con un solo servicio externo.
No contienen lógica de negocio — solo I/O y manejo de errores de la API.

## Archivos

### `ai.py` — Cliente OpenAI
- `generate_turn(system_prompt, history, session, user_message) -> dict`
- Usa `response_format` con el JSON schema de `app/schema.py`
- Si la API falla: lanzar excepción, nunca devolver datos inventados

### `db.py` — Cliente Supabase
- `get_session(chat_id) -> dict`
- `get_history(chat_id, limit=8) -> list`
- `save_message(chat_id, text, role) -> None`
- `update_session(chat_id, ai_response) -> None`
- `create_request(chat_id, ai_response) -> str`  ← devuelve request_id
- `find_client(clinic_name=None, tax_id=None) -> dict | None`
- `get_courier_for_client(client_id) -> dict | None`

### `telegram.py` — Cliente Telegram
- `send_message(chat_id, text) -> None`
- `set_webhook(url, secret) -> None`

## Reglas

- Ningún método de estos archivos importa de `app/agent.py` o `app/rules.py`
- Todos los errores de red/API se capturan y re-lanzan con contexto útil para el log
- Las queries a Supabase usan el SDK (`.select()`, `.insert()`, `.update()`)
  — no SQL raw excepto en casos muy específicos con `.rpc()`
- El cliente Supabase se inicializa una vez en `config.py`, no en cada request
