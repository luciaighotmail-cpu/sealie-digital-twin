"""Schema and policy tests for TwinEvent."""

import pytest
from sealie_twin.models.events import TwinEvent, EventKind, SimulationLabel


def test_synthetic_event_ok():
    ev = TwinEvent(
        kind=EventKind.AGENT_SPAWN,
        source="agent-test",
        label=SimulationLabel.SYNTHETIC,
        payload={"ok": True},
    )
    assert ev.label == SimulationLabel.SYNTHETIC
    assert ev.id


def test_measured_label_rejected_in_r01():
    with pytest.raises(ValueError, match="R01 forbids"):
        TwinEvent(
            kind=EventKind.TELEMETRY,
            source="sensor",
            label=SimulationLabel.MEASURED,
            payload={},
        )


def test_verified_label_rejected_in_r01():
    with pytest.raises(ValueError, match="R01 forbids"):
        TwinEvent(
            kind=EventKind.EVIDENCE_ATTACHED,
            source="auditor",
            label=SimulationLabel.VERIFIED,
            payload={},
        )


def test_audit_dict_shape():
    ev = TwinEvent(
        kind=EventKind.SCENE_HEARTBEAT,
        source="twin-service",
        label=SimulationLabel.SYNTHETIC,
    )
    d = ev.to_audit_dict()
    assert set(d.keys()) >= {"id", "kind", "timestamp", "source", "label", "payload"}
