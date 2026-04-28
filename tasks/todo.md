# Tareas — A3 Laboratorio Veterinario V2

## En progreso

_ninguna_

## Pendiente

### Tests obligatorios (bootstrap sección 12)
- [ ] Test 1: cliente con motorizado asignado → solicitud `assigned`
- [ ] Test 2: cliente sin motorizado → `error_pending_assignment` + evento en `request_events`
- [ ] Test 3: cliente nuevo → `fase_7_escalado` inmediato, sin recolectar datos
- [ ] Test 4: solicitud post-17:30 → `scheduled_pickup_date` = siguiente día hábil
- [ ] Test 5: múltiples intenciones en un mensaje → ambas procesadas en orden correcto
- [ ] Test 6: usuario repite sin dar dato → agente ofrece opciones en vez de preguntar de nuevo
- [ ] Test 7: usuario cancela solicitud en curso → cancelación confirmada, flujo limpio
- [ ] Test 8: conversación interrumpida y retomada → sin saludo, continúa donde estaba
- [ ] Test 9: gestión de pagos → derivación inmediata a contabilidad
- [ ] Test 10: alta de cliente nuevo → derivación inmediata a operaciones
- [ ] Test 11: solicitud urgente → visible en filtros y logs de eventos

## Completado

### Bloque 1 — Core del schema y prompt
- [x] `schema.py` → 10 campos, intents en inglés, 8 fases nombradas, message_mode, pending_intents, confidence
- [x] `prompt.py` → system prompt limpio (sección 9 del bootstrap), sin JSON embebido
- [x] `rules.py` → INTENT_TO_SERVICE_AREA con intents en inglés + TERMINAL_PHASES

### Bloque 2 — Capa de datos
- [x] `db.py` → get_or_create_session sin columnas fantasma
- [x] `db.py` → update_session alineado con modelo real (last_activity, sin columnas inexistentes)
- [x] `db.py` → create_request usa intents en inglés directamente

### Bloque 3 — Lógica del agente
- [x] `agent.py` → manejo de pending_intents entre turnos
- [x] `agent.py` → transición a fase terminal usando TERMINAL_PHASES
- [x] `ai.py` → recibe pending_intents, filtra campos internos del contexto

### Bloque 4 — Infraestructura
- [x] `.env.example` con todas las variables del bootstrap sección 11

---

## Resultados

**2026-04-27** — Bloques 1-4 completados. Pendiente: 11 tests de la sección 12 del bootstrap.
