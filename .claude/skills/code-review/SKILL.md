---
name: Code Review
description: Revisión de código con checklist específico para el stack Python/Flask/Supabase de A3
---

# Code Review — A3 Veterinaria

Realiza una revisión del código modificado siguiendo este checklist.

## Checklist

### Correctitud
- [ ] La lógica cumple con las reglas de negocio (corte 17:30, motorizado determinista, escalados)
- [ ] Los edge cases están cubiertos (cliente sin motorizado, post-17:30, cliente no identificado)
- [ ] No hay bugs en el manejo de timezone (siempre `America/Bogota`, nunca UTC naïve)

### Arquitectura
- [ ] El archivo tiene una sola responsabilidad
- [ ] El archivo es < 200 líneas
- [ ] No hay lógica de negocio en `main.py`
- [ ] No hay I/O en `rules.py`
- [ ] No hay queries directas fuera de `services/db.py`

### Calidad
- [ ] Nombrado claro en español para variables de dominio, snake_case para todo lo demás
- [ ] Funciones pequeñas con una sola responsabilidad
- [ ] Sin código duplicado
- [ ] Sin imports no usados

### Seguridad
- [ ] Sin secretos hardcodeados (tokens, keys, URLs de Supabase)
- [ ] El webhook valida `TELEGRAM_WEBHOOK_SECRET` antes de procesar
- [ ] Inputs del usuario no se usan directamente en queries (Supabase SDK los parameteriza)

### Supabase
- [ ] No se modifica el esquema de tablas existentes
- [ ] Las queries usan el SDK de Supabase (no SQL raw innecesario)
- [ ] Los errores de BD se capturan y loggean — nunca fallan silenciosamente

### OpenAI
- [ ] El schema tiene máximo 7 campos
- [ ] El system prompt y el schema están en archivos separados (`prompt.py` vs `schema.py`)
- [ ] Se usa `response_format` con JSON schema para structured output

## Formato de salida

Para cada issue encontrado:
1. Archivo y línea (`app/agent.py:45`)
2. Severidad: `crítico` / `medio` / `bajo`
3. Descripción del problema
4. Sugerencia de fix en 1-2 líneas
