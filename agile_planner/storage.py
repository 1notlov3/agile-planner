"""Хранение данных планировщика в файле JSON."""

import json
from pathlib import Path

from .models import Sprint, Task

DEFAULT_FILE = Path.home() / ".agile_planner.json"


def load(path=DEFAULT_FILE):
    """Читает задачи и спринты из файла.

    Если файла нет, возвращает пустые списки.
    """
    path = Path(path)
    if not path.exists():
        return [], []
    data = json.loads(path.read_text(encoding="utf-8"))
    tasks = [Task(**t) for t in data.get("tasks", [])]
    sprints = [Sprint(**s) for s in data.get("sprints", [])]
    return tasks, sprints


def save(tasks, sprints, path=DEFAULT_FILE):
    """Записывает задачи и спринты в файл."""
    data = {
        "tasks": [t.to_dict() for t in tasks],
        "sprints": [s.to_dict() for s in sprints],
    }
    Path(path).write_text(json.dumps(data, ensure_ascii=False, indent=2),
                          encoding="utf-8")
