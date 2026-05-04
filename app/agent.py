import re

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
    "chao", "chau", "bye", "hasta", "luego", "claro", "excelente", "genial",
    "bien", "super", "súper", "👍", "de nada", "con gusto", "bueno",
})

_CONTINUE_TOKENS = frozenset({
    "consulta", "pregunta", "quiero", "necesito", "puedo", "podria", "podrías", "podrias",
    "otra", "adicional", "tambien", "también", "informacion", "información", "perfil", "perfiles",
    "cotizar", "resultado", "resultados", "muestra", "ruta", "retiro", "agendar", "programar",
})


def _tokenize(text: str) -> list[str]:
    return re.findall(r"[a-z0-9áéíóúñü]+", text.lower())


def _is_farewell(text: str) -> bool:
    tokens = _tokenize(text)
    if not tokens:
        return False

    words = set(tokens)
    if words & _CONTINUE_TOKENS:
        return False

    if len(tokens) <= 6 and all(token in _FAREWELL_TOKENS for token in tokens):
        return True

    return len(tokens) <= 3 and tokens[0] in _FAREWELL_TOKENS


_AFFIRMATIVE_TOKENS = frozenset({
    "si", "sí", "ok", "okay", "listo", "perfecto", "claro", "bien",
    "correcto", "exacto", "dale", "sip", "aja", "ajá",
})

_HANDOFF_INTENTS = frozenset({"accounting", "new_client"})

PAYMENT_METHODS = frozenset({"contado", "contraentrega"})
PAYMENT_METHOD_QUESTION = "Antes de cerrar, ¿preferís pagar ahora (contado) o contraentrega con el motorizado?"

_ORDER_RESET_FIELDS = frozenset({
    "exam_type", "patient_name", "species", "patient_age",
    "owner_name", "payment_method", "selected_tests",
})


def _strip_question_sentences(text: str) -> str:
    chunks = [c.strip() for c in re.split(r"(?<=[.!?])\s+", (text or "").strip()) if c.strip()]
    kept = [chunk for chunk in chunks if "?" not in chunk and "¿" not in chunk]
    return " ".join(kept).strip()


def _default_handoff_reply(handoff_area: str | None) -> str:
    if handoff_area == "contabilidad":
        return "Para este tema te voy a comunicar con contabilidad para que te ayuden."
    if handoff_area == "operaciones":
        return "Te voy a comunicar con atención al cliente para ayudarte con este proceso."
    return "Te voy a comunicar con el equipo correspondiente para ayudarte mejor."


def _limit_to_single_question(text: str) -> str:
    if not text:
        return text
    if text.count("?") <= 1:
        return text
    first_q = text.find("?")
    return text[: first_q + 1].strip()


def _apply_handoff_guardrails(ai_response: dict) -> dict:
    intent = ai_response.get("intent", "unknown")
    needs_handoff = bool(ai_response.get("requires_handoff")) or intent in _HANDOFF_INTENTS
    if not needs_handoff:
        ai_response["reply"] = _limit_to_single_question(ai_response.get("reply", ""))
        return ai_response

    ai_response["requires_handoff"] = True
    ai_response["phase"] = "fase_7_escalado"

    if intent == "accounting":
        ai_response["handoff_area"] = "contabilidad"
        ai_response["service_area"] = "accounting"
    elif intent == "new_client":
        ai_response["handoff_area"] = ai_response.get("handoff_area") or "operaciones"
        ai_response["service_area"] = "new_client"
    elif intent == "route_scheduling":
        payment_method = (ai_response.get("captured_fields") or {}).get("payment_method")
        if payment_method == "contado":
            ai_response["handoff_area"] = ai_response.get("handoff_area") or "contabilidad"
        ai_response["service_area"] = "route_scheduling"

    cleaned_reply = _strip_question_sentences(ai_response.get("reply", ""))
    if not cleaned_reply:
        cleaned_reply = _default_handoff_reply(ai_response.get("handoff_area"))
    ai_response["reply"] = cleaned_reply
    return ai_response


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


def _route_ready_for_payment(session: dict, fields: dict) -> bool:
    has_client = bool(session.get("client_id") or fields.get("_client_found"))
    has_route_data = all(fields.get(k) for k in ("pickup_address", "exam_type", "patient_name", "species"))
    return has_client and has_route_data


def _enforce_payment_step(session: dict, ai_response: dict, fields: dict) -> dict:
    if ai_response.get("intent") != "route_scheduling":
        return ai_response

    if not _route_ready_for_payment(session, fields):
        return ai_response

    payment_method = fields.get("payment_method")
    if payment_method in PAYMENT_METHODS:
        ai_response["service_area"] = "route_scheduling"
        if payment_method == "contado":
            ai_response["requires_handoff"] = True
            ai_response["handoff_area"] = ai_response.get("handoff_area") or "contabilidad"
        elif payment_method == "contraentrega":
            ai_response["requires_handoff"] = False
            ai_response["handoff_area"] = None
        return ai_response

    ai_response["reply"] = PAYMENT_METHOD_QUESTION
    ai_response["phase"] = "fase_2_recogida_datos"
    ai_response["intent"] = "route_scheduling"
    ai_response["service_area"] = "route_scheduling"
    ai_response["requires_handoff"] = False
    ai_response["handoff_area"] = None
    ai_response["message_mode"] = "flow_progress"
    ai_response["pending_intents"] = ai_response.get("pending_intents", [])
    return ai_response


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

    # Nueva orden en misma sesión: fase terminal + no es despedida → limpiar datos de la orden anterior
    if session.get("phase_current") in TERMINAL_PHASES:
        for field in _ORDER_RESET_FIELDS:
            prev_captured.pop(field, None)
        prev_captured.pop("_custom_profile_summary", None)
        prev_captured.pop("_pending_intents", None)
        session["phase_current"] = "fase_1_clasificacion"
        session["intent_current"] = "unknown"
        pending = []

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
                if prev_captured.get("_handoff_announced"):
                    # Ya se notificó la derivación en un turno anterior.
                    # No repetir el mismo mensaje: dejar que el AI responda la nueva consulta.
                    fields["_handoff_announced"] = True
                else:
                    # Ya se preguntó y confirmó cliente nuevo → escalar una sola vez
                    fields["_handoff_announced"] = True
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

    ai_response = _enforce_payment_step(session, ai_response, fields)
    ai_response["captured_fields"] = fields
    ai_response = _apply_handoff_guardrails(ai_response)

    previous_phase = session.get("phase_current", "")
    new_phase = ai_response["phase"]

    # Notificación del motorizado al cerrar una solicitud de ruta
    if (new_phase in TERMINAL_PHASES
            and previous_phase not in TERMINAL_PHASES
            and ai_response.get("intent") == "route_scheduling"):
        client_id = session.get("client_id")
        if client_id:
            courier = db.get_courier_for_client(client_id)
            if courier and courier.get("name"):
                ai_response["reply"] += f"\n\nNuestro motorizado {courier['name']} fue notificado y pasará a retirar la muestra."

    db.save_message(chat_id, user_message, "user")
    db.save_message(chat_id, ai_response["reply"], "bot")

    fields["_pending_intents"] = ai_response.get("pending_intents", [])
    ai_response["captured_fields"] = fields
    db.update_session(chat_id, ai_response)

    if new_phase in TERMINAL_PHASES and previous_phase not in TERMINAL_PHASES:
        db.create_request(chat_id, session, ai_response)

    return ai_response["reply"]
