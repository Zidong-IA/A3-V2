# Arquitectura — A3 Laboratorio Veterinario

## Visión general

Bot conversacional de Telegram para A3 Laboratorio Veterinario. Procesa mensajes entrantes,
mantiene estado de conversación en Supabase, llama a OpenAI con un JSON schema fijo,
y registra solicitudes operativas en la base de datos.

```
Telegram → Flask webhook → process_turn() → OpenAI → Supabase → Telegram
```

---

## Componentes principales

### API (`app/main.py`)
- Responsabilidad: recibir webhook de Telegram, validar secret, llamar `process_turn()`
- < 100 líneas, sin lógica de negocio
- Solo dos rutas: `POST /webhook` y `GET /health`

### Agente (`app/agent.py`)
- Responsabilidad: orquestar un turno de conversación completo
- Función central: `process_turn(chat_id: str, user_message: str) -> str`
- Leer sesión → leer historial → llamar OpenAI → guardar → devolver reply

### Prompt (`app/prompt.py`)
- Responsabilidad: system prompt para OpenAI
- Solo tono, intenciones y reglas de conversación — separado del schema

### Schema (`app/schema.py`)
- Responsabilidad: JSON schema para OpenAI structured output
- 7 campos máximo — nunca ampliar sin analizar el impacto

### Reglas (`app/rules.py`)
- Responsabilidad: lógica de negocio pura, sin I/O
- Calcular fecha de recogida respetando corte 17:30
- Determinar si una solicitud necesita escalado

### Config (`app/config.py`)
- Responsabilidad: leer variables de entorno, validarlas al inicio
- Falla rápido si falta alguna variable crítica

---

## Servicios (`app/services/`)

### `ai.py` — Cliente OpenAI
- Llama a `openai.chat.completions.create()` con el JSON schema
- Maneja errores de la API (rate limit, timeout)

### `db.py` — Cliente Supabase
- `get_session(chat_id)` — leer estado actual de conversación
- `get_history(chat_id, limit=8)` — últimos N mensajes
- `save_message(chat_id, text, role)` — persistir mensaje
- `update_session(chat_id, ai_response)` — actualizar fase y campos capturados
- `create_request(chat_id, ai_response)` — registrar solicitud operativa

### `telegram.py` — Cliente Telegram
- `send_message(chat_id, text)` — enviar respuesta al usuario
- `set_webhook(url)` — configurar webhook

---

## Modelo de datos Supabase (producción — no modificar)

### Tablas de operación

**`clients`** — clínicas veterinarias registradas
```
id uuid PK | clinic_name text | tax_id text | phone text UNIQUE
address text | city text | zone text | billing_type (credit|cash) | is_active bool
```

**`couriers`** — motorizados
```
id uuid PK | name text | phone text UNIQUE | availability (available|busy|offline) | is_active bool
```

**`client_courier_assignment`** — asignación determinista cliente → motorizado
```
client_id uuid UNIQUE → clients | courier_id uuid → couriers | assigned_by text
```

**`requests`** — solicitudes operativas
```
id uuid PK | client_id → clients | entry_channel (telegram|liveconnect|manual)
service_area (route_scheduling|accounting|results|new_client|unknown)
priority text DEFAULT 'normal' | status text | exam_type text | patient_name text
pickup_address text | scheduled_pickup_date date | assigned_courier_id → couriers
fallback_reason text
```

**`request_events`** — auditoría inmutable
```
id uuid PK | request_id → requests | event_type text | event_payload jsonb | created_at timestamptz
```

### Tabla de sesión

**`telegram_sessions`** — estado activo de conversación por chat
```
external_chat_id text PK | client_id uuid → clients (nullable)
phase_current text | intent_current text | captured_fields jsonb | last_activity timestamptz
```

### Ciclo de estados de solicitud

```
received → assigned → on_route → picked_up → in_lab → processed → sent
         ↓ (sin motorizado asignado)
         error_pending_assignment
any → cancelled
```

---

## Flujo de datos por intención

### Programación de ruta (happy path)
1. Usuario: "necesito un retiro"
2. Agent identifica `route_scheduling`, fase `collecting`
3. Recolecta: `clinic_name/tax_id` → `exam_type` → `pickup_address`
4. Fase `confirming`: muestra resumen, pide confirmación
5. Fase `done`: crea registro en `requests`, asigna motorizado de `client_courier_assignment`
6. Informa fecha/franja al usuario

### Consulta de resultados
1. Usuario da referencia o nombre de paciente
2. Agent busca en `requests` por `sample_reference` o `patient_name + client_id`
3. Devuelve estado actual

### Escalado (pagos / cliente nuevo)
1. Agent detecta intención → fase `escalated` inmediatamente
2. Un solo mensaje claro al usuario
3. Crea registro en `requests` con `service_area = accounting|new_client`
4. `requires_handoff = true`

---

## Reglas de negocio

### Hora de corte
- Corte: **17:30 hora Colombia (UTC-5)**
- Solicitud antes del corte → siguiente día hábil
- Solicitud después del corte → segundo día hábil siguiente
- Días hábiles V1: lunes a viernes (festivos no gestionados automáticamente)

### Asignación de motorizado
- Fuente de verdad: `client_courier_assignment`
- Si existe → usar ese courier → estado `assigned`
- Si no existe → estado `error_pending_assignment` + evento en `request_events` + escalar

### Identificación del cliente
- Antes de registrar cualquier solicitud, el agente debe tener `client_id`
- Si no está identificado: pedir `clinic_name` o `tax_id` primero
- Buscar en `clients` por nombre o NIT — nunca crear cliente nuevo en chat

---

## Casos de prueba obligatorios

| # | Escenario | Resultado esperado |
|---|---|---|
| 1 | Saludo simple | Respuesta natural, no menú numerado |
| 2 | Cliente con motorizado asignado | Solicitud creada, estado `assigned` |
| 3 | Cliente sin motorizado | Estado `error_pending_assignment`, evento en `request_events` |
| 4 | Cliente nuevo | `escalated` inmediato, sin pedir datos |
| 5 | Solicitud post-17:30 | `scheduled_pickup_date` = segundo día hábil |
| 6 | Múltiples intenciones en un mensaje | Ambas procesadas en orden |
| 7 | Usuario repite sin dar dato | Agente ofrece opciones concretas |
| 8 | Gestión de pagos | Derivación inmediata a contabilidad |
| 9 | Small talk | Respuesta breve, retoma flujo |
| 10 | Conversación retomada | Sin saludo, continúa desde donde estaba |

---

## Decisiones de arquitectura

Ver [decisions/](decisions/) para el registro completo.

- [001 — Selección de stack](decisions/001-stack-selection.md)
