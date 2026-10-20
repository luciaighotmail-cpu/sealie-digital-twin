# Sealie Digital Twin R01 — v0.1.0-r01

**SEALIE FEDERATION · PROJECT OMNIS · 20 OCTOBER 2026**

## Controls

| Control | Value |
|---------|--------|
| NEW SPENDING | R0 |
| INITIAL DATA | Synthetic only |
| EXTERNAL ACTIONS | None |
| EXECUTION AUTHORITY | Not granted |

## Included

- Python shared twin service (FastAPI + WebSocket)
- Typed events with fail-closed `SimulationLabel` (rejects MEASURED/VERIFIED)
- Agent/task registry, event store, synthetic fixtures
- Schema + API tests (12 passed locally pre-push)
- Browser observer (`web/index.html`)
- Scene plan, Blueprint guide, governance docs

## Explicitly not included / not verified

- Compiled Unreal project
- Pixel Streaming
- Live / measured telemetry
- Any external write or paid service

## Status

**MODEL** — implementation package for review. Not independently certified.

## Tag instruction

Create annotated tag `v0.1.0-r01` on `main` via GitHub UI Releases or:

```bash
git tag -a v0.1.0-r01 -m "Sealie Digital Twin R01 — MODEL package"
git push origin v0.1.0-r01
```
