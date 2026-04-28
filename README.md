# A3 Laboratorio Veterinario — Agente Conversacional

Bot conversacional de Telegram para A3 Laboratorio Veterinario (Bogotá, Colombia).
Gestiona recogidas de muestras, consulta de resultados, y derivación a equipo humano.

## Stack

- Python 3.12+ + Flask
- Supabase (PostgreSQL) — modelo de datos existente, no modificar
- OpenAI API (gpt-5.4-nano)
- Telegram Bot API (webhook)
- Render (hosting)

## Instalación

```bash
pip install -r requirements.txt
cp .env.example .env   # completar con las variables reales
python -m app.main
```

## Estructura del proyecto

Ver [docs/architecture.md](docs/architecture.md) para la arquitectura completa.

```
app/
├── main.py          Flask + webhook (< 100 líneas)
├── agent.py         process_turn() — función central
├── prompt.py        System prompt
├── schema.py        JSON schema para OpenAI
├── rules.py         Reglas de negocio puras
├── config.py        Variables de entorno
└── services/
    ├── ai.py        Cliente OpenAI
    ├── db.py        Cliente Supabase
    └── telegram.py  Cliente Telegram
```

## Trabajo con IA

Este proyecto está diseñado para trabajar con dos modelos de IA en paralelo:

| Herramienta | Archivo de contexto | Uso |
|---|---|---|
| Claude Code | `CLAUDE.md` | Instrucciones, reglas, arquitectura |
| OpenCode (ChatGPT) | `AGENTS.md` | Instrucciones, reglas, arquitectura |

Ambos archivos contienen el mismo contexto adaptado al formato de cada herramienta.

### Skills disponibles (Claude Code)

- `/code-review` — Revisión de código con checklist
- `/deploy` — Proceso de deploy a Render

### Estado del trabajo

- Tareas actuales: `tasks/todo.md`
- Lecciones aprendidas: `tasks/lessons.md`

## Variables de entorno

```
TELEGRAM_BOT_TOKEN
TELEGRAM_WEBHOOK_SECRET
SUPABASE_URL
SUPABASE_SERVICE_ROLE_KEY
OPENAI_API_KEY
OPENAI_MODEL=gpt-5.4-nano
APP_TIMEZONE=America/Bogota
CUTOFF_HOUR=17
CUTOFF_MINUTE=30
FLASK_SECRET_KEY
```
