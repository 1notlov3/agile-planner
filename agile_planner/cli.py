"""Интерфейс командной строки."""

import argparse

from . import storage
from .models import STATUS_NAMES
from .planner import Planner


def build_parser():
    p = argparse.ArgumentParser(prog="planner",
                                description="Личный Agile-планировщик")
    sub = p.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("add", help="добавить задачу в бэклог")
    a.add_argument("title")
    a.add_argument("-p", "--points", type=int, default=1)
    a.add_argument("--priority", default="medium",
                   choices=["low", "medium", "high"])
    sub.add_parser("backlog", help="показать бэклог")
    s = sub.add_parser("sprint", help="начать спринт")
    s.add_argument("goal")
    s.add_argument("-d", "--days", type=int, default=14)
    pl = sub.add_parser("plan", help="взять задачу в спринт")
    pl.add_argument("task_id", type=int)
    m = sub.add_parser("move", help="сменить статус задачи")
    m.add_argument("task_id", type=int)
    m.add_argument("status", choices=["todo", "in_progress", "done"])
    sub.add_parser("board", help="показать доску спринта")
    sub.add_parser("close", help="закрыть спринт")
    return p


def main(argv=None):
    args = build_parser().parse_args(argv)
    tasks, sprints = storage.load()
    planner = Planner(tasks, sprints)
    try:
        if args.cmd == "add":
            t = planner.add_task(args.title, args.points, args.priority)
            print(f"Добавлена задача #{t.id}: {t.title}")
        elif args.cmd == "backlog":
            for t in planner.backlog():
                print(f"#{t.id:<3} [{t.priority:<6}] {t.points:>2} SP"
                      f"  {t.title}")
        elif args.cmd == "sprint":
            s = planner.start_sprint(args.goal, args.days)
            print(f"Спринт {s.id}: {s.goal} ({s.start} - {s.end})")
        elif args.cmd == "plan":
            t = planner.plan(args.task_id)
            print(f"Задача #{t.id} взята в спринт")
        elif args.cmd == "move":
            t = planner.move(args.task_id, args.status)
            print(f"#{t.id} -> {STATUS_NAMES[t.status]}")
        elif args.cmd == "board":
            for status, items in planner.board().items():
                print(f"== {STATUS_NAMES[status]} ({len(items)})")
                for t in items:
                    print(f"   #{t.id} {t.title}")
        elif args.cmd == "close":
            s = planner.close_sprint()
            print(f"Спринт {s.id} закрыт, скорость {planner.velocity()} SP")
    except (KeyError, ValueError, RuntimeError) as err:
        print("Ошибка:", err)
        return 1
    storage.save(planner.tasks, planner.sprints)
    return 0
