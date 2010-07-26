from unittest import TestCase

from pylinq import PyLINQ

data = [
{"name": "item1", "class": "classA", "size": 8},
{"name": "item2", "class": "classA", "size": 10},
{"name": "item3", "class": "classB", "size": 6},
]

class PyLINQTest(TestCase):

    def test1(self):
        """test 01: where/select test"""
        pq = PyLINQ(data)
        self.assertEqual(
            pq.where(lambda it: it["class"] == "classA")
            .select(lambda it: {"name": it["name"], "size": it["size"]}).items(),
            [{"name": "item1", "size": 8},
             {"name": "item2", "size": 10}])

    def test2(self):
        """test 02: order_by test"""
        pq = PyLINQ(data)
        self.assertEqual(
            pq.where(lambda it: it["size"] < 10)
            .order_by(lambda it: it["size"])
            .select(lambda it: (it["name"], it["size"])).items(),
            [("item3", 6), ("item1", 8)])

    def test3(self):
        """test 03: count test with generator"""
        pq = PyLINQ(iter(data))
        self.assertEqual(
            pq.where(lambda it: it["size"] < 10)
            .count(), 2)
        self.assertEqual(
            pq.where(lambda it: it["class"] == "classB")
            .count(), 1)

    def test4(self):
        """test 04: distinct test"""
        pq = PyLINQ(data)
        self.assertEqual(
            pq.distinct(lambda x: x["class"]).items(),
            ["classA", "classB"])

    def test5(self):
        """test 05: any test"""
        l = [1,3,5,7,6]
        pq = PyLINQ(iter(l))
        self.assertEqual(pq.any(lambda x: x % 2 == 0), True)
        self.assertEqual(pq.any(lambda x: x == 0), False)

    def test6(self):
        """test 06: all test"""
        l = [1,3,5,7]
        pq = PyLINQ(iter(l))
        self.assertEqual(pq.all(lambda x: x % 2 != 0), True)
        self.assertEqual(pq.all(lambda x: x < 6), False)

    def test7(self):
        """test 07: reverse test"""
        l = [1,3,5,7]
        pq = PyLINQ(iter(l))
        self.assertEqual(pq.reverse().items(), list(reversed(l)))

    def test8(self):
        """test 08: first & last test"""
        gen = (x for x in "hello")
        pq = PyLINQ(iter(gen))
        self.assertEqual(pq.first(), "h")
        self.assertEqual(pq.last(), "o")
        l = range(10)
        pq = PyLINQ(l)
        self.assertEqual(pq.last(lambda x: x < 4), 3)
        self.assertEqual(pq.first(lambda x: x > 7), 8)

    def test9(self):
        """test 09: element_at test"""
        l = [100, 200, 300]
        pq = PyLINQ(iter(l))
        self.assertEqual(pq.element_at(0), 100)
        self.assertEqual(pq.element_at(1), 200)
        self.assertEqual(pq.element_at(2), 300)
        self.assertRaises(IndexError, pq.element_at, 50)
        self.assertRaises(IndexError, pq.element_at, -2)

    def test10(self):
        """test 10: concat test"""
        l1 = [5, 8]
        l2 = [10, 12]
        pq = PyLINQ(iter(l1))
        self.assertEqual(pq.concat(l2).items(), l1 + l2)

    def test11(self):
        """test 11: default_if_empty test"""
        l = [1,2]
        pq = PyLINQ(iter(l))
        self.assertEqual(pq.default_if_empty().items(), [1, 2])
        pq = PyLINQ([])
        self.assertEqual(pq.default_if_empty(), [])
        self.assertEqual(pq.default_if_empty([3]), [3])

    def test12(self):
        """test 12: element_at_or_default test"""
        l = [100, 200, 300]
        pq = PyLINQ(iter(l))
        self.assertEqual(pq.element_at_or_default(0), 100)
        self.assertEqual(pq.element_at_or_default(1), 200)
        self.assertEqual(pq.element_at_or_default(2), 300)
        self.assertEqual(pq.element_at_or_default(50, default=0), 0)

    def test13(self):
        """test 13: first_or_default test"""
        l = [100, 200, 300]
        self.assertEqual(PyLINQ(l).first_or_default(default=0), 100)
        self.assertEqual(PyLINQ([]).first_or_default(default=0), 0)

    def test14(self):
        """test 14: first_or_default test"""
        l = [100, 200, 300]
        self.assertEqual(PyLINQ(l).last_or_default(default=0), 300)
        self.assertEqual(PyLINQ([]).last_or_default(default=0), 0)

    def test15(self):
        """test 15: aggregate test"""
        l = ["h", "e", "l", "l", "o"]
        self.assertEqual(PyLINQ(l).aggregate(lambda x,y: x + y), "hello")

        l = [1, 2, 3]
        self.assertEqual(PyLINQ(l).aggregate(lambda x,y:x*y), 6)

    def test16(self):
        """test 16: sum test"""
        l = [1, 2, 3, 4, 5]
        self.assertEqual(PyLINQ(iter(l)).sum(), 15)
        self.assertEqual(PyLINQ(iter(l)).sum(lambda x: x*2), 30)

    def test17(self):
        """test 17: average test"""
        l = [1.0, 2.0, 3.0, 4.0]
        self.assertEqual(PyLINQ(iter(l)).average(), 2.5)
        self.assertEqual(PyLINQ(iter(l)).average(lambda x: x-1), 1.5)

    def test18(self):
        """test 18: max test"""
        l = [
            {"name": "andres", "age" : 27},
            {"name": "martin", "age" : 35},
            {"name": "jose", "age" : 20}
        ]
        self.assertEqual(PyLINQ(l).max()["name"], "martin")
        self.assertEqual(PyLINQ(["a", "d", "z"]).max(), "z")

    def test19(self):
        """test 19: min test"""
        l = [
            {"name": "andres", "age" : 27},
            {"name": "martin", "age" : 35},
            {"name": "jose", "age" : 20}
        ]
        self.assertEqual(PyLINQ(l).min()["name"], "jose")
        self.assertEqual(PyLINQ(["a", "d", "z"]).min(), "a")

