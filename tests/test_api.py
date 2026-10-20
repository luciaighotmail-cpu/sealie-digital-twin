"""API tests — synthetic bootstrap and read-only behaviour."""

import pytest
from fastapi.testclient import TestClient

from sealie_twin.api.main import app

client = TestClient(app)


def test_health_policy():
    r = client.get("/health")
    assert r.status_code == 200
    body = r.json()
    assert body["data_policy"] == "SYNTHETIC_ONLY"
    assert body["spending"] == "R0"
    assert body["external_actions"] == "NONE"
    assert body["execution_authority"] == "NOT_GRANTED"


def test_agents_bootstrapped():
    r = client.get("/agents")
    assert r.status_code == 200
    agents = r.json()
    assert len(agents) >= 3
    assert all(a["label"] == "SYNTHETIC" for a in agents)


def test_tasks_bootstrapped():
    r = client.get("/tasks")
    assert r.status_code == 200
    tasks = r.json()
    assert len(tasks) >= 1
    assert all(t["label"] == "SYNTHETIC" for t in tasks)


def test_events_present():
    r = client.get("/events")
    assert r.status_code == 200
    events = r.json()
    assert len(events) >= 1
    assert all(e["label"] in ("SYNTHETIC", "MODELLED") for e in events)


def test_scene_nodes():
    r = client.get("/scene/nodes")
    assert r.status_code == 200
    body = r.json()
    assert "executive-command-room" in body["nodes"]
    assert body["label"] == "SYNTHETIC"


def test_telemetry_synthetic():
    r = client.get("/telemetry/synthetic")
    assert r.status_code == 200
    samples = r.json()
    assert all(s["label"] == "SYNTHETIC" for s in samples)


def test_post_event_synthetic_ok():
    r = client.post(
        "/events",
        json={
            "kind": "authority.note",
            "source": "test-runner",
            "label": "SYNTHETIC",
            "payload": {"msg": "r01 test"},
        },
    )
    assert r.status_code == 200
    assert r.json()["label"] == "SYNTHETIC"


def test_post_event_measured_rejected():
    r = client.post(
        "/events",
        json={
            "kind": "telemetry.sample",
            "source": "test-runner",
            "label": "MEASURED",
            "payload": {},
        },
    )
    assert r.status_code == 422  # validation error
