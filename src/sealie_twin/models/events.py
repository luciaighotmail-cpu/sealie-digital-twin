"""
Typed event records for the Digital Twin.
All events are synthetic in R01. Simulation labels are mandatory.
"""

from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum
from typing import Any, Optional
from uuid import uuid4

from pydantic import BaseModel, Field, field_validator


class EventKind(str, Enum):
    AGENT_SPAWN = "agent.spawn"
    AGENT_STATUS = "agent.status"
    TASK_CREATED = "task.created"
    TASK_UPDATED = "task.updated"
    TELEMETRY = "telemetry.sample"
    EVIDENCE_ATTACHED = "evidence.attached"
    SCENE_HEARTBEAT = "scene.heartbeat"
    AUTHORITY_NOTE = "authority.note"


class SimulationLabel(str, Enum):
    """Mandatory visibility of data provenance."""
    SYNTHETIC = "SYNTHETIC"
    MODELLED = "MODELLED"
    MEASURED = "MEASURED"      # not used in R01 data
    VERIFIED = "VERIFIED"      # not used in R01 data


class TwinEvent(BaseModel):
    """Canonical event record. Fail-closed validation."""

    id: str = Field(default_factory=lambda: str(uuid4()))
    kind: EventKind
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    source: str = Field(..., min_length=1, description="Agent or system id that emitted the event")
    label: SimulationLabel = SimulationLabel.SYNTHETIC
    payload: dict[str, Any] = Field(default_factory=dict)
    evidence_ref: Optional[str] = None
    scene_node: Optional[str] = None  # e.g. "command-room", "machine-floor"

    @field_validator("label")
    @classmethod
    def r01_only_synthetic_or_modelled(cls, v: SimulationLabel) -> SimulationLabel:
        # R01 control: INITIAL DATA = Synthetic only
        if v not in (SimulationLabel.SYNTHETIC, SimulationLabel.MODELLED):
            raise ValueError(
                f"R01 forbids label={v}. Only SYNTHETIC or MODELLED allowed until live data is authorised."
            )
        return v

    def to_audit_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "kind": self.kind.value,
            "timestamp": self.timestamp.isoformat(),
            "source": self.source,
            "label": self.label.value,
            "payload": self.payload,
            "evidence_ref": self.evidence_ref,
            "scene_node": self.scene_node,
        }


class AgentRecord(BaseModel):
    id: str
    name: str
    role: str
    status: str = "idle"  # idle | working | blocked | offline
    workstation: Optional[str] = None
    label: SimulationLabel = SimulationLabel.SYNTHETIC
    last_seen: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    meta: dict[str, Any] = Field(default_factory=dict)


class TaskRecord(BaseModel):
    id: str
    title: str
    status: str = "open"  # open | in_progress | blocked | done
    assignee: Optional[str] = None
    label: SimulationLabel = SimulationLabel.SYNTHETIC
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    evidence_refs: list[str] = Field(default_factory=list)


class TelemetrySample(BaseModel):
    node_id: str
    metric: str
    value: float
    unit: str
    label: SimulationLabel = SimulationLabel.SYNTHETIC
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
