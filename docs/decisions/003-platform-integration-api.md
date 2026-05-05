# 003 — API interna para integración de plataforma

## Estado

Aprobada (2026-05-04)

## Contexto

El agente conversacional y la plataforma operativa deben compartir la misma información en Supabase.
La plataforma necesita consultar estado de solicitudes, clientes sin motorizado asignado y etapas conversacionales,
y también actualizar estados operativos sin tocar el chatbot.

## Decisión

Exponer una API interna en Flask bajo `/api/platform/*` que use el mismo cliente Supabase existente,
sin modificar esquema de base de datos.

Rutas incluidas:

- `GET /api/platform/overview`
- `GET /api/platform/clients`
- `GET /api/platform/requests`
- `GET /api/platform/requests/unassigned`
- `GET /api/platform/requests/<request_id>/events`
- `PATCH /api/platform/requests/<request_id>/status`

Auditoría:

- Cada actualización de estado desde la API registra evento `status_updated` en `request_events`.

Seguridad:

- Si existe `PLATFORM_API_TOKEN`, se exige `X-Platform-Token` en todas las rutas de integración.

## Consecuencias

- La plataforma puede conectarse de forma directa al backend del agente para ver y gestionar operación en tiempo real.
- No se duplica lógica de negocio ni se crean tablas nuevas.
- Se mantiene compatibilidad con V1/V2 porque la API es aditiva.
