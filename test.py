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

    def test4(self):
        """distinct test"""
        pq = PyLINQ(data)
        self.assertEqual(
            pq.distinct(lambda x: x["class"]).items(),
            ["classA", "classB"])

    def test5(self):
        """any test"""
        l = [1,3,5,7,6]
        pq = PyLINQ(iter(l))
        self.assertEqual(pq.any(lambda x: x % 2 == 0), True)
        self.assertEqual(pq.any(lambda x: x == 0), False)

    def test6(self):
        """all test"""
        l = [1,3,5,7]
        pq = PyLINQ(iter(l))
        self.assertEqual(pq.all(lambda x: x % 2 != 0), True)
        self.assertEqual(pq.all(lambda x: x < 6), False)

    def test7(self):
        """reverse test"""
        l = [1,3,5,7]
        pq = PyLINQ(iter(l))
        self.assertEqual(pq.reverse().items(), list(reversed(l)))

    def test8(self):
        """first & last test"""
        gen = (x for x in "hello")
        pq = PyLINQ(iter(gen))
        self.assertEqual(pq.first(), "h")
        self.assertEqual(pq.last(), "o")
        l = range(10)
        pq = PyLINQ(l)
        self.assertEqual(pq.last(lambda x: x < 4), 3)
        self.assertEqual(pq.first(lambda x: x > 7), 8)

    def test9(self):
        """element_at test"""
        l = [100, 200, 300]
        pq = PyLINQ(iter(l))
        self.assertEqual(pq.element_at(0), 100)
        self.assertEqual(pq.element_at(1), 200)
        self.assertEqual(pq.element_at(2), 300)
        self.assertRaises(IndexError, pq.element_at, 50)

    def test10(self):
        """concat test"""
        l1 = [5, 8]
        l2 = [10, 12]
        pq = PyLINQ(iter(l1))
        self.assertEqual(pq.concat(l2).items(), l1 + l2)

    def test11(self):
        """default_if_empty test"""
        l = [1,2]
        pq = PyLINQ(iter(l))
        self.assertEqual(pq.default_if_empty().items(), [1, 2])
        pq = PyLINQ([])
        self.assertEqual(pq.default_if_empty(), [])

    def test12(self):
        """element_at_or_default test"""
        l = [100, 200, 300]
        pq = PyLINQ(iter(l))
        self.assertEqual(pq.element_at_or_default(0), 100)
        self.assertEqual(pq.element_at_or_default(1), 200)
        self.assertEqual(pq.element_at_or_default(2), 300)
        self.assertEqual(pq.element_at_or_default(50, default=0), 0)

    def test13(self):
        """first_or_default test"""
        l = [100, 200, 300]
        self.assertEqual(PyLINQ(l).first_or_default(default=0), 100)
        self.assertEqual(PyLINQ([]).first_or_default(default=0), 0)

    def test14(self):
        """first_or_default test"""
        l = [100, 200, 300]
        self.assertEqual(PyLINQ(l).last_or_default(default=0), 300)
        self.assertEqual(PyLINQ([]).last_or_default(default=0), 0)
