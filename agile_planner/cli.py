"""Интерфейс командной строки."""

import argparse

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
