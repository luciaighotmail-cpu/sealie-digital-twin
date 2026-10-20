"""
Synthetic bootstrap data for R01.
All records are explicitly labelled SYNTHETIC.
"""

from __future__ import annotations

from uuid import uuid4

from sealie_twin.models.events import (
    AgentRecord,
    TaskRecord,
    TwinEvent,
    EventKind,
    SimulationLabel,
    TelemetrySample,
)
from sealie_twin.services.registry import AgentRegistry, TaskRegistry
from sealie_twin.services.event_store import EventStore


SCENE_NODES = [
    "executive-command-room",
    "machine-floor",
    "ai-network-hub",
    "agent-workstations",
    "evidence-gallery",
]


def bootstrap_agents(registry: AgentRegistry) -> list[AgentRecord]:
    agents = [
        AgentRecord(
            id="agent-luci-01",
            name="Luci Observer",
            role="cognitive-os",
            status="idle",
            workstation="agent-workstations",
            label=SimulationLabel.SYNTHETIC,
            meta={"panel": "Luci Prime HOLD surface"},
        ),
        AgentRecord(
            id="agent-legion-01",
            name="LegionCore Worker",
            role="authority-substrate",
            status="working",
            workstation="machine-floor",
            label=SimulationLabel.SYNTHETIC,
        ),
        AgentRecord(
            id="agent-omnis-01",
            name="OMNIS Corridor Monitor",
            role="infrastructure",
            status="idle",
            workstation="ai-network-hub",
            label=SimulationLabel.SYNTHETIC,
            meta={"region": "Gauteng"},
        ),
    ]
    for a in agents:
        registry.register(a)
    return agents


def bootstrap_tasks(registry: TaskRegistry) -> list[TaskRecord]:
    tasks = [
        TaskRecord(
            id=str(uuid4()),
            title="R01 scene plan review",
            status="open",
            assignee="agent-luci-01",
            label=SimulationLabel.SYNTHETIC,
        ),
        TaskRecord(
            id=str(uuid4()),
            title="Synthetic telemetry validation",
            status="in_progress",
            assignee="agent-legion-01",
            label=SimulationLabel.SYNTHETIC,
        ),
        TaskRecord(
            id=str(uuid4()),
            title="Blueprint actor class inventory",
            status="open",
            label=SimulationLabel.SYNTHETIC,
        ),
    ]
    for t in tasks:
        registry.create(t)
    return tasks


def bootstrap_events(store: EventStore, agents: list[AgentRecord]) -> list[TwinEvent]:
    events: list[TwinEvent] = []
    for a in agents:
        ev = TwinEvent(
            kind=EventKind.AGENT_SPAWN,
            source=a.id,
            label=SimulationLabel.SYNTHETIC,
            payload={"name": a.name, "role": a.role},
            scene_node=a.workstation,
        )
        store.append(ev)
        events.append(ev)

    hb = TwinEvent(
        kind=EventKind.SCENE_HEARTBEAT,
        source="twin-service",
        label=SimulationLabel.SYNTHETIC,
        payload={"nodes": SCENE_NODES, "mode": "R01-synthetic"},
        scene_node="executive-command-room",
    )
    store.append(hb)
    events.append(hb)
    return events


def sample_telemetry() -> list[TelemetrySample]:
    return [
        TelemetrySample(
            node_id="pretoria",
            metric="modelled_load_pct",
            value=42.0,
            unit="%",
            label=SimulationLabel.SYNTHETIC,
        ),
        TelemetrySample(
            node_id="johannesburg",
            metric="modelled_load_pct",
            value=58.0,
            unit="%",
            label=SimulationLabel.SYNTHETIC,
        ),
        TelemetrySample(
            node_id="cape-town",
            metric="modelled_load_pct",
            value=31.0,
            unit="%",
            label=SimulationLabel.SYNTHETIC,
        ),
    ]
