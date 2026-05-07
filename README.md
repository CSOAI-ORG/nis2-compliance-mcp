[![nis2-compliance-mcp MCP server](https://glama.ai/mcp/servers/CSOAI-ORG/nis2-compliance-mcp/badges/score.svg)](https://glama.ai/mcp/servers/CSOAI-ORG/nis2-compliance-mcp)
[![MCP Registry](https://img.shields.io/badge/MCP_Registry-Published-green)](https://registry.modelcontextprotocol.io)
[![PyPI](https://img.shields.io/pypi/v/nis2-compliance-mcp)](https://pypi.org/project/nis2-compliance-mcp/)

[![nis2-compliance-mcp MCP server](https://glama.ai/mcp/servers/CSOAI-ORG/nis2-compliance-mcp/badges/card.svg)](https://glama.ai/mcp/servers/CSOAI-ORG/nis2-compliance-mcp)

<div align="center">

[![PyPI](https://img.shields.io/pypi/v/nis2-compliance-mcp)](https://pypi.org/project/nis2-compliance-mcp/)
[![Downloads](https://img.shields.io/pypi/dm/nis2-compliance-mcp)](https://pypi.org/project/nis2-compliance-mcp/)
[![GitHub stars](https://img.shields.io/github/stars/CSOAI-ORG/nis2-compliance-mcp)](https://github.com/CSOAI-ORG/nis2-compliance-mcp/stargazers)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

# NIS2 Compliance MCP

**Automate NIS2 (Directive 2022/2555) compliance for essential and important entities across 18 sectors.**

Transposition deadline: 17 October 2024. Penalties: up to EUR 10M or 2% of global turnover.

[![MEOK AI Labs](https://img.shields.io/badge/MEOK_AI_Labs-224+_servers-purple)](https://meok.ai)

[Install](#install) · [Tools](#tools) · [Pricing](#pricing) · [Attestation API](#attestation-api)

</div>

---

## Why This Exists

NIS2 expanded the scope from ~10,000 entities under NIS1 to an estimated 160,000+ across the EU. If your organisation operates in energy, transport, banking, health, water, digital infrastructure, ICT service management, public administration, space, postal services, waste management, chemicals, food, manufacturing, digital providers, or research — you are in scope.

Member states are transposing NIS2 at different speeds. Germany's BSI NIS2 register (Section 30/32) requires self-registration and incident reporting. This MCP checks your sector classification, maps your obligations under Articles 21 and 23, generates incident notification timelines, and produces supply chain risk assessments — from a single prompt.

## Install

```bash
pip install nis2-compliance-mcp
```

## Tools

| Tool | NIS2 Article | What it does |
|------|-------------|-------------|
| `classify_entity` | Art 3 | Essential vs important entity classification |
| `assess_cybersecurity_measures` | Art 21 | 10-point cybersecurity risk management assessment |
| `plan_incident_reporting` | Art 23 | Incident notification timeline (24h/72h/1mo) |
| `assess_supply_chain` | Art 21(2)(d) | Supply chain security assessment |
| `check_governance` | Art 20 | Management body accountability check |
| `run_full_audit` | All | Complete NIS2 readiness assessment |
| `sign_attestation` | — | HMAC-SHA256 signed compliance certificate |

## Example

```
Prompt: "We're a German SaaS company providing cloud ERP to hospitals.
Classify us under NIS2, check our Article 21 cybersecurity measures,
and generate the BSI registration requirements."

Result: Classified as "important entity" (ICT service management +
healthcare supply chain). Article 21 gap analysis with 3 critical
findings (incident response < 24h not met, supply chain risk
assessment missing, MFA not enforced). BSI Section 30 registration
checklist generated. Each finding signed with attestation cert.
```

## Pricing

| Tier | Price | What you get |
|------|-------|-------------|
| **Free** | £0 | 10 calls/day — entity classification + audit |
| **Pro** | £199/mo | Unlimited + HMAC-signed attestations + verify URLs |
| **Enterprise** | £1,499/mo | Multi-tenant + co-branded reports + webhooks |

[Subscribe to Pro](https://buy.stripe.com/14A4gB3K4eUWgYR56o8k836) · [Enterprise](https://buy.stripe.com/4gM9AV80kaEG0ZT42k8k837)

## Attestation API

```
POST https://meok-attestation-api.vercel.app/sign
GET  https://meok-attestation-api.vercel.app/verify/{cert_id}
```

Zero-dep verifier: `pip install meok-attestation-verify`

## Links

- Website: [meok.ai](https://meok.ai)
- German NIS2 BSI Register: [meok-nis2-de-register-mcp](https://github.com/CSOAI-ORG/meok-nis2-de-register-mcp)
- DORA + NIS2 Crosswalk: [dora-nis2-crosswalk-mcp](https://github.com/CSOAI-ORG/dora-nis2-crosswalk-mcp)
- All MCP servers: [meok.ai/labs/mcp/servers](https://meok.ai/labs/mcp/servers)
- Enterprise support: nicholas@csoai.org

## License

MIT
<!-- mcp-name: io.github.CSOAI-ORG/nis2-compliance-mcp -->
