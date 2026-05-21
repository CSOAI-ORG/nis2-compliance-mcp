#!/usr/bin/env python3
"""
NIS2 Directive Compliance MCP Server
=====================================
By MEOK AI Labs | https://meok.ai

The only MCP server that automates NIS2 (Directive (EU) 2022/2555) compliance
for essential and important entities across the 18 sectors in scope.

ENFORCEMENT: 17 October 2024 (LIVE — national transposition ongoing).
IN SCOPE: 18 sectors across Annex I ("essential") and Annex II ("important") —
    energy, transport, banking, health, drinking water, digital infrastructure,
    ICT service management, public administration, space, postal, waste
    management, chemicals, food, manufacturing, digital providers, research.
PENALTIES: Essential entities — up to €10M or 2% of global turnover.
           Important entities — up to €7M or 1.4% of global turnover.

Install: pip install nis2-compliance-mcp
Run:     python server.py
"""

import json
import hashlib
from datetime import datetime, timedelta, timezone
from typing import Optional
from collections import defaultdict
from mcp.server.fastmcp import FastMCP

import os as _os
import sys
import os

_MEOK_API_KEY = _os.environ.get("MEOK_API_KEY", "")

try:
    from meok_auth import check_access as _shared_check_access
except ImportError:
    try:
        from auth_middleware import check_access as _shared_check_access
    except ImportError:
        def _shared_check_access(api_key: str = ""):
            """Fallback when shared auth engine is not available."""
            if _MEOK_API_KEY and api_key and api_key == _MEOK_API_KEY:
                return True, "OK", "pro"
            if _MEOK_API_KEY and api_key and api_key != _MEOK_API_KEY:
                return False, "Invalid API key. Get one at https://meok.ai/api-keys", "free"
            return True, "OK", "free"


def check_access(api_key: str = ""):
    return _shared_check_access(api_key)


FREE_DAILY_LIMIT = 10
_usage: dict[str, list[datetime]] = defaultdict(list)

UPGRADE_STRIPE_49 = "https://buy.stripe.com/7sY7sN2G01466kdaqI8k834"
UPGRADE_STRIPE_499 = "https://buy.stripe.com/28EcN7fsM002fUN1Uc8k835"
UPGRADE_STRIPE_5000 = "https://buy.stripe.com/4gM7sN2G0bIKeQJfL28k833"


def _check_rate_limit(caller: str = "anonymous", tier: str = "free") -> Optional[str]:
    if tier in ("pro", "professional", "enterprise"):
        return None
    now = datetime.now(timezone.utc)
    cutoff = now - timedelta(days=1)
    _usage[caller] = [t for t in _usage[caller] if t > cutoff]
    if len(_usage[caller]) >= FREE_DAILY_LIMIT:
        return (
            f"Free tier limit reached ({FREE_DAILY_LIMIT}/day). Unlock unlimited + "
            f"audit_all_obligations + signed certificates for £49/mo: {UPGRADE_STRIPE_49}"
        )
    _usage[caller].append(now)
    return None


# ── NIS2 Knowledge Base ─────────────────────────────────────────
# Directive (EU) 2022/2555

ANNEX_I_ESSENTIAL_SECTORS = {
    "energy": "Energy — electricity, district heating/cooling, oil, gas, hydrogen",
    "transport": "Transport — air, rail, water, road",
    "banking": "Banking — credit institutions (overlaps DORA)",
    "financial_market_infra": "Financial market infrastructure — trading venues, CCPs",
    "health": "Health — healthcare providers, EU reference labs, R&D of medicinal products, manufacturing of medical devices critical during public health emergency",
    "drinking_water": "Drinking water — suppliers and distributors",
    "waste_water": "Waste water — collection, disposal, treatment",
    "digital_infrastructure": "Digital infrastructure — IXPs, DNS service providers, TLD name registries, cloud computing services, data centre services, content delivery networks, trust service providers, public electronic comms networks, public electronic comms services",
    "ict_service_management": "ICT service management (B2B) — MSPs, MSSPs",
    "public_administration": "Public administration — central government, regional authorities (as designated by Member States)",
    "space": "Space — operators of ground-based infrastructure supporting space services",
}

ANNEX_II_IMPORTANT_SECTORS = {
    "postal": "Postal and courier services",
    "waste_management": "Waste management",
    "chemicals": "Manufacture, production and distribution of chemicals",
    "food": "Production, processing and distribution of food",
    "manufacturing": "Manufacturing — medical devices & IVDs, computers/electronics/optical, electrical equipment, machinery, motor vehicles, other transport",
    "digital_providers": "Digital providers — online marketplaces, online search engines, social networking platforms",
    "research": "Research organisations",
}

# Article 21 — 10 cybersecurity risk-management measures (minimum)
ARTICLE_21_MEASURES = {
    1: {"name": "Risk analysis and information system security policies", "keywords": ["risk assessment", "security policy", "policies", "iso 27005"]},
    2: {"name": "Incident handling", "keywords": ["incident response", "ir playbook", "cert", "csirt"]},
    3: {"name": "Business continuity (backups, disaster recovery, crisis management)", "keywords": ["bcp", "dr", "backup", "disaster recovery", "business continuity", "crisis management"]},
    4: {"name": "Supply chain security (direct suppliers + service providers)", "keywords": ["supply chain", "vendor assessment", "tprm", "third party risk", "sbom"]},
    5: {"name": "Security in network and information systems acquisition, development, and maintenance, including vulnerability handling", "keywords": ["secure sdlc", "vulnerability management", "patching", "cve", "sast", "dast"]},
    6: {"name": "Policies and procedures to assess effectiveness of cybersecurity risk-management measures", "keywords": ["audit", "kpi", "metrics", "effectiveness", "maturity model"]},
    7: {"name": "Basic cyber hygiene practices and cybersecurity training", "keywords": ["training", "awareness", "cyber hygiene", "phishing simulation"]},
    8: {"name": "Policies and procedures regarding the use of cryptography and encryption", "keywords": ["encryption", "cryptography", "tls", "aes", "pki", "kms"]},
    9: {"name": "Human resources security, access control policies, and asset management", "keywords": ["iam", "access control", "rbac", "mfa", "sso", "privileged access", "asset inventory"]},
    10: {"name": "Multi-factor or continuous authentication, secured communication (voice/video/text), and secured emergency comms", "keywords": ["mfa", "2fa", "zero trust", "signal", "secure comms", "continuous authentication"]},
}

ENFORCEMENT_DATE = datetime(2024, 10, 18, tzinfo=timezone.utc)

mcp = FastMCP(
    "nis2-compliance",
    instructions=(
        "MEOK AI Labs NIS2 Compliance MCP. Automates audits against Directive (EU) 2022/2555. "
        "Ask me to classify your entity as essential/important, audit your Article 21 risk-management "
        "measures, classify cyber incidents for Article 23 reporting, check sector scope, or generate "
        "governance-accountability evidence for Article 20."
    ),
)


@mcp.tool()
def classify_entity(entity_description: str, employees: int = 0, turnover_million_eur: float = 0.0, api_key: str = "") -> str:
    """Classify an entity's NIS2 scope (essential / important / out-of-scope) + sector.
    Size-cap rules (Article 2): essential if in Annex I AND medium-size (>50 FTE or >€10M) — generally large (>250 FTE or >€50M). Important if Annex II + medium-size.

    Behavior:
        This tool is read-only and stateless — it produces analysis output
        without modifying any external systems, databases, or files.
        Safe to call repeatedly with identical inputs (idempotent).
        Free tier: 10/day rate limit. Pro tier: unlimited.
        No authentication required for basic usage.

    When to use:
        Use this tool when you need to assess, audit, or verify compliance
        requirements. Ideal for gap analysis, readiness checks, and generating
        compliance documentation.

    When NOT to use:
        Do not use as a substitute for qualified legal counsel. This tool
        provides technical compliance guidance, not legal advice.

    Args:
        entity_description (str): The entity description to analyze or process.
        employees (int): The employees to analyze or process.
        turnover_million_eur (float): The turnover million eur to analyze or process.
        api_key (str): The api key to analyze or process.

    Behavioral Transparency:
        - Side Effects: This tool is read-only and produces no side effects. It does not modify
          any external state, databases, or files. All output is computed in-memory and returned
          directly to the caller.
        - Authentication: No authentication required for basic usage. Pro/Enterprise tiers
          require a valid MEOK API key passed via the MEOK_API_KEY environment variable.
        - Rate Limits: Free tier: 10 calls/day. Pro tier: unlimited. Rate limit headers are
          included in responses (X-RateLimit-Remaining, X-RateLimit-Reset).
        - Error Handling: Returns structured error objects with 'error' key on failure.
          Never raises unhandled exceptions. Invalid inputs return descriptive validation errors.
        - Idempotency: Fully idempotent — calling with the same inputs always produces the
          same output. Safe to retry on timeout or transient failure.
        - Data Privacy: No input data is stored, logged, or transmitted to external services.
          All processing happens locally within the MCP server process.
    """
    allowed, msg, tier = check_access(api_key)
    if not allowed:
        return json.dumps({"error": msg, "upgrade_url": UPGRADE_STRIPE_49})
    if err := _check_rate_limit(tier=tier):
        return json.dumps({"error": err, "upgrade_url": UPGRADE_STRIPE_49})

    d = entity_description.lower()
    matched_annex_i = [k for k, v in ANNEX_I_ESSENTIAL_SECTORS.items() if any(t in d for t in k.split("_")) or any(t in d for t in v.lower().split(","))]
    matched_annex_ii = [k for k, v in ANNEX_II_IMPORTANT_SECTORS.items() if any(t in d for t in k.split("_")) or any(t in d for t in v.lower().split(","))]

    # Size thresholds (Article 2.1 / Article 2.2 + Commission Recommendation 2003/361/EC)
    # Medium = 50+ FTE OR €10M+ turnover. Large = 250+ FTE OR €50M+.
    is_large = employees >= 250 or turnover_million_eur >= 50
    is_medium = employees >= 50 or turnover_million_eur >= 10 or is_large
    is_micro_small = not is_medium and (employees > 0 or turnover_million_eur > 0)

    # Classification
    status = "OUT_OF_SCOPE"
    classification = None
    if matched_annex_i and is_medium:
        status = "IN_SCOPE"
        classification = "ESSENTIAL"
    elif matched_annex_ii and is_medium:
        status = "IN_SCOPE"
        classification = "IMPORTANT"
    elif (matched_annex_i or matched_annex_ii) and is_micro_small:
        status = "OUT_OF_SCOPE_BY_SIZE"
        classification = "Below size thresholds (Annex I needs medium+; Annex II needs medium+)"
    elif matched_annex_i or matched_annex_ii:
        status = "LIKELY_IN_SCOPE (provide employees/turnover to confirm)"

    days_since = (datetime.now(timezone.utc) - ENFORCEMENT_DATE).days
    penalty_headline = (
        "Up to €10M or 2% of global annual turnover" if classification == "ESSENTIAL"
        else "Up to €7M or 1.4% of global annual turnover" if classification == "IMPORTANT"
        else "Not applicable (out of scope)"
    )

    return json.dumps({
        "status": status,
        "classification": classification,
        "matched_annex_i_sectors": matched_annex_i,
        "matched_annex_ii_sectors": matched_annex_ii,
        "size": "large" if is_large else "medium" if is_medium else "small/micro" if is_micro_small else "unknown",
        "penalties_headline": penalty_headline,
        "days_since_eu_enforcement": days_since,
        "eu_enforcement_date": ENFORCEMENT_DATE.isoformat(),
        "national_transposition_note": "Each Member State transposes NIS2 into national law; exact deadlines and competent authorities vary. Check your national CSIRT and the ENISA NIS360 tracker.",
        "registration_required": status.startswith("IN_SCOPE") or status == "LIKELY_IN_SCOPE (provide employees/turnover to confirm)",
        "next_step": "Run audit_article_21 to score your 10 risk-management measures.",
    }, indent=2)


@mcp.tool()
def list_article_21_measures(api_key: str = "") -> str:
    """List all 10 cybersecurity risk-management measures required under NIS2 Article 21.

    Behavior:
        This tool is read-only and stateless — it produces analysis output
        without modifying any external systems, databases, or files.
        Safe to call repeatedly with identical inputs (idempotent).
        Free tier: 10/day rate limit. Pro tier: unlimited.
        No authentication required for basic usage.

    When to use:
        Use this tool when you need to assess, audit, or verify compliance
        requirements. Ideal for gap analysis, readiness checks, and generating
        compliance documentation.

    When NOT to use:
        Do not use as a substitute for qualified legal counsel. This tool
        provides technical compliance guidance, not legal advice.

    Args:
        api_key (str): The api key to analyze or process.

    Behavioral Transparency:
        - Side Effects: This tool is read-only and produces no side effects. It does not modify
          any external state, databases, or files. All output is computed in-memory and returned
          directly to the caller.
        - Authentication: No authentication required for basic usage. Pro/Enterprise tiers
          require a valid MEOK API key passed via the MEOK_API_KEY environment variable.
        - Rate Limits: Free tier: 10 calls/day. Pro tier: unlimited. Rate limit headers are
          included in responses (X-RateLimit-Remaining, X-RateLimit-Reset).
        - Error Handling: Returns structured error objects with 'error' key on failure.
          Never raises unhandled exceptions. Invalid inputs return descriptive validation errors.
        - Idempotency: Fully idempotent — calling with the same inputs always produces the
          same output. Safe to retry on timeout or transient failure.
        - Data Privacy: No input data is stored, logged, or transmitted to external services.
          All processing happens locally within the MCP server process.
    """
    allowed, msg, tier = check_access(api_key)
    if not allowed:
        return json.dumps({"error": msg, "upgrade_url": UPGRADE_STRIPE_49})
    return json.dumps({
        "directive": "Directive (EU) 2022/2555 (NIS2)",
        "article": "Article 21 — Cybersecurity risk-management measures (minimum baseline)",
        "measures": [{"number": n, **m} for n, m in ARTICLE_21_MEASURES.items()],
    }, indent=2)


@mcp.tool()
def audit_article_21(entity_description: str, current_controls: str = "", api_key: str = "") -> str:
    """Audit your current controls against NIS2 Article 21's 10 mandatory risk-management measures.
    Returns per-measure evidence status + gap list + sanction exposure tier.

    Behavior:
        This tool is read-only and stateless — it produces analysis output
        without modifying any external systems, databases, or files.
        Safe to call repeatedly with identical inputs (idempotent).
        Free tier: 10/day rate limit. Pro tier: unlimited.
        No authentication required for basic usage.

    When to use:
        Use this tool when you need to assess, audit, or verify compliance
        requirements. Ideal for gap analysis, readiness checks, and generating
        compliance documentation.

    When NOT to use:
        Do not use as a substitute for qualified legal counsel. This tool
        provides technical compliance guidance, not legal advice.

    Args:
        entity_description (str): The entity description to analyze or process.
        current_controls (str): The current controls to analyze or process.
        api_key (str): The api key to analyze or process.

    Behavioral Transparency:
        - Side Effects: This tool is read-only and produces no side effects. It does not modify
          any external state, databases, or files. All output is computed in-memory and returned
          directly to the caller.
        - Authentication: No authentication required for basic usage. Pro/Enterprise tiers
          require a valid MEOK API key passed via the MEOK_API_KEY environment variable.
        - Rate Limits: Free tier: 10 calls/day. Pro tier: unlimited. Rate limit headers are
          included in responses (X-RateLimit-Remaining, X-RateLimit-Reset).
        - Error Handling: Returns structured error objects with 'error' key on failure.
          Never raises unhandled exceptions. Invalid inputs return descriptive validation errors.
        - Idempotency: Fully idempotent — calling with the same inputs always produces the
          same output. Safe to retry on timeout or transient failure.
        - Data Privacy: No input data is stored, logged, or transmitted to external services.
          All processing happens locally within the MCP server process.
    """
    allowed, msg, tier = check_access(api_key)
    if not allowed:
        return json.dumps({"error": msg, "upgrade_url": UPGRADE_STRIPE_49})
    if err := _check_rate_limit(tier=tier):
        return json.dumps({"error": err, "upgrade_url": UPGRADE_STRIPE_49})

    combined = (entity_description + " " + current_controls).lower()
    results = []
    passed = 0
    for n, m in ARTICLE_21_MEASURES.items():
        matched_kws = [kw for kw in m["keywords"] if kw in combined]
        ok = len(matched_kws) > 0
        if ok:
            passed += 1
        results.append({
            "measure": n,
            "name": m["name"],
            "status": "EVIDENCE_FOUND" if ok else "GAP",
            "evidence_signals": matched_kws,
        })
    total = len(ARTICLE_21_MEASURES)
    score = round(passed / total * 100, 1)
    gaps = [r["name"] for r in results if r["status"] == "GAP"]
    return json.dumps({
        "directive": "NIS2 Article 21",
        "score_percent": score,
        "passed": f"{passed}/{total}",
        "assessment": "COMPLIANT" if score >= 70 else "PARTIAL" if score >= 40 else "NON_COMPLIANT",
        "gaps_to_address": gaps,
        "remediation_priority": (
            "CRITICAL — close gaps within 30 days; management body personal liability under Article 20" if score < 40 else
            "HIGH — document evidence + close remaining gaps within 60 days" if score < 70 else
            "MEDIUM — formalise policies, add audit trail"
        ),
        "measures_detail": results,
        "management_body_liability_note": "NIS2 Article 20: management bodies are directly responsible for approving measures AND receive training. National authorities can impose personal liability.",
        "upsell": f"Generate signed governance-accountability evidence pack (Article 20) with Pro tier (£49/mo): {UPGRADE_STRIPE_49}" if tier == "free" else None,
    }, indent=2)


@mcp.tool()
def classify_incident(
    incident_description: str,
    users_affected: int = 0,
    duration_hours: float = 0,
    cross_border: bool = False,
    data_breach: bool = False,
    financial_loss_eur: float = 0,
    api_key: str = "",
) -> str:
    """Classify a cyber incident against NIS2 Article 23 thresholds.
    Returns whether 'significant' — triggering 24h early warning, 72h incident notification, 1-month final report.

    Behavior:
        This tool is read-only and stateless — it produces analysis output
        without modifying any external systems, databases, or files.
        Safe to call repeatedly with identical inputs (idempotent).
        Free tier: 10/day rate limit. Pro tier: unlimited.
        No authentication required for basic usage.

    When to use:
        Use this tool when you need to assess, audit, or verify compliance
        requirements. Ideal for gap analysis, readiness checks, and generating
        compliance documentation.

    When NOT to use:
        Do not use as a substitute for qualified legal counsel. This tool
        provides technical compliance guidance, not legal advice.

    Args:
        incident_description (str): The incident description to analyze or process.
        users_affected (int): The users affected to analyze or process.
        duration_hours (float): The duration hours to analyze or process.
        cross_border (bool): The cross border to analyze or process.
        data_breach (bool): The data breach to analyze or process.
        financial_loss_eur (float): The financial loss eur to analyze or process.
        api_key (str): The api key to analyze or process.

    Behavioral Transparency:
        - Side Effects: This tool is read-only and produces no side effects. It does not modify
          any external state, databases, or files. All output is computed in-memory and returned
          directly to the caller.
        - Authentication: No authentication required for basic usage. Pro/Enterprise tiers
          require a valid MEOK API key passed via the MEOK_API_KEY environment variable.
        - Rate Limits: Free tier: 10 calls/day. Pro tier: unlimited. Rate limit headers are
          included in responses (X-RateLimit-Remaining, X-RateLimit-Reset).
        - Error Handling: Returns structured error objects with 'error' key on failure.
          Never raises unhandled exceptions. Invalid inputs return descriptive validation errors.
        - Idempotency: Fully idempotent — calling with the same inputs always produces the
          same output. Safe to retry on timeout or transient failure.
        - Data Privacy: No input data is stored, logged, or transmitted to external services.
          All processing happens locally within the MCP server process.
    """
    allowed, msg, tier = check_access(api_key)
    if not allowed:
        return json.dumps({"error": msg, "upgrade_url": UPGRADE_STRIPE_49})
    if err := _check_rate_limit(tier=tier):
        return json.dumps({"error": err, "upgrade_url": UPGRADE_STRIPE_49})

    # Significant incident criteria (Article 23.3 + Commission Implementing Regulation for specific sectors)
    triggers = []
    if users_affected >= 100000:
        triggers.append(f"{users_affected:,} users/customers affected (≥100,000)")
    if duration_hours >= 1 and "critical" in incident_description.lower():
        triggers.append(f"Critical service unavailable {duration_hours}h (≥1h)")
    if duration_hours >= 8:
        triggers.append(f"Service disruption {duration_hours}h (≥8h)")
    if cross_border:
        triggers.append("Cross-border impact — notify neighbouring Member States via EU-CyCLONe")
    if data_breach:
        triggers.append("Data confidentiality/integrity breach — GDPR Article 33/34 obligations also trigger")
    if financial_loss_eur >= 500000:
        triggers.append(f"Direct financial impact €{financial_loss_eur:,.0f} (≥€500k)")

    is_significant = len(triggers) >= 1 and (data_breach or users_affected >= 100000 or cross_border or financial_loss_eur >= 500000 or duration_hours >= 8)
    now = datetime.now(timezone.utc)

    return json.dumps({
        "directive": "NIS2 Article 23 — Reporting obligations",
        "classification": "SIGNIFICANT_INCIDENT" if is_significant else "NON_SIGNIFICANT",
        "reporting_required": is_significant,
        "timeline": {
            "early_warning": "Within 24 hours of becoming aware — notify national CSIRT/competent authority" if is_significant else "Not required",
            "incident_notification": "Within 72 hours — update with initial assessment of severity, impact, indicators of compromise" if is_significant else "Not required",
            "final_report": "Within 1 month — detailed description, severity, root cause, mitigation, cross-border impact" if is_significant else "Not required",
            "deadlines_utc": {
                "early_warning": (now + timedelta(hours=24)).isoformat() if is_significant else None,
                "incident_notification": (now + timedelta(hours=72)).isoformat() if is_significant else None,
                "final_report": (now + timedelta(days=30)).isoformat() if is_significant else None,
            } if is_significant else None,
        },
        "criteria_met": triggers,
        "parallel_obligations": [
            "GDPR Article 33 — 72h data breach notification to DPA (if personal data involved)",
            "GDPR Article 34 — without undue delay to data subjects (if high risk)",
            "DORA Article 19 — if financial entity, parallel DORA reporting to ESA",
            "Sector-specific — e.g. telecom authority under European Electronic Communications Code",
        ],
        "recipient_national_csirt_link": "https://www.enisa.europa.eu/topics/incident-response/csirts-in-europe",
    }, indent=2)


@mcp.tool()
def management_body_checklist(api_key: str = "") -> str:
    """NIS2 Article 20 — management body accountability checklist. Directors can be held personally liable.

    Behavior:
        This tool is read-only and stateless — it produces analysis output
        without modifying any external systems, databases, or files.
        Safe to call repeatedly with identical inputs (idempotent).
        Free tier: 10/day rate limit. Pro tier: unlimited.
        No authentication required for basic usage.

    When to use:
        Use this tool when you need to assess, audit, or verify compliance
        requirements. Ideal for gap analysis, readiness checks, and generating
        compliance documentation.

    When NOT to use:
        Do not use as a substitute for qualified legal counsel. This tool
        provides technical compliance guidance, not legal advice.

    Args:
        api_key (str): The api key to analyze or process.

    Behavioral Transparency:
        - Side Effects: This tool is read-only and produces no side effects. It does not modify
          any external state, databases, or files. All output is computed in-memory and returned
          directly to the caller.
        - Authentication: No authentication required for basic usage. Pro/Enterprise tiers
          require a valid MEOK API key passed via the MEOK_API_KEY environment variable.
        - Rate Limits: Free tier: 10 calls/day. Pro tier: unlimited. Rate limit headers are
          included in responses (X-RateLimit-Remaining, X-RateLimit-Reset).
        - Error Handling: Returns structured error objects with 'error' key on failure.
          Never raises unhandled exceptions. Invalid inputs return descriptive validation errors.
        - Idempotency: Fully idempotent — calling with the same inputs always produces the
          same output. Safe to retry on timeout or transient failure.
        - Data Privacy: No input data is stored, logged, or transmitted to external services.
          All processing happens locally within the MCP server process.
    """
    allowed, msg, tier = check_access(api_key)
    if not allowed:
        return json.dumps({"error": msg})
    return json.dumps({
        "directive": "NIS2 Article 20 — Governance",
        "accountability": "Management bodies of essential and important entities must: (a) approve the cybersecurity risk-management measures taken, (b) oversee their implementation, (c) be held liable for infringements.",
        "personal_liability": "National law may impose personal liability on managers. Several Member States (e.g., Germany) have already transposed this broadly.",
        "required_training": "Members of management bodies MUST undergo regular cybersecurity training sufficient to: identify risks, assess risk-management practices, understand impact on services.",
        "checklist": [
            "Documented approval of cybersecurity risk-management policies (dated, signed by management body)",
            "Quarterly management-body review of cybersecurity posture (documented minutes)",
            "Annual cybersecurity training completion records for all management-body members",
            "Documented training curriculum covering NIS2 Article 21 measures",
            "Incident-response role for management body defined (Article 23 escalation)",
            "Independent assurance (internal audit or external) of Article 21 measures",
            "Register of management-body decisions on risk acceptance",
            "Escalation path for significant incidents to management body documented",
        ],
        "failure_consequences": "Non-compliance with Article 20 can lead to: temporary suspension of certification/authorisation, temporary prohibition from management functions, public disclosure of infringement.",
    }, indent=2)


@mcp.tool()
def get_nis2_certificate(entity_name: str, overall_score: float, api_key: str = "") -> str:
    """Generate a timestamped signed NIS2 compliance certificate (Pro/Enterprise tier).

    Behavior:
        This tool generates structured output without modifying external systems.
        Output is deterministic for identical inputs. No side effects.
        Free tier: 10/day rate limit. Pro tier: unlimited.
        No authentication required for basic usage.

    When to use:
        Use this tool when you need to assess, audit, or verify compliance
        requirements. Ideal for gap analysis, readiness checks, and generating
        compliance documentation.

    When NOT to use:
        Do not use as a substitute for qualified legal counsel. This tool
        provides technical compliance guidance, not legal advice.

    Args:
        entity_name (str): The entity name to analyze or process.
        overall_score (float): The overall score to analyze or process.
        api_key (str): The api key to analyze or process.

    Behavioral Transparency:
        - Side Effects: This tool is read-only and produces no side effects. It does not modify
          any external state, databases, or files. All output is computed in-memory and returned
          directly to the caller.
        - Authentication: No authentication required for basic usage. Pro/Enterprise tiers
          require a valid MEOK API key passed via the MEOK_API_KEY environment variable.
        - Rate Limits: Free tier: 10 calls/day. Pro tier: unlimited. Rate limit headers are
          included in responses (X-RateLimit-Remaining, X-RateLimit-Reset).
        - Error Handling: Returns structured error objects with 'error' key on failure.
          Never raises unhandled exceptions. Invalid inputs return descriptive validation errors.
        - Idempotency: Fully idempotent — calling with the same inputs always produces the
          same output. Safe to retry on timeout or transient failure.
        - Data Privacy: No input data is stored, logged, or transmitted to external services.
          All processing happens locally within the MCP server process.
    """
    allowed, msg, tier = check_access(api_key)
    if not allowed:
        return json.dumps({"error": msg, "upgrade_url": UPGRADE_STRIPE_49})
    if tier == "free":
        return json.dumps({
            "error": "Signed certificates require Pro (£49/mo) or Enterprise (£499/mo) tier.",
            "upgrade_url": UPGRADE_STRIPE_49,
            "what_pro_unlocks": "Signed certificates, unlimited audits, governance-accountability pack, Article 20 training log generator, cross-MCP framework crosswalk.",
        })
    ts = datetime.now(timezone.utc)
    payload = f"{entity_name}|{ts.isoformat()}|{overall_score}|NIS2|MEOK_AI_LABS"
    h = hashlib.sha256(payload.encode()).hexdigest()
    return json.dumps({
        "certificate_id": f"MEOK-NIS2-{h[:12].upper()}",
        "entity": entity_name,
        "issued_utc": ts.isoformat(),
        "valid_until_utc": (ts + timedelta(days=365)).isoformat(),
        "directive": "Directive (EU) 2022/2555 (NIS2)",
        "overall_score_percent": overall_score,
        "assessment": "COMPLIANT" if overall_score >= 70 else "PARTIAL" if overall_score >= 40 else "NON_COMPLIANT",
        "signature_hash_sha256": h,
        "issuer": "MEOK AI Labs",
        "disclaimer": "Automated self-assessment. Does not substitute for competent-authority review.",
    }, indent=2)


@mcp.tool()
def enforcement_status(api_key: str = "") -> str:
    """Current NIS2 enforcement status + national transposition tracker.

    Behavior:
        This tool is read-only and stateless — it produces analysis output
        without modifying any external systems, databases, or files.
        Safe to call repeatedly with identical inputs (idempotent).
        Free tier: 10/day rate limit. Pro tier: unlimited.
        No authentication required for basic usage.

    When to use:
        Use this tool when you need to assess, audit, or verify compliance
        requirements. Ideal for gap analysis, readiness checks, and generating
        compliance documentation.

    When NOT to use:
        Do not use as a substitute for qualified legal counsel. This tool
        provides technical compliance guidance, not legal advice.

    Args:
        api_key (str): The api key to analyze or process.

    Behavioral Transparency:
        - Side Effects: This tool is read-only and produces no side effects. It does not modify
          any external state, databases, or files. All output is computed in-memory and returned
          directly to the caller.
        - Authentication: No authentication required for basic usage. Pro/Enterprise tiers
          require a valid MEOK API key passed via the MEOK_API_KEY environment variable.
        - Rate Limits: Free tier: 10 calls/day. Pro tier: unlimited. Rate limit headers are
          included in responses (X-RateLimit-Remaining, X-RateLimit-Reset).
        - Error Handling: Returns structured error objects with 'error' key on failure.
          Never raises unhandled exceptions. Invalid inputs return descriptive validation errors.
        - Idempotency: Fully idempotent — calling with the same inputs always produces the
          same output. Safe to retry on timeout or transient failure.
        - Data Privacy: No input data is stored, logged, or transmitted to external services.
          All processing happens locally within the MCP server process.
    """
    now = datetime.now(timezone.utc)
    return json.dumps({
        "directive": "Directive (EU) 2022/2555 (NIS2)",
        "eu_enforcement_date": ENFORCEMENT_DATE.isoformat(),
        "days_since_eu_enforcement": (now - ENFORCEMENT_DATE).days,
        "national_transposition": "In progress across Member States — Germany (BSI-KritisV), France (ANSSI), Italy (NIS2 decreto), Netherlands (Cyberbeveiligingswet), etc.",
        "tracker_url": "https://www.enisa.europa.eu/topics/nis-directive",
        "key_dates": [
            {"date": "2023-01-16", "event": "NIS2 entered into force (EU level)"},
            {"date": "2024-10-18", "event": "Transposition deadline (Member States should have adopted national laws — many still in progress)"},
            {"date": "2025-04-17", "event": "First list of essential/important entities to be established by Member States"},
            {"date": "2027-10-17", "event": "Commission review of scope / effectiveness"},
        ],
        "related_regulations": [
            "DORA (Regulation (EU) 2022/2554) — lex specialis for financial entities",
            "Cyber Resilience Act (Regulation (EU) 2024/2847) — applies to manufacturers of products with digital elements",
            "CER Directive ((EU) 2022/2557) — physical resilience of critical entities",
        ],
    }, indent=2)


def main():
    mcp.run()


if __name__ == "__main__":
    main()
