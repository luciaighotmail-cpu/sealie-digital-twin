# Blueprint Implementation Guide (R01)

**Status:** MODEL — guide only. No compiled Blueprints or UE5 project are included.

## Suggested actor classes

| Class | Parent | Responsibility |
|-------|--------|----------------|
| `BP_TwinSceneRoot` | Actor | Holds scene metadata, simulation label, API base URL |
| `BP_AgentWorkstation` | Actor | Visual representation of one agent; binds to `/agents` |
| `BP_TaskBoard` | Actor | Displays open tasks from `/tasks` |
| `BP_TelemetryPanel` | Actor | Shows synthetic samples; always labelled SYNTHETIC |
| `BP_EvidencePlaque` | Actor | Read-only display of event / witness references |
| `BP_CommandCamera` | Pawn / Camera | WATCH-mode fly-through; no possession of world state |

## Components

- `UC_ApiClient` — HTTP GET to twin service; no POST that implies external action.
- `UC_EventStream` — WebSocket subscriber to `/ws/events`.
- `UC_SimulationLabel` — UI widget forced visible on every data surface.

## Materials

- Dark federation palette (deep charcoal, gold accent `#c9a227`).
- Emissive “status” materials for idle / working / blocked (never claim live authority).

## API connection flow

```
BeginPlay
  → Read API base from config (default 127.0.0.1:8765)
  → GET /health  (assert data_policy == SYNTHETIC_ONLY)
  → GET /agents, /tasks, /scene/nodes
  → Open WebSocket /ws/events
  → On message: update bound actors
  → On failure: display explicit UNAVAILABLE state (never fabricate)
```

## Permission model inside UE

- Read-only by default.
- Any future “EXECUTE” interaction requires a separate authority token and is **out of scope for R01**.

## Acceptance for a future UE build (not claimed now)

- [ ] Project opens in target UE5 version without missing plugins
- [ ] All data widgets show SYNTHETIC/MODELLED label
- [ ] Disconnect path shows clear unavailable state
- [ ] No network write except to the approved twin service
- [ ] No spend, no external third-party call
