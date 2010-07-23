"""
PyLINQ 

LINQ to python, based on http://jslinq.codeplex.com/.

"""
from itertools import tee

class PyLINQException(Exception):
    pass

def _check(clause):
    if not callable(clause):
        raise PyLINQException("clause argument must be callable.")


class PyLINQ(object):
    def __init__(self, items):
        self.__items = iter(items)
        self._exitems = None

    def iteritems(self):
        self.__items, ret = tee(self.__items)
        return ret

    def items(self):
        self.__items, ret = tee(self.__items)
        return list(ret)

    def Where(self, clause):
        _check(clause)
        return PyLINQ((e for e in self.iteritems() if clause(e)))

    def Select(self, clause):
        _check(clause)
        return PyLINQ((clause(e) for e in self.iteritems()))
    
    def OrderBy(self, clause, cmp=None, order='asc'):
        _check(clause)
        ls = sorted(self.iteritems(), key=clause, cmp=cmp, reverse=(order != 'asc'))
        return PyLINQ(ls)

    def Count(self, clause=None):
        if not clause:
            return len(self.items())
        else:
            return len([e for e in self.items() if clause(e)])

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

    def FirstOrDefault(self, defaultitem=None):
        return self.First() or defaultitem

    def LastOrDefault(sefl, defaultitem=None):
        return self.Last() or defaultitem


