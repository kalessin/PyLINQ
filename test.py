from unittest import TestCase

from pylinq import PyLINQ

data = [
{"name": "item1", "class": "classA", "size": 8},
{"name": "item2", "class": "classA", "size": 10},
{"name": "item3", "class": "classB", "size": 6},
]

class PyLINQTest(TestCase):
    def test1(self):
        """where/select test"""
        pq = PyLINQ(data)
        self.assertEqual(
            pq.where(lambda it: it["class"] == "classA")
            .select(lambda it: {"name": it["name"], "size": it["size"]}).items(),
            [{"name": "item1", "size": 8},
             {"name": "item2", "size": 10}])
    def test2(self):
        """order_by test"""
        pq = PyLINQ(data)
        self.assertEqual(
            pq.where(lambda it: it["size"] < 10)
            .order_by(lambda it: it["size"])
            .select(lambda it: (it["name"], it["size"])).items(),
            [("item3", 6), ("item1", 8)])

    def test3(self):
        """count test with generator"""
        pq = PyLINQ(iter(data))
        self.assertEqual(
            pq.where(lambda it: it["size"] < 10)
            .count(), 2)
        self.assertEqual(
            pq.where(lambda it: it["class"] == "classB")
            .count(), 1)

