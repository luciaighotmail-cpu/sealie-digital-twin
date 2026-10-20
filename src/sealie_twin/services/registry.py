"""
In-memory agent and task registry.
R01: synthetic only, no external writes.
"""

from __future__ import annotations

from typing import Optional

from sealie_twin.models.events import AgentRecord, TaskRecord, SimulationLabel


class AgentRegistry:
    def __init__(self) -> None:
        self._agents: dict[str, AgentRecord] = {}

    def register(self, agent: AgentRecord) -> AgentRecord:
        if agent.label not in (SimulationLabel.SYNTHETIC, SimulationLabel.MODELLED):
            raise ValueError("R01: only SYNTHETIC/MODELLED agents permitted")
        self._agents[agent.id] = agent
        return agent

    def get(self, agent_id: str) -> Optional[AgentRecord]:
        return self._agents.get(agent_id)

    def list(self) -> list[AgentRecord]:
        return list(self._agents.values())

    def update_status(self, agent_id: str, status: str) -> AgentRecord:
        agent = self._agents.get(agent_id)
        if not agent:
            raise KeyError(f"agent not found: {agent_id}")
        agent.status = status
        return agent


class TaskRegistry:
    def __init__(self) -> None:
        self._tasks: dict[str, TaskRecord] = {}

    def create(self, task: TaskRecord) -> TaskRecord:
        if task.label not in (SimulationLabel.SYNTHETIC, SimulationLabel.MODELLED):
            raise ValueError("R01: only SYNTHETIC/MODELLED tasks permitted")
        self._tasks[task.id] = task
        return task

    def get(self, task_id: str) -> Optional[TaskRecord]:
        return self._tasks.get(task_id)

    def list(self) -> list[TaskRecord]:
        return list(self._tasks.values())

    def update_status(self, task_id: str, status: str) -> TaskRecord:
        task = self._tasks.get(task_id)
        if not task:
            raise KeyError(f"task not found: {task_id}")
        task.status = status
        return task
