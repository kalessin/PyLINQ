from unittest import TestCase

from pylinq import PyLINQ

data = [
{"name": "item1", "class": "classA", "size": 8},
{"name": "item2", "class": "classA", "size": 10},
{"name": "item3", "class": "classB", "size": 6},
]

class PyLINQTest(TestCase):
    def test1(self):
        """Where/Select test"""
        pq = PyLINQ(data)
        self.assertEqual(
            pq.Where(lambda it: it["class"] == "classA")
            .Select(lambda it: {"name": it["name"], "size": it["size"]}).items(),
            [{"name": "item1", "size": 8},
             {"name": "item2", "size": 10}])
    def test2(self):
        """OrderBy test"""
        pq = PyLINQ(data)
        self.assertEqual(
            pq.Where(lambda it: it["size"] < 10)
            .OrderBy(lambda it: it["size"])
            .Select(lambda it: (it["name"], it["size"])).items(),
            [("item3", 6), ("item1", 8)])

    def test3(self):
        """Count test with generator"""
        pq = PyLINQ(iter(data))
        self.assertEqual(
            pq.Where(lambda it: it["size"] < 10)
            .Count(), 2)
        self.assertEqual(
            pq.Where(lambda it: it["class"] == "classB")
            .Count(), 1)

