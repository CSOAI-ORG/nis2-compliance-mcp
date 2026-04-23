# NIS2 Compliance MCP

**The only MCP server that automates NIS2 (Directive (EU) 2022/2555) compliance** for essential and important entities across the 18 sectors in scope.

Built by [MEOK AI Labs](https://meok.ai). Pairs with our DORA, EU AI Act, ISO 42001, GDPR, and CRA MCPs for full-stack EU regulatory coverage.

## What it does

Give any Claude / ChatGPT / Cursor agent the ability to:

- **Classify your entity** as essential, important, or out-of-scope across 18 sectors
- **Audit all 10 Article 21 risk-management measures** (the minimum cybersecurity baseline)
- **Classify cyber incidents** against Article 23 thresholds (24h / 72h / 1-month reporting)
- **Generate the management-body accountability checklist** under Article 20 (with personal liability)
- **Emit signed certificates** for audit trail and board reporting
- **Track enforcement + national transposition status**

## Install

```bash
pip install nis2-compliance-mcp
```

## Use with Claude Desktop

Add to `~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "nis2": {
      "command": "nis2-compliance-mcp"
    }
  }
}
```

Then ask Claude things like:

- *"Am I in scope for NIS2? I run a German cloud service provider with 300 employees and €60M revenue."*
- *"Audit my Article 21 measures against this list of current controls: ISO 27001, Falcon EDR, Okta SSO, etc."*
- *"Classify this incident: 120,000 customers affected, 4 hours downtime, cross-border impact."*
- *"Generate my Article 20 management-body accountability checklist."*

## Tiers

- **Free** — 10 calls/day, per-measure audits, incident classification, checklists
- **Pro (£49/mo)** — unlimited calls, full Article 21 sweep, **signed certificates**, Article 20 training log generator
- **Enterprise (£499/mo)** — multi-entity, neural-net gap detection, cross-MCP framework crosswalk, audit trail export
- **48-hour written assessment (£5,000)** — senior compliance engineer delivers full NIS2 gap report + remediation plan

## Why it matters

- **Enforcement live since 17 Oct 2024** — national laws rolling out across 27 Member States
- **Essential entity penalties: up to €10M or 2% of global turnover**
- **Important entity penalties: up to €7M or 1.4% of global turnover**
- **Management bodies personally liable** under Article 20 (several Member States already transposed this)
- **Overlaps DORA, GDPR, CRA** — crosswalk MCP (separate) unifies all three

## Legal basis

- Directive (EU) 2022/2555 (NIS2)
- Commission Implementing Regulation laying down technical requirements for specific sectors
- Related: DORA (financial), CRA (products with digital elements), CER Directive (physical resilience)

Automated self-assessment. Not a substitute for national competent-authority review or legal counsel.

## License

MIT. MEOK AI Labs, 2026.
