"""Операции с бэклогом, спринтами и доской."""

from datetime import date, timedelta

from .models import PRIORITIES, STATUSES, Sprint, Task

PRIORITY_ORDER = {p: i for i, p in enumerate(reversed(PRIORITIES))}


class Planner:
    def __init__(self, tasks=None, sprints=None):
        self.tasks = tasks or []
        self.sprints = sprints or []

    # --- бэклог ---
    def add_task(self, title, points=1, priority="medium"):
        if priority not in PRIORITIES:
            raise ValueError(f"неизвестный приоритет: {priority}")
        if points <= 0:
            raise ValueError("оценка должна быть положительной")
        new_id = max((t.id for t in self.tasks), default=0) + 1
        task = Task(new_id, title, points, priority)
        self.tasks.append(task)
        return task

    def get_task(self, task_id):
        for task in self.tasks:
            if task.id == task_id:
                return task
        raise KeyError(f"задача {task_id} не найдена")

    def backlog(self):
        """Задачи без спринта, отсортированные по приоритету."""
        items = [t for t in self.tasks if t.sprint_id is None
                 and t.status != "done"]
        return sorted(items, key=lambda t: (PRIORITY_ORDER[t.priority], t.id))

    # --- спринты ---
    def active_sprint(self):
        for sprint in self.sprints:
            if not sprint.closed:
                return sprint
        return None

    def start_sprint(self, goal, days=14, start=None):
        if self.active_sprint():
            raise RuntimeError("предыдущий спринт ещё не закрыт")
        start = start or date.today()
        sprint = Sprint(len(self.sprints) + 1, goal, start.isoformat(),
                        (start + timedelta(days=days)).isoformat())
        self.sprints.append(sprint)
        return sprint

    def plan(self, task_id):
        """Переносит задачу из бэклога в активный спринт."""
        sprint = self.active_sprint()
        if sprint is None:
            raise RuntimeError("нет активного спринта")
        task = self.get_task(task_id)
        task.sprint_id = sprint.id
        task.status = "todo"
        return task

    def close_sprint(self):
        """Закрывает спринт, незавершённые задачи возвращаются в бэклог."""
        sprint = self.active_sprint()
        if sprint is None:
            raise RuntimeError("нет активного спринта")
        for task in self.tasks:
            if task.sprint_id == sprint.id and task.status != "done":
                task.sprint_id = None
                task.status = "backlog"
        sprint.closed = True
        return sprint
