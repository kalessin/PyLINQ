"""
PyLINQ 

LINQ to python, based on http://jslinq.codeplex.com/.

"""

class PyLINQException(Exception):
    pass

class PyLINQ(object):
    def __init__(self, items):
        self.items = items
        self._exitems = None

    def Items(self):
        return self.items

    def toList(self):
        if not self._exitems:
            self._exitems = self.items
            self.items = iter(self._exitems)
        return list(self.items)

    def Where(self, clause):
        it = iter(self.items)
        if not callable(clause):
            raise PyLINQException("caluse argument must be callable.")
        return PyLINQ((e for e in it if clause(e)))

    def Select(self, clause):
        it = iter(self.items)
        if not callable(clause):
            raise PyLINQException("caluse argument must be callable.")
        return PyLINQ((e for e in it if clause(e)))

    def OrderBy(self, clause, cmp=None, order='asc'):
        it = iter(self.items)
        if not callable(clause):
            raise PyLINQException("caluse argument must be callable.")
        ls = sorted(it, key=clause, cmp=cmp, reverse=(order != 'asc'))
        return PyLINQ(ls)

    def Count(self, clause=None):
        if not clause:
            return len(self.toList())
        else:
            return len([e for e in self.toList() if clause(e)])

    def Distinct(self, clause):
        it = iter(self.items)
        if not callable(clause):
            raise PyLINQException("caluse argument must be callable.")
        try:
            diselems = set(clause(x) for x in it)
            return PyLINQ(diselems)
        except TypeError, e:
            raise PyLINQException("clause should return a hashable item")

    def Any(self, clause):
        if not callable(clause):
            raise PyLINQException("caluse argument must be callable.")
        for x in self.toList():
            if clause(x):
                return x
        return

    def All(self, clause):
        for x in self.toList():
            if not clause(x):
                return False
        return True

    def Reverse(self):
        return PyLINQ(self.toList()[::-1])

    def _get_elem(self, clause, pos):
        if clause:
            return self.Where(clause).First()
        elist = self.toList()
        return elist[pos] if elist else None

    def First(self, clause=None):
        return self._get_elem(0)

    def Last(self, clause=None):
        return self._get_elem(-1)

    def ElementAt(self, index):
        elist = self.toList()
        return elist[index]
    
    def Concat(self, items):
        elist = self.toList()
        return PyLINQ(elist + items)

    def DefaultIfEmpty(self, default=None):
        default = default or []
        if not self.toList():
            return default
        return self

    def ElementAtOrDefault(self, index, defaultitem=None):
        try:
            elist = self.toList()
            item = elist[index]
            return item
        except IndexError:
            return defaultitem

    def FirstOrDefault(self, defaultitem=None)
        return self.First() or defaultitem

    def LastOrDefault(sefl, defaultitem=None)
        return self.Last() or defaultitem


