# Federation Governance — Digital Twin R01

## Defaults

| Rule | Value |
|------|--------|
| Access mode | Read-only |
| Data provenance | Visible simulation labels on every record |
| Approvals | Explicit human approval required for any EXECUTE-class change |
| Audit | Append-only event trail (`/events/audit`) |

## Labels

| Label | Meaning in R01 |
|-------|----------------|
| SYNTHETIC | Generated fixtures / bootstrap data |
| MODELLED | Derived from models, not live measurement |
| MEASURED | Forbidden until live telemetry is authorised |
| VERIFIED | Forbidden until independent evidence exists |

## Event trail

Every accepted `TwinEvent` is stored with:

- `id`, `kind`, `timestamp`, `source`
- `label` (mandatory)
- `payload`, optional `evidence_ref`, optional `scene_node`

Consumers must treat the trail as integrity of the recorded event, not proof of external reality.

## Authority boundary

- R01 grants **no** execution authority.
- The twin service does not call LegionCore, Luci, or any production system.
- Future linkage requires a separate approval gate and evidence package.
