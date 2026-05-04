"""
Tests de helpers de identificación de cliente (sin I/O de red).
"""


def test_nit_candidates_include_hyphen_and_base_variants():
    from app.services.db import _nit_candidates

    candidates = _nit_candidates("194207252")

    assert "194207252" in candidates
    assert "19420725" in candidates
    assert "19420725-2" in candidates


def test_nit_candidates_preserve_original_input_when_present():
    from app.services.db import _nit_candidates

    candidates = _nit_candidates("19420725-2")

    assert candidates[0] == "19420725-2"
    assert "194207252" in candidates
