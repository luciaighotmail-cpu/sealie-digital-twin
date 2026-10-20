# R01 Scene Plan — UE5 Digital Headquarters

**Status:** MODEL — documentation only. Unreal compilation and hardware compatibility are **not verified**.

## Zones

| Zone ID | Name | Purpose |
|---------|------|---------|
| `executive-command-room` | Executive Command Room | Read-only overview, Luci Prime surface, authority boundary display |
| `machine-floor` | Machine Floor | LegionCore / compute substrate visualisation, interlock states |
| `ai-network-hub` | AI Network Hub | Agent registry, message flows, synthetic telemetry feeds |
| `agent-workstations` | Agent Workstations | Per-agent desks, task boards, status indicators |
| `evidence-gallery` | Evidence Gallery | Witness chain / Merkle evidence displays (read-only) |

## Camera & interaction principles

- Default mode: **WATCH** (read-only orbit / fly-through).
- No world mutation without explicit future EXECUTE authority (not granted in R01).
- Every data-bound widget must show a visible **SYNTHETIC** or **MODELLED** label.
- Measured / Verified labels are reserved and must not appear until live data is authorised.

## PC client path

1. UE5 project (to be created under separate approval).
2. Connect to `http://127.0.0.1:8765` REST + `/ws/events` WebSocket.
3. Bind agent / task / telemetry actors to API payloads.

## Phone / browser path

- Responsive observer at `web/index.html` (delivered in R01).
- Later: Pixel Streaming from UE5 (path documented, **not implemented or verified** in R01).

## Non-goals for R01

- Compiled `.uproject` or packaged build
- Hardware-in-the-loop
- Live sensor feeds
- Paid cloud streaming
- Any external write or spend
