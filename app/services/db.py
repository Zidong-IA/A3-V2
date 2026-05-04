import re
from datetime import datetime, timezone
from supabase import create_client, Client
from app.config import SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY
from app.rules import INTENT_TO_SERVICE_AREA, get_scheduled_pickup_date

_client: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)


# ── Session ───────────────────────────────────────────────────────────────────

def get_or_create_session(chat_id: str) -> dict:
    result = _client.table("telegram_sessions").select("*").eq("external_chat_id", chat_id).execute()
    if result.data:
        return result.data[0]
    new_session = {
        "channel":        "telegram",
        "external_chat_id": chat_id,
        "client_id":      None,
        "phase_current":  "fase_0_bienvenida",
        "intent_current": "unknown",
        "captured_fields": {},
        "status":         "in_progress",
    }
    _client.table("telegram_sessions").insert(new_session).execute()
    return new_session


_VALID_HANDOFF_AREAS = {"contabilidad", "operaciones", "tecnico"}


def update_session(chat_id: str, ai_response: dict) -> None:
    update_data = {
        "phase_current":    ai_response["phase"],
        "intent_current":   ai_response["intent"],
        "service_area":     ai_response["service_area"],
        "captured_fields":  ai_response["captured_fields"],
        "requires_handoff": ai_response["requires_handoff"],
        "last_bot_message": ai_response["reply"],
        "ai_confidence":    ai_response.get("confidence"),
    }
    handoff = ai_response["handoff_area"]
    if handoff is not None and handoff in _VALID_HANDOFF_AREAS:
        update_data["handoff_area"] = handoff
    _client.table("telegram_sessions").update(update_data).eq("external_chat_id", chat_id).execute()


def link_client_to_session(chat_id: str, client_id: str) -> None:
    _client.table("telegram_sessions").update({"client_id": client_id}).eq("external_chat_id", chat_id).execute()


# ── Messages ──────────────────────────────────────────────────────────────────

def get_recent_messages(chat_id: str, limit: int = 8) -> list[dict]:
    result = (
        _client.table("conversation_messages")
        .select("role, content")
        .eq("external_chat_id", chat_id)
        .order("created_at", desc=True)
        .limit(limit)
        .execute()
    )
    return list(reversed(result.data))


def save_message(chat_id: str, content: str, role: str) -> None:
    _client.table("conversation_messages").insert({
        "external_chat_id": chat_id,
        "role": role,
        "content": content,
    }).execute()


# ── Client identification ─────────────────────────────────────────────────────

def _normalize_nit(nit: str) -> str:
    return re.sub(r"[^0-9]", "", nit)


def _nit_candidates(tax_id: str) -> list[str]:
    raw = (tax_id or "").strip()
    clean = _normalize_nit(raw)

    candidates: list[str] = []

    def add(value: str) -> None:
        if value and value not in candidates:
            candidates.append(value)

    add(raw)
    add(clean)

    if len(clean) > 1:
        base = clean[:-1]
        dv = clean[-1]
        add(base)
        add(f"{base}-{dv}")

    return candidates


def identify_client(name: str = None, tax_id: str = None) -> dict | None:
    if tax_id:
        for nit in _nit_candidates(tax_id):
            result = _client.table("clients").select("*").eq("tax_id", nit).eq("is_active", True).execute()
            if result.data:
                return result.data[0]
    if name:
        result = (
            _client.table("clients")
            .select("*")
            .ilike("clinic_name", f"%{name}%")
            .eq("is_active", True)
            .execute()
        )
        if result.data:
            return result.data[0]
    return None


def get_catalog_context(species: str | None = None) -> str:
    """Returns a compact catalog string for AI context injection."""
    query = _client.table("catalog_profiles").select("code, name, category, price").eq("is_active", True)
    if species and species.lower() in ("canino", "felino"):
        query = query.in_("species", [species.lower(), "ambos"])
    rows = query.order("code").execute().data
    if not rows:
        return ""

    from collections import defaultdict
    by_cat: dict[str, list[str]] = defaultdict(list)
    for r in rows:
        by_cat[r["category"]].append(f"{r['code']}-{r['name']} ${r['price']//1000}k")

    label = f" ({species})" if species else ""
    lines = [f"Catálogo A3{label}:"]
    for cat, items in by_cat.items():
        lines.append(f"[{cat}] " + ", ".join(items))
    return "\n".join(lines)


def get_individual_tests_context(species: str | None = None) -> str:
    """Compact catalog of individual tests for AI context (custom profile flow)."""
    query = _client.table("catalog_tests").select("code, name, category, price").eq("is_active", True)
    if species and species.lower() in ("canino", "felino"):
        query = query.in_("species", [species.lower(), "ambos"])
    rows = query.order("code").execute().data
    if not rows:
        return ""

    from collections import defaultdict
    by_cat: dict[str, list[str]] = defaultdict(list)
    for r in rows:
        by_cat[r["category"]].append(f"{r['code']}-{r['name']} ${r['price']//1000}k")

    label = f" ({species})" if species else ""
    lines = [f"Análisis individuales A3{label}:"]
    for cat, items in by_cat.items():
        lines.append(f"[{cat}] " + ", ".join(items))
    return "\n".join(lines)


def get_tests_by_codes(codes: list[str]) -> list[dict]:
    if not codes:
        return []
    result = (
        _client.table("catalog_tests")
        .select("code, name, price")
        .in_("code", codes)
        .eq("is_active", True)
        .execute()
    )
    return result.data or []


def get_courier_for_client(client_id: str) -> dict | None:
    result = (
        _client.table("client_courier_assignment")
        .select("courier_id, couriers(id, name, phone, availability)")
        .eq("client_id", client_id)
        .execute()
    )
    if result.data:
        return result.data[0].get("couriers")
    return None


# ── Requests ──────────────────────────────────────────────────────────────────

def create_request(chat_id: str, session: dict, ai_response: dict) -> str | None:
    intent = ai_response["intent"]
    fields = ai_response.get("captured_fields", {})
    client_id = session.get("client_id")
    now = datetime.now(timezone.utc)

    request_data = {
        "client_id":           client_id,
        "entry_channel":       "telegram",
        "service_area":        INTENT_TO_SERVICE_AREA.get(intent, "unknown"),
        "intent":              intent,
        "priority":            "normal",
        "status":              "received",
        "exam_type":           fields.get("exam_type"),
        "patient_name":        fields.get("patient_name"),
        "species":             fields.get("species"),
        "patient_age":         fields.get("patient_age"),
        "owner_name":          fields.get("owner_name"),
        "pickup_address":      fields.get("pickup_address"),
        "requested_at":        now.isoformat(),
        "fallback_reason":     None,
        "assigned_courier_id": None,
        "scheduled_pickup_date": None,
    }

    if intent == "route_scheduling" and client_id:
        courier = get_courier_for_client(client_id)
        if courier:
            request_data["assigned_courier_id"] = courier["id"]
            request_data["status"] = "assigned"
            request_data["scheduled_pickup_date"] = get_scheduled_pickup_date(now).isoformat()
        else:
            request_data["status"] = "error_pending_assignment"
            request_data["fallback_reason"] = "no_courier_assigned"

    elif intent in ("accounting", "new_client"):
        request_data["status"] = "received"
        request_data["fallback_reason"] = ai_response.get("handoff_area")

    result = _client.table("requests").insert(request_data).execute()
    if not result.data:
        return None

    request_id = result.data[0]["id"]
    _client.table("request_events").insert({
        "request_id":     request_id,
        "event_type":     "created",
        "event_payload":  {
            "source":   "telegram",
            "chat_id":  chat_id,
            "intent":   intent,
            "priority": "normal",
            "payment_method": fields.get("payment_method"),
        },
    }).execute()

    return request_id
