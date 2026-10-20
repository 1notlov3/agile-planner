import unittest
from datetime import date

from agile_planner.planner import Planner


class PlannerTest(unittest.TestCase):
    def setUp(self):
        self.p = Planner()
        self.p.add_task("Сверстать доску", 3, "high")
        self.p.add_task("Экспорт в CSV", 2, "low")
        self.p.add_task("Напоминания", 5)

    def test_backlog_sorted_by_priority(self):
        titles = [t.title for t in self.p.backlog()]
        self.assertEqual(titles, ["Сверстать доску", "Напоминания",
                                  "Экспорт в CSV"])

    def test_sprint_flow(self):
        self.p.start_sprint("Первый выпуск", 7, date(2026, 11, 2))
        self.p.plan(1)
        self.p.plan(3)
        self.p.move(1, "done")
        self.assertEqual(len(self.p.board()["done"]), 1)
        self.p.close_sprint()
        self.assertEqual(self.p.velocity(), 3)
        self.assertEqual(self.p.get_task(3).status, "backlog")

    def test_only_one_active_sprint(self):
        self.p.start_sprint("A")
        with self.assertRaises(RuntimeError):
            self.p.start_sprint("B")

    def test_bad_priority(self):
        with self.assertRaises(ValueError):
            self.p.add_task("x", 1, "urgent")


if __name__ == "__main__":
    unittest.main()
