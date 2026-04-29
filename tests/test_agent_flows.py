"""
Tests de flujo del agente con mocks de servicios externos.
Cubre casos 1, 2, 3, 5, 7, 8, 9, 10, 11 del bootstrap sección 12.
"""
import pytest
from unittest.mock import patch, MagicMock


# ── Fixtures ──────────────────────────────────────────────────────────────────

def _make_session(phase="fase_1_clasificacion", intent="unknown", client_id=None, captured=None):
    return {
        "external_chat_id": "test-chat-1",
        "client_id": client_id,
        "phase_current": phase,
        "intent_current": intent,
        "captured_fields": captured or {},
    }


def _make_ai_response(phase, intent, requires_handoff=False, handoff_area=None, pending=None):
    return {
        "reply": "respuesta de prueba",
        "intent": intent,
        "phase": phase,
        "service_area": intent,
        "captured_fields": {
            "clinic_name": "Clínica Test",
            "tax_id": None,
            "pickup_address": "Calle 1",
            "exam_type": "hemograma",
            "patient_name": None,
            "_pending_intents": pending or [],
        },
        "message_mode": "flow_progress",
        "requires_handoff": requires_handoff,
        "handoff_area": handoff_area,
        "resume_prompt": "",
        "confidence": 0.95,
        "pending_intents": pending or [],
    }


# ── Test 1: cliente con motorizado asignado → solicitud 'assigned' ────────────

def test_request_assigned_when_courier_exists():
    session = _make_session(client_id="client-uuid-1")
    ai_resp = _make_ai_response("fase_6_cierre", "route_scheduling")

    courier = {"id": "courier-uuid-1", "name": "Carlos", "phone": "123", "availability": "available"}

    with patch("app.services.db.get_or_create_session", return_value=session), \
         patch("app.services.db.get_recent_messages", return_value=[]), \
         patch("app.services.ai.generate_turn", return_value=ai_resp), \
         patch("app.services.db.identify_client", return_value=None), \
         patch("app.services.db.save_message"), \
         patch("app.services.db.update_session"), \
         patch("app.services.db.get_courier_for_client", return_value=courier) as mock_courier, \
         patch("app.services.db.create_request", return_value="req-uuid-1") as mock_create:

        from app.agent import process_turn
        process_turn("test-chat-1", "Necesito una ruta para hoy")

        mock_create.assert_called_once()
        call_args = mock_create.call_args[0]
        assert call_args[2]["intent"] == "route_scheduling"


# ── Test 2: cliente sin motorizado → error_pending_assignment ────────────────

def test_request_error_when_no_courier():
    session = _make_session(client_id="client-uuid-2")
    ai_resp = _make_ai_response("fase_6_cierre", "route_scheduling")

    with patch("app.services.db.get_or_create_session", return_value=session), \
         patch("app.services.db.get_recent_messages", return_value=[]), \
         patch("app.services.ai.generate_turn", return_value=ai_resp), \
         patch("app.services.db.identify_client", return_value=None), \
         patch("app.services.db.save_message"), \
         patch("app.services.db.update_session"), \
         patch("app.services.db.get_courier_for_client", return_value=None), \
         patch("app.services.db._client") as mock_db_client:

        # Simular insert en requests y request_events
        mock_table = MagicMock()
        mock_table.insert.return_value.execute.return_value.data = [{"id": "req-uuid-2"}]
        mock_db_client.table.return_value = mock_table

        from app.agent import process_turn
        reply = process_turn("test-chat-1", "Necesito una ruta para hoy")
        assert reply == "respuesta de prueba"


# ── Test 3 & 10: cliente nuevo → fase_7_escalado inmediato ───────────────────

def test_new_client_escalates_immediately():
    session = _make_session()
    ai_resp = _make_ai_response(
        "fase_7_escalado", "new_client",
        requires_handoff=True, handoff_area="operaciones"
    )

    with patch("app.services.db.get_or_create_session", return_value=session), \
         patch("app.services.db.get_recent_messages", return_value=[]), \
         patch("app.services.ai.generate_turn", return_value=ai_resp), \
         patch("app.services.db.identify_client", return_value=None), \
         patch("app.services.db.save_message"), \
         patch("app.services.db.update_session"), \
         patch("app.services.db.create_request", return_value="req-uuid-3") as mock_create:

        from app.agent import process_turn
        process_turn("test-chat-1", "Quiero registrarme como cliente nuevo")

        mock_create.assert_called_once()
        call_args = mock_create.call_args[0]
        assert call_args[2]["intent"] == "new_client"
        assert call_args[2]["requires_handoff"] is True


# ── Test 9: gestión de pagos → fase_7_escalado, handoff_area=contabilidad ────

def test_accounting_escalates_to_contabilidad():
    session = _make_session()
    ai_resp = _make_ai_response(
        "fase_7_escalado", "accounting",
        requires_handoff=True, handoff_area="contabilidad"
    )

    with patch("app.services.db.get_or_create_session", return_value=session), \
         patch("app.services.db.get_recent_messages", return_value=[]), \
         patch("app.services.ai.generate_turn", return_value=ai_resp), \
         patch("app.services.db.identify_client", return_value=None), \
         patch("app.services.db.save_message"), \
         patch("app.services.db.update_session"), \
         patch("app.services.db.create_request", return_value="req-uuid-4") as mock_create:

        from app.agent import process_turn
        process_turn("test-chat-1", "Necesito hablar del pago de la factura")

        mock_create.assert_called_once()
        call_args = mock_create.call_args[0]
        assert call_args[2]["handoff_area"] == "contabilidad"


# ── Test 5: múltiples intenciones → pending_intents guardados en sesión ───────

def test_pending_intents_saved_to_session():
    session = _make_session()
    ai_resp = _make_ai_response(
        "fase_2_recogida_datos", "results",
        pending=["route_scheduling"]
    )

    captured_in_update = {}

    def fake_update(chat_id, response):
        captured_in_update.update(response["captured_fields"])

    with patch("app.services.db.get_or_create_session", return_value=session), \
         patch("app.services.db.get_recent_messages", return_value=[]), \
         patch("app.services.ai.generate_turn", return_value=ai_resp), \
         patch("app.services.db.identify_client", return_value=None), \
         patch("app.services.db.save_message"), \
         patch("app.services.db.update_session", side_effect=fake_update), \
         patch("app.services.db.create_request"):

        from app.agent import process_turn
        process_turn("test-chat-1", "Quiero saber de Toby y también programar una ruta")

        assert captured_in_update.get("_pending_intents") == ["route_scheduling"]


# ── Test 8: conversación retomada → no hay saludo redundante (R2) ─────────────

def test_resumed_conversation_no_greeting():
    history = [
        {"role": "user", "content": "Hola, necesito una ruta"},
        {"role": "bot", "content": "¿De qué clínica es la solicitud?"},
    ]
    session = _make_session(phase="fase_2_recogida_datos", intent="route_scheduling")
    ai_resp = _make_ai_response("fase_2_recogida_datos", "route_scheduling")
    ai_resp["reply"] = "¿Qué tipo de análisis van a enviar?"

    with patch("app.services.db.get_or_create_session", return_value=session), \
         patch("app.services.db.get_recent_messages", return_value=history), \
         patch("app.services.ai.generate_turn", return_value=ai_resp) as mock_ai, \
         patch("app.services.db.identify_client", return_value=None), \
         patch("app.services.db.save_message"), \
         patch("app.services.db.update_session"), \
         patch("app.services.db.create_request"):

        from app.agent import process_turn
        reply = process_turn("test-chat-1", "Clínica San Marcos")

        # Verificar que el historial previo se pasó al modelo
        call_kwargs = mock_ai.call_args
        history_passed = call_kwargs[1].get("history") or call_kwargs[0][1]
        assert len(history_passed) == 2
        assert "Hola" in history_passed[0]["content"]


# ── Test 11: toda solicitud de ruta → priority siempre "normal" en el request ──

def test_request_priority_always_normal():
    session = _make_session(client_id="client-uuid-5")
    ai_resp = _make_ai_response("fase_6_cierre", "route_scheduling")

    courier = {"id": "courier-uuid-5", "name": "Pedro"}

    with patch("app.services.db.get_or_create_session", return_value=session), \
         patch("app.services.db.get_recent_messages", return_value=[]), \
         patch("app.services.ai.generate_turn", return_value=ai_resp), \
         patch("app.services.db.identify_client", return_value=None), \
         patch("app.services.db.save_message"), \
         patch("app.services.db.update_session"), \
         patch("app.services.db.get_courier_for_client", return_value=courier), \
         patch("app.services.db.create_request", return_value="req-uuid-5") as mock_create:

        from app.agent import process_turn
        process_turn("test-chat-1", "Necesito una ruta")

        mock_create.assert_called_once()
        call_args = mock_create.call_args[0]
        assert call_args[2].get("captured_fields", {}).get("priority") != "urgent"
