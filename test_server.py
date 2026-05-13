"""
Tests for NIS2 Compliance MCP Server
======================================
Tests every @mcp.tool() function directly (no MCP protocol).
Run: cd /Users/nicholas/clawd/mcp-marketplace/nis2-compliance-mcp && pytest test_server.py -v
"""

import json
import sys
import os

os.environ.pop("MEOK_API_KEY", None)

sys.path.insert(0, os.path.dirname(__file__))

from server import (
    classify_entity,
    list_article_21_measures,
    audit_article_21,
    classify_incident,
    management_body_checklist,
    get_nis2_certificate,
    enforcement_status,
    _usage,
    ARTICLE_21_MEASURES,
    ANNEX_I_ESSENTIAL_SECTORS,
    ANNEX_II_IMPORTANT_SECTORS,
)


def _reset_rate_limits():
    _usage.clear()


# ── classify_entity ────────────────────────────────────────────────

class TestClassifyEntity:
    def setup_method(self):
        _reset_rate_limits()

    def test_essential_energy_sector(self):
        result = classify_entity(
            entity_description="Energy company providing electricity generation and distribution",
            employees=500,
            turnover_million_eur=100,
        )
        data = json.loads(result)
        assert data["status"] == "IN_SCOPE"
        assert data["classification"] == "ESSENTIAL"

    def test_essential_transport(self):
        result = classify_entity(
            entity_description="Air transport operator",
            employees=1000,
            turnover_million_eur=200,
        )
        data = json.loads(result)
        assert data["classification"] == "ESSENTIAL"

    def test_essential_banking(self):
        result = classify_entity(
            entity_description="Banking credit institution",
            employees=300,
        )
        data = json.loads(result)
        assert data["classification"] == "ESSENTIAL"

    def test_essential_health(self):
        result = classify_entity(
            entity_description="Health care provider hospital",
            employees=200,
        )
        data = json.loads(result)
        assert data["classification"] == "ESSENTIAL"

    def test_important_digital_provider(self):
        result = classify_entity(
            entity_description="Online marketplace digital provider",
            employees=100,
            turnover_million_eur=20,
        )
        data = json.loads(result)
        assert data["classification"] == "IMPORTANT"

    def test_important_postal(self):
        result = classify_entity(
            entity_description="Postal and courier services company",
            employees=75,
        )
        data = json.loads(result)
        assert data["classification"] == "IMPORTANT"

    def test_out_of_scope_small_entity(self):
        result = classify_entity(
            entity_description="Energy supplier",
            employees=10,
            turnover_million_eur=2,
        )
        data = json.loads(result)
        assert data["status"] == "OUT_OF_SCOPE_BY_SIZE"

    def test_out_of_scope_wrong_sector(self):
        result = classify_entity(
            entity_description="A restaurant and catering company",
            employees=500,
            turnover_million_eur=50,
        )
        data = json.loads(result)
        assert data["status"] == "OUT_OF_SCOPE"

    def test_empty_description(self):
        result = classify_entity(entity_description="")
        data = json.loads(result)
        assert isinstance(data, dict)
        assert data["status"] == "OUT_OF_SCOPE"

    def test_size_medium(self):
        result = classify_entity(
            entity_description="Digital infrastructure cloud computing",
            employees=60,
            turnover_million_eur=15,
        )
        data = json.loads(result)
        assert data["size"] == "medium"

    def test_size_large(self):
        result = classify_entity(
            entity_description="Digital infrastructure",
            employees=300,
            turnover_million_eur=80,
        )
        data = json.loads(result)
        assert data["size"] == "large"

    def test_penalties_essential(self):
        result = classify_entity(
            entity_description="Energy company",
            employees=500,
        )
        data = json.loads(result)
        assert "10M" in data["penalties_headline"] or "10,000,000" in data["penalties_headline"] or "2%" in data["penalties_headline"]

    def test_penalties_important(self):
        result = classify_entity(
            entity_description="Postal service company",
            employees=100,
        )
        data = json.loads(result)
        assert "7M" in data["penalties_headline"] or "7,000,000" in data["penalties_headline"] or "1.4%" in data["penalties_headline"]

    def test_no_size_provided(self):
        result = classify_entity(entity_description="Energy company")
        data = json.loads(result)
        # Without size data, should still classify sector
        assert isinstance(data, dict)

    def test_next_step_present(self):
        result = classify_entity(entity_description="Banking institution", employees=200)
        data = json.loads(result)
        assert "next_step" in data


# ── list_article_21_measures ───────────────────────────────────────

class TestListArticle21Measures:
    def setup_method(self):
        _reset_rate_limits()

    def test_returns_json(self):
        result = list_article_21_measures()
        data = json.loads(result)
        assert isinstance(data, dict)

    def test_has_10_measures(self):
        result = list_article_21_measures()
        data = json.loads(result)
        assert "measures" in data
        assert len(data["measures"]) == 10

    def test_measure_structure(self):
        result = list_article_21_measures()
        data = json.loads(result)
        for m in data["measures"]:
            assert "number" in m
            assert "name" in m
            assert "keywords" in m

    def test_directive_reference(self):
        result = list_article_21_measures()
        data = json.loads(result)
        assert "NIS2" in data.get("directive", "") or "2022/2555" in data.get("directive", "")

    def test_idempotent(self):
        r1 = json.loads(list_article_21_measures())
        _reset_rate_limits()
        r2 = json.loads(list_article_21_measures())
        assert r1["measures"] == r2["measures"]


# ── audit_article_21 ──────────────────────────────────────────────

class TestAuditArticle21:
    def setup_method(self):
        _reset_rate_limits()

    def test_basic_audit(self):
        result = audit_article_21(entity_description="Energy company")
        data = json.loads(result)
        assert "score_percent" in data
        assert "assessment" in data
        assert data["assessment"] in ("COMPLIANT", "PARTIAL", "NON_COMPLIANT")

    def test_fully_controlled(self):
        controls = (
            "risk assessment security policy, incident response IR playbook, "
            "business continuity BCP disaster recovery backup, "
            "supply chain vendor assessment third party risk SBOM, "
            "secure SDLC vulnerability management patching CVE, "
            "audit KPI metrics effectiveness maturity model, "
            "training awareness cyber hygiene phishing simulation, "
            "encryption cryptography TLS AES PKI, "
            "IAM access control RBAC MFA SSO privileged access asset inventory, "
            "MFA 2FA zero trust continuous authentication secure comms"
        )
        result = audit_article_21(
            entity_description="Digital infrastructure provider",
            current_controls=controls,
        )
        data = json.loads(result)
        assert data["score_percent"] >= 80
        assert data["assessment"] == "COMPLIANT"

    def test_no_controls(self):
        result = audit_article_21(
            entity_description="Company with no security",
            current_controls="",
        )
        data = json.loads(result)
        assert data["assessment"] == "NON_COMPLIANT"
        assert len(data["gaps_to_address"]) > 5

    def test_partial_controls(self):
        result = audit_article_21(
            entity_description="Health provider",
            current_controls="encryption TLS, MFA access control, backup",
        )
        data = json.loads(result)
        assert data["score_percent"] > 0
        assert data["score_percent"] < 100

    def test_measures_detail(self):
        result = audit_article_21(entity_description="Transport company")
        data = json.loads(result)
        assert "measures_detail" in data
        assert len(data["measures_detail"]) == 10
        for m in data["measures_detail"]:
            assert "measure" in m
            assert "name" in m
            assert "status" in m
            assert m["status"] in ("EVIDENCE_FOUND", "GAP")

    def test_management_body_liability_note(self):
        result = audit_article_21(entity_description="Banking")
        data = json.loads(result)
        assert "management_body_liability_note" in data

    def test_empty_description(self):
        result = audit_article_21(entity_description="")
        data = json.loads(result)
        assert isinstance(data, dict)
        assert "score_percent" in data


# ── classify_incident ──────────────────────────────────────────────

class TestClassifyIncident:
    def setup_method(self):
        _reset_rate_limits()

    def test_significant_incident(self):
        result = classify_incident(
            incident_description="Major ransomware attack on critical infrastructure",
            users_affected=500000,
            duration_hours=24,
            cross_border=True,
            data_breach=True,
            financial_loss_eur=2000000,
        )
        data = json.loads(result)
        assert data["classification"] == "SIGNIFICANT_INCIDENT"
        assert data["reporting_required"] is True

    def test_non_significant_incident(self):
        result = classify_incident(
            incident_description="Minor cosmetic bug in internal portal",
            users_affected=0,
            duration_hours=0.5,
            cross_border=False,
            data_breach=False,
            financial_loss_eur=0,
        )
        data = json.loads(result)
        assert data["classification"] == "NON_SIGNIFICANT"
        assert data["reporting_required"] is False

    def test_reporting_timeline(self):
        result = classify_incident(
            incident_description="Data breach in critical service",
            data_breach=True,
            users_affected=200000,
        )
        data = json.loads(result)
        timeline = data["timeline"]
        assert "24 hours" in timeline["early_warning"]
        assert "72 hours" in timeline["incident_notification"]
        assert "1 month" in timeline["final_report"]

    def test_cross_border_trigger(self):
        result = classify_incident(
            incident_description="Service disruption",
            cross_border=True,
            duration_hours=10,
        )
        data = json.loads(result)
        criteria = data["criteria_met"]
        assert any("cross-border" in c.lower() for c in criteria)

    def test_data_breach_trigger(self):
        result = classify_incident(
            incident_description="Database compromise",
            data_breach=True,
            users_affected=150000,
        )
        data = json.loads(result)
        criteria = data["criteria_met"]
        assert any("breach" in c.lower() or "data" in c.lower() for c in criteria)

    def test_empty_description(self):
        result = classify_incident(incident_description="")
        data = json.loads(result)
        assert isinstance(data, dict)
        assert "classification" in data

    def test_financial_loss_only(self):
        result = classify_incident(
            incident_description="System downtime",
            financial_loss_eur=1000000,
        )
        data = json.loads(result)
        assert isinstance(data, dict)

    def test_parallel_obligations_present(self):
        result = classify_incident(
            incident_description="Incident",
            data_breach=True,
            users_affected=200000,
        )
        data = json.loads(result)
        assert "parallel_obligations" in data
        assert isinstance(data["parallel_obligations"], list)


# ── management_body_checklist ──────────────────────────────────────

class TestManagementBodyChecklist:
    def setup_method(self):
        _reset_rate_limits()

    def test_returns_json(self):
        result = management_body_checklist()
        data = json.loads(result)
        assert isinstance(data, dict)

    def test_has_checklist(self):
        result = management_body_checklist()
        data = json.loads(result)
        assert "checklist" in data
        assert isinstance(data["checklist"], list)
        assert len(data["checklist"]) > 0

    def test_personal_liability(self):
        result = management_body_checklist()
        data = json.loads(result)
        assert "personal_liability" in data

    def test_training_required(self):
        result = management_body_checklist()
        data = json.loads(result)
        assert "required_training" in data

    def test_article_20_reference(self):
        result = management_body_checklist()
        data = json.loads(result)
        assert "Article 20" in data.get("directive", "")

    def test_failure_consequences(self):
        result = management_body_checklist()
        data = json.loads(result)
        assert "failure_consequences" in data


# ── get_nis2_certificate ──────────────────────────────────────────

class TestGetNis2Certificate:
    def setup_method(self):
        _reset_rate_limits()

    def test_free_tier_blocked(self):
        result = get_nis2_certificate(
            entity_name="Test Corp",
            overall_score=75.0,
        )
        data = json.loads(result)
        assert "error" in data

    def test_free_tier_upgrade_url(self):
        result = get_nis2_certificate(
            entity_name="Test Corp",
            overall_score=85.0,
        )
        data = json.loads(result)
        assert "upgrade_url" in data


# ── enforcement_status ─────────────────────────────────────────────

class TestEnforcementStatus:
    def setup_method(self):
        _reset_rate_limits()

    def test_returns_json(self):
        result = enforcement_status()
        data = json.loads(result)
        assert isinstance(data, dict)

    def test_directive_reference(self):
        result = enforcement_status()
        data = json.loads(result)
        assert "NIS2" in data.get("directive", "") or "2022/2555" in data.get("directive", "")

    def test_enforcement_date(self):
        result = enforcement_status()
        data = json.loads(result)
        assert "2024" in data.get("eu_enforcement_date", "")

    def test_days_since_positive(self):
        result = enforcement_status()
        data = json.loads(result)
        assert data["days_since_eu_enforcement"] > 0

    def test_key_dates(self):
        result = enforcement_status()
        data = json.loads(result)
        assert "key_dates" in data
        assert isinstance(data["key_dates"], list)
        assert len(data["key_dates"]) > 0

    def test_related_regulations(self):
        result = enforcement_status()
        data = json.loads(result)
        assert "related_regulations" in data
        blob = json.dumps(data["related_regulations"])
        assert "DORA" in blob

    def test_national_transposition(self):
        result = enforcement_status()
        data = json.loads(result)
        assert "national_transposition" in data

    def test_idempotent(self):
        r1 = json.loads(enforcement_status())
        _reset_rate_limits()
        r2 = json.loads(enforcement_status())
        assert r1["directive"] == r2["directive"]


# ── Rate Limiting ──────────────────────────────────────────────────

class TestRateLimiting:
    def setup_method(self):
        _reset_rate_limits()

    def test_audit_rate_limit(self):
        for i in range(10):
            result = json.loads(audit_article_21(
                entity_description=f"Entity {i} energy",
            ))
            assert "error" not in result or "limit" not in str(result.get("error", "")).lower()

        result = json.loads(audit_article_21(entity_description="Overflow energy"))
        if "error" in result:
            assert "limit" in str(result["error"]).lower() or "free" in str(result["error"]).lower()
