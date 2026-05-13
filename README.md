<div align="center">

# Nis2 Compliance MCP

**MCP server for nis2 compliance mcp operations**

[![PyPI](https://img.shields.io/pypi/v/meok-nis2-compliance-mcp)](https://pypi.org/project/meok-nis2-compliance-mcp/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![MEOK AI Labs](https://img.shields.io/badge/MEOK_AI_Labs-MCP_Server-purple)](https://meok.ai)

</div>


## Quick Install

| Client | Install |
|--------|---------|
| **Claude Desktop** | [![Install in Claude](https://img.shields.io/badge/Install-Claude-blue)](https://claude.ai) |
| **Cursor** | [![Install in Cursor](https://img.shields.io/badge/Install-Cursor-black)](https://cursor.com) |
| **VS Code** | [![Install in VS Code](https://img.shields.io/badge/Install-VS_Code-blue)](https://code.visualstudio.com) |
| **Windsurf** | [![Install in Windsurf](https://img.shields.io/badge/Install-Windsurf-purple)](https://codeium.com/windsurf) |
| **Docker** | `docker run -p 8000:8000 nis2-compliance-mcp` |
| **pip** | `pip install nis2-compliance-mcp` |

## Overview

Nis2 Compliance MCP provides AI-powered tools via the Model Context Protocol (MCP).

## Tools

| Tool | Description |
|------|-------------|
| `classify_entity` | Classify an entity's NIS2 scope (essential / important / out-of-scope) + sector. |
| `list_article_21_measures` | List all 10 cybersecurity risk-management measures required under NIS2 Article 2 |
| `audit_article_21` | Audit your current controls against NIS2 Article 21's 10 mandatory risk-manageme |
| `classify_incident` | Classify a cyber incident against NIS2 Article 23 thresholds. |
| `management_body_checklist` | NIS2 Article 20 — management body accountability checklist. Directors can be hel |
| `get_nis2_certificate` | Generate a cryptographically signed NIS2 compliance attestation (Pro/Enterprise) |
| `enforcement_status` | Current NIS2 enforcement status + national transposition tracker. |

## Installation

```bash
pip install meok-nis2-compliance-mcp
```

## Usage with Claude Desktop

Add to your Claude Desktop MCP config (`claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "nis2-compliance-mcp": {
      "command": "python",
      "args": ["-m", "meok_nis2_compliance_mcp.server"]
    }
  }
}
```

## Usage with FastMCP

```python
from mcp.server.fastmcp import FastMCP

# This server exposes 7 tool(s) via MCP
# See server.py for full implementation
```

## License

MIT © [MEOK AI Labs](https://meok.ai)

<!-- mcp-name: io.github.CSOAI-ORG/nis2-compliance-mcp -->
