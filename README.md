<div align="center">

# NIS2 Compliance MCP

**NIS2 Directive (EU 2022/2555) Compliance — Entity Classification, Risk Management, Incident Reporting**

[![MCP](https://img.shields.io/badge/MCP-Server-blue)](https://github.com/CSOAI-ORG)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)
</div>

## Overview

Automated compliance with the NIS2 Directive (EU 2022/2555), the EU's updated cybersecurity framework. Classify entities, audit Article 21 risk-management measures, classify incidents under Article 23, and manage the Register of Information.

## Tools

| Tool | Description | Parameters |
|------|-------------|------------|
| `classify_entity` | Classify entity type (essential/important) and sector | `entity_description`, `sector`, `size` |
| `audit_risk_management` | Audit Article 21 risk-management measures | `measures`, `entity_type` |
| `classify_incident` | Classify an incident per Article 23 criteria | `incident_type`, `impact`, `entities_affected` |
| `generate_register_entry` | Generate Register of Information entry | `entity_name`, `sector`, `measures` |
| `check_supply_chain` | Assess supply chain security requirements | `suppliers`, `critical_services` |
| `reporting_timeline` | Get incident reporting deadlines by severity | `severity`, `entity_type` |
| `gap_analysis` | Full NIS2 compliance gap analysis | `current_state`, `sector`, `entity_type` |

## Installation

```bash
pip install mcp
```

### Claude Desktop
```json
{
  "mcpServers": {
    "nis2-compliance": {
      "command": "python",
      "args": ["path/to/server.py"]
    }
  }
}
```

### Cursor / VS Code / Windsurf
```json
{
  "mcpServers": {
    "nis2-compliance": {
      "command": "python",
      "args": ["path/to/server.py"]
    }
  }
}
```

## Usage Examples

<<<<<<< Updated upstream
MIT © [MEOK AI Labs](https://meok.ai)


## Sister MCPs

Part of the MEOK **Governance** pack — designed to work together as a fleet. Install the whole pack with `npx meok-setup --pack governance`, or pick the ones you need:

- **EU AI Act** → `uvx eu-ai-act-compliance-mcp` · [PyPI](https://pypi.org/project/eu-ai-act-compliance-mcp/) · [GitHub](https://github.com/CSOAI-ORG/eu-ai-act-compliance-mcp)
- **DORA** → `uvx dora-compliance-mcp` · [PyPI](https://pypi.org/project/dora-compliance-mcp/) · [GitHub](https://github.com/CSOAI-ORG/dora-compliance-mcp)
- **Cyber Resilience Act** → `uvx cra-compliance-mcp` · [PyPI](https://pypi.org/project/cra-compliance-mcp/) · [GitHub](https://github.com/CSOAI-ORG/cra-compliance-mcp)
- **AI Bill of Materials** → `uvx ai-bom-mcp` · [PyPI](https://pypi.org/project/ai-bom-mcp/) · [GitHub](https://github.com/CSOAI-ORG/ai-bom-mcp)
- **AI Incident Reporting** → `uvx ai-incident-reporting-mcp` · [PyPI](https://pypi.org/project/ai-incident-reporting-mcp/) · [GitHub](https://github.com/CSOAI-ORG/ai-incident-reporting-mcp)
- **DORA × NIS2 Crosswalk** → `uvx dora-nis2-crosswalk-mcp` · [PyPI](https://pypi.org/project/dora-nis2-crosswalk-mcp/) · [GitHub](https://github.com/CSOAI-ORG/dora-nis2-crosswalk-mcp)

Full catalogue + Anthropic Registry verify links: [meok.ai/anthropic-registry](https://meok.ai/anthropic-registry)

<!-- mcp-name: io.github.CSOAI-ORG/nis2-compliance-mcp -->
=======
### Classify an entity
```json
{
  "entity_description": "Cloud service provider offering SaaS to 500+ healthcare organizations across EU",
  "sector": "digital_infrastructure",
  "size": "large"
}
```

### Audit risk management measures
```json
{
  "measures": ["basic firewall", "quarterly backups", "no encryption"],
  "entity_type": "essential"
}
```

## Pricing

- **Free:** 10 classifications/day
- **Pro:** $99/mo — unlimited audits + reports
- **Enterprise:** $499/mo — full audit trail + supply chain analysis

---

*Built by MEOK AI Labs | [meok.ai](https://meok.ai)*
>>>>>>> Stashed changes
