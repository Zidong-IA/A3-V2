from app.services import ai, db
from app.rules import TERMINAL_PHASES

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


def process_turn(chat_id: str, user_message: str) -> str:
    session = db.get_or_create_session(chat_id)
    history = db.get_recent_messages(chat_id, limit=8)

    # Primer mensaje: saludo exacto, sin llamar al AI
    if len(history) == 0:
        db.save_message(chat_id, user_message, "user")
        db.save_message(chat_id, WELCOME_MESSAGE, "bot")
        return WELCOME_MESSAGE

    prev_captured = session.get("captured_fields") or {}
    pending = prev_captured.get("_pending_intents", [])

    ai_response = ai.generate_turn(
        session=session,
        history=history,
        user_message=user_message,
        pending_intents=pending,
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
            # Regla determinista: no depender del AI para escalar
            ai_response = {
                "reply": CLIENT_NOT_FOUND_MESSAGE,
                "phase": "fase_7_escalado",
                "intent": "new_client",
                "service_area": "recepcion",
                "requires_handoff": True,
                "handoff_area": "recepcion",
                "captured_fields": fields,
                "confidence": 1.0,
                "message_mode": "flow_progress",
                "pending_intents": [],
            }
        else:
            updated_session = {**session, "captured_fields": fields}
            ai_response = ai.generate_turn(
                session=updated_session,
                history=history,
                user_message=user_message,
                pending_intents=pending,
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
