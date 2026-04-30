from app.services import ai, db
from app.rules import TERMINAL_PHASES, calculate_custom_profile_total

WELCOME_MESSAGE = (
    "Hola! Buen día, me alegra que nos visites.\n"
    "Bienvenido a A3 laboratorio clínico veterinario 🧪 🧫\n"
    "¿En qué podemos ayudarte?"
)

CLIENT_NOT_FOUND_MESSAGE = (
    "En este momento no encuentro la veterinaria registrada en nuestra base de datos.\n"
    "Para poder coordinar el retiro de muestras, primero necesitamos realizar el registro del cliente.\n"
    "Te voy a comunicar con atención al cliente para que puedan ayudarte con este proceso."
)

CLIENT_SEARCH_FAILED_MESSAGE = (
    "No encuentro ninguna veterinaria registrada con ese dato.\n"
    "¿Sos cliente nuevo?"
)

FAREWELL_REPLY = (
    "Con mucho gusto, para eso estamos! "
    "Si en algún momento necesitás algo más, acá seguimos. ¡Hasta luego, cuídate!"
)

_FAREWELL_TOKENS = frozenset({
    "gracias", "dale", "ok", "okay", "listo", "perfecto", "entendido",
    "chao", "chau", "bye", "hasta", "claro", "excelente", "genial",
    "bien", "super", "súper", "👍", "de nada", "con gusto", "bueno",
})


def _is_farewell(text: str) -> bool:
    words = set(text.lower().split())
    return bool(words & _FAREWELL_TOKENS) and len(words) <= 6


_AFFIRMATIVE_TOKENS = frozenset({
    "si", "sí", "ok", "okay", "listo", "perfecto", "claro", "bien",
    "correcto", "exacto", "dale", "sip", "aja", "ajá",
})


def _consecutive_affirmatives(history: list[dict]) -> int:
    count = 0
    for msg in reversed(history):
        if msg["role"] != "user":
            continue
        words = set(msg["content"].lower().strip().split())
        if words & _AFFIRMATIVE_TOKENS and len(words) <= 4:
            count += 1
        else:
            break
    return count


def process_turn(chat_id: str, user_message: str) -> str:
    session = db.get_or_create_session(chat_id)
    history = db.get_recent_messages(chat_id, limit=8)

    # Primer mensaje: saludo exacto, sin llamar al AI
    if len(history) == 0:
        db.save_message(chat_id, user_message, "user")
        db.save_message(chat_id, WELCOME_MESSAGE, "bot")
        return WELCOME_MESSAGE

    # Despedida después de fase terminal: cerrar sin llamar al AI
    if session.get("phase_current") in TERMINAL_PHASES and _is_farewell(user_message):
        db.save_message(chat_id, user_message, "user")
        db.save_message(chat_id, FAREWELL_REPLY, "bot")
        return FAREWELL_REPLY

    prev_captured = session.get("captured_fields") or {}
    pending = prev_captured.get("_pending_intents", [])

    consecutive_aff = _consecutive_affirmatives(history)
    if consecutive_aff >= 2:
        session["_force_close_hint"] = (
            f"ALERTA DE BUCLE: el usuario lleva {consecutive_aff} respuestas afirmativas seguidas. "
            "Ya tenés los datos necesarios. Cerrá el flujo ahora con fase_6_cierre. No hagas más preguntas."
        )

    # Inyectar catálogo cuando se está eligiendo el tipo de análisis
    catalog_ctx = None
    prev_intent = session.get("intent_current", "")
    prev_fields = session.get("captured_fields") or {}
    selected = prev_fields.get("selected_tests")
    if prev_intent == "route_scheduling":
        if selected is not None:
            # Modo perfil personalizado: catálogo de análisis individuales + resumen calculado
            catalog_ctx = db.get_individual_tests_context(prev_fields.get("species"))
            if selected:
                rows = db.get_tests_by_codes(selected)
                totals = calculate_custom_profile_total([r["price"] for r in rows])
                items = ", ".join(f"{r['code']}-{r['name']} ${r['price']//1000}k" for r in rows)
                session["_custom_profile_summary"] = (
                    f"PERFIL PERSONALIZADO EN CONSTRUCCIÓN ({totals['count']} análisis): {items}. "
                    f"Subtotal ${totals['subtotal']:,} COP. Total ${totals['total']:,} COP."
                )
        elif not prev_fields.get("exam_type"):
            catalog_ctx = db.get_catalog_context(prev_fields.get("species"))

    ai_response = ai.generate_turn(
        session=session,
        history=history,
        user_message=user_message,
        pending_intents=pending,
        catalog_context=catalog_ctx,
    )

    fields = ai_response.get("captured_fields", {})

    # Mantener metadata de turno anterior (campos con _)
    for k, v in prev_captured.items():
        if k.startswith("_") and k != "_pending_intents" and k not in fields:
            fields[k] = v

    # Buscar cliente cuando el AI capturó nombre o NIT por primera vez
    client_status_changed = False
    if not session.get("client_id") and (fields.get("clinic_name") or fields.get("tax_id")):
        client = db.identify_client(
            name=fields.get("clinic_name"),
            tax_id=fields.get("tax_id"),
        )
        if client:
            db.link_client_to_session(chat_id, client["id"])
            session["client_id"] = client["id"]
            fields["_client_found"] = True
            fields["_client_not_found"] = False
            fields["_client_display_name"] = client.get("clinic_name", "")
            fields["_client_address"] = client.get("address") or ""
        else:
            fields["_client_found"] = False
            fields["_client_not_found"] = True
        client_status_changed = True

    # Si el cliente acaba de ser identificado (o no encontrado), resolver en el mismo turno
    if client_status_changed:
        if fields.get("_client_not_found"):
            if prev_captured.get("_asked_if_new_client"):
                # Ya se preguntó → escalar
                ai_response = {
                    "reply": CLIENT_NOT_FOUND_MESSAGE,
                    "phase": "fase_7_escalado",
                    "intent": "new_client",
                    "service_area": "new_client",
                    "requires_handoff": True,
                    "handoff_area": "operaciones",
                    "captured_fields": fields,
                    "confidence": 1.0,
                    "message_mode": "flow_progress",
                    "pending_intents": [],
                    "resume_prompt": "",
                }
            else:
                # Primera vez que no se encuentra → preguntar antes de escalar
                fields["_asked_if_new_client"] = True
                ai_response = {
                    "reply": CLIENT_SEARCH_FAILED_MESSAGE,
                    "phase": "fase_2_recogida_datos",
                    "intent": ai_response.get("intent", "unknown"),
                    "service_area": "unknown",
                    "requires_handoff": False,
                    "handoff_area": None,
                    "captured_fields": fields,
                    "confidence": 1.0,
                    "message_mode": "flow_progress",
                    "pending_intents": [],
                    "resume_prompt": "",
                }
        else:
            updated_session = {**session, "captured_fields": fields}
            ai_response = ai.generate_turn(
                session=updated_session,
                history=history,
                user_message=user_message,
                pending_intents=pending,
                catalog_context=catalog_ctx,
            )
            new_fields = ai_response.get("captured_fields", {})
            for k, v in fields.items():
                if k.startswith("_"):
                    new_fields[k] = v
            fields = new_fields

    db.save_message(chat_id, user_message, "user")
    db.save_message(chat_id, ai_response["reply"], "bot")

    previous_phase = session.get("phase_current", "")
    new_phase = ai_response["phase"]

    fields["_pending_intents"] = ai_response.get("pending_intents", [])
    ai_response["captured_fields"] = fields
    db.update_session(chat_id, ai_response)

    if new_phase in TERMINAL_PHASES and previous_phase not in TERMINAL_PHASES:
        db.create_request(chat_id, session, ai_response)

    return ai_response["reply"]
