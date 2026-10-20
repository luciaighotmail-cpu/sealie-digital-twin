# Sealie Digital Twin R01

**SEALIE FEDERATION · PROJECT OMNIS · REVISION 01 · 20 OCTOBER 2026**

Foundation for a shared 3D environment in which AI agents, software tasks, engineering infrastructure and evidence can be observed from a PC or phone.

**Invariant:** `AUTHORITY ≤ VERIFIED PROOF`

## Delivery controls (binding)

| Control | Value |
|---------|--------|
| NEW SPENDING | **R0** |
| INITIAL DATA | **Synthetic only** |
| EXTERNAL ACTIONS | **None** |
| EXECUTION AUTHORITY | **Not granted** |

Unreal compilation, hardware compatibility, browser streaming (Pixel Streaming) and live integrations are **not verified** in R01.

## What R01 contains

| # | Deliverable | Status in this package |
|---|-------------|------------------------|
| 01 | UE5 digital headquarters (scene plan) | MODEL — documentation + Blueprint guide only |
| 02 | Shared digital-twin service | MODEL — Python API, typed events, agent registry, synthetic telemetry, WebSocket stub |
| 03 | PC and phone interface | MODEL — responsive browser dashboard (read-only); UE client / Pixel Streaming path documented, not built |
| 04 | Blueprint implementation guide | MODEL — actor classes, components, materials, API flow |
| 05 | Tests and verification | MODEL — synthetic fixtures, schema validation, API tests |
| 06 | Federation governance | SUPPORTED — read-only default, simulation labels, audit trail design |

## Quick start (synthetic service only)

```bash
cd sealie-digital-twin
python -m venv .venv && source .venv/bin/activate   # optional
pip install -r requirements.txt
PYTHONPATH=src pytest tests/ -v
PYTHONPATH=src uvicorn sealie_twin.api.main:app --reload --port 8765
# open http://127.0.0.1:8765/docs  and  web/index.html
```

No cloud accounts, no paid APIs, no external network writes.

## Status claim

**MODEL** — implementation specification and source package prepared for review.  
Not PROVEN. Not independently certified. Unreal / streaming / live integrations remain UNVERIFIED.
