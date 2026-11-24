"""Классы данных планировщика."""

from dataclasses import dataclass, field, asdict
from datetime import date

STATUSES = ("backlog", "todo", "in_progress", "done")
STATUS_NAMES = {
    "backlog": "Бэклог",
    "todo": "К выполнению",
    "in_progress": "В работе",
    "done": "Готово",
}
PRIORITIES = ("low", "medium", "high")


@dataclass
class Task:
    """Задача (пользовательская история) личного бэклога."""

    id: int
    title: str
    points: int = 1
    priority: str = "medium"
    status: str = "backlog"
    sprint_id: int | None = None
    created: str = field(default_factory=lambda: date.today().isoformat())
    done_date: str | None = None

    def to_dict(self):
        return asdict(self)


@dataclass
class Sprint:
    """Спринт: ограниченный по времени отрезок работы."""

    id: int
    goal: str
    start: str
    end: str
    closed: bool = False

    def to_dict(self):
        return asdict(self)
