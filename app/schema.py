RESPONSE_SCHEMA = {
    "name": "agent_response",
    "strict": True,
    "schema": {
        "type": "object",
        "properties": {
            "reply": {"type": "string"},
            "intent": {
                "type": "string",
                "enum": ["route_scheduling", "results", "accounting", "new_client", "unknown"],
            },
            "phase": {
                "type": "string",
                "enum": [
                    "fase_0_bienvenida",
                    "fase_1_clasificacion",
                    "fase_2_recogida_datos",
                    "fase_3_validacion",
                    "fase_4_confirmacion",
                    "fase_5_ejecucion",
                    "fase_6_cierre",
                    "fase_7_escalado",
                ],
            },
            "service_area": {
                "type": "string",
                "enum": ["route_scheduling", "accounting", "results", "new_client", "unknown"],
            },
            "captured_fields": {
                "type": "object",
                "properties": {
                    "clinic_name":        {"anyOf": [{"type": "string"}, {"type": "null"}]},
                    "tax_id":             {"anyOf": [{"type": "string"}, {"type": "null"}]},
                    "pickup_address":     {"anyOf": [{"type": "string"}, {"type": "null"}]},
                    "exam_type":          {"anyOf": [{"type": "string"}, {"type": "null"}]},
                    "priority":           {"type": "string", "enum": ["normal", "urgent"]},
                    "patient_name":       {"anyOf": [{"type": "string"}, {"type": "null"}]},
                    "sample_reference":   {"anyOf": [{"type": "string"}, {"type": "null"}]},
                },
                "required": [
                    "clinic_name", "tax_id", "pickup_address", "exam_type",
                    "priority", "patient_name", "sample_reference",
                ],
                "additionalProperties": False,
            },
            "message_mode": {
                "type": "string",
                "enum": ["flow_progress", "side_question", "intent_switch", "small_talk", "cancellation"],
            },
            "requires_handoff": {"type": "boolean"},
            "handoff_area": {
                "anyOf": [
                    {"type": "string", "enum": ["contabilidad", "operaciones", "tecnico", "recepcion"]},
                    {"type": "null"},
                ]
            },
            "resume_prompt":   {"type": "string"},
            "confidence":      {"type": "number"},
            "pending_intents": {"type": "array", "items": {"type": "string"}},
        },
        "required": [
            "reply", "intent", "phase", "service_area", "captured_fields",
            "message_mode", "requires_handoff", "handoff_area",
            "resume_prompt", "confidence", "pending_intents",
        ],
        "additionalProperties": False,
    },
}
