"""
Sealie Digital Twin R01 — HTTP + WebSocket API
Read-only by default. Synthetic data only. No external actions.
"""

from __future__ import annotations

import asyncio
from typing import Optional

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from sealie_twin.models.events import TwinEvent, AgentRecord, TaskRecord, SimulationLabel
from sealie_twin.services.registry import AgentRegistry, TaskRegistry
from sealie_twin.services.event_store import EventStore
from sealie_twin.fixtures.synthetic import (
    bootstrap_agents,
    bootstrap_tasks,
    bootstrap_events,
    sample_telemetry,
    SCENE_NODES,
)

app = FastAPI(
    title="Sealie Digital Twin R01",
    description="Shared digital-twin service. SYNTHETIC data only. R0 spending. No external actions.",
    version="0.1.0-r01",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

# In-process state (R01 — not durable, not multi-instance)
agents = AgentRegistry()
tasks = TaskRegistry()
events = EventStore()

# Bootstrap synthetic world once
_agents = bootstrap_agents(agents)
_tasks = bootstrap_tasks(tasks)
bootstrap_events(events, _agents)


@app.get("/health")
def health():
    return {
        "status": "ok",
        "revision": "R01",
        "data_policy": "SYNTHETIC_ONLY",
        "spending": "R0",
        "external_actions": "NONE",
        "execution_authority": "NOT_GRANTED",
    }


@app.get("/scene/nodes")
def scene_nodes():
    return {
        "label": SimulationLabel.SYNTHETIC.value,
        "nodes": SCENE_NODES,
        "note": "Scene plan only. Unreal compilation not verified in R01.",
    }


@app.get("/agents")
def list_agents():
    return [a.model_dump(mode="json") for a in agents.list()]


@app.get("/tasks")
def list_tasks():
    return [t.model_dump(mode="json") for t in tasks.list()]


@app.get("/events")
def list_events(
    kind: Optional[str] = Query(None),
    source: Optional[str] = Query(None),
    limit: int = Query(50, ge=1, le=500),
):
    return [e.model_dump(mode="json") for e in events.list(kind=kind, source=source, limit=limit)]


@app.get("/events/audit")
def audit_trail(limit: int = Query(100, ge=1, le=500)):
    return events.audit_trail(limit=limit)


@app.get("/telemetry/synthetic")
def telemetry_synthetic():
    return [s.model_dump(mode="json") for s in sample_telemetry()]


@app.post("/events")
def post_event(event: TwinEvent):
    """
    Accept a new event. Still constrained to SYNTHETIC/MODELLED labels.
    Does not trigger any external action.
    """
    stored = events.append(event)
    return stored.model_dump(mode="json")


@app.websocket("/ws/events")
async def ws_events(websocket: WebSocket):
    """
    Push new events to connected clients.
    Read-only stream of the in-memory store.
    """
    await websocket.accept()
    queue: asyncio.Queue = asyncio.Queue()

    def on_event(ev: TwinEvent) -> None:
        try:
            queue.put_nowait(ev)
        except Exception:
            pass

    events.subscribe(on_event)

    # Send recent history first
    for ev in events.list(limit=20):
        await websocket.send_json(ev.model_dump(mode="json"))

    try:
        while True:
            # Also accept client pings / ignore messages (no command execution)
            try:
                incoming = await asyncio.wait_for(websocket.receive_text(), timeout=0.5)
                if incoming == "ping":
                    await websocket.send_json({"type": "pong"})
            except asyncio.TimeoutError:
                pass

            try:
                ev = queue.get_nowait()
                await websocket.send_json(ev.model_dump(mode="json"))
            except asyncio.QueueEmpty:
                await asyncio.sleep(0.1)
    except WebSocketDisconnect:
        pass


@app.get("/")
def root():
    return JSONResponse(
        {
            "service": "Sealie Digital Twin R01",
            "docs": "/docs",
            "health": "/health",
            "policy": {
                "spending": "R0",
                "data": "SYNTHETIC_ONLY",
                "external_actions": "NONE",
                "execution_authority": "NOT_GRANTED",
            },
        }
    )
