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
        if not self._exitems:
            self._exitems = list(self.items)
            self.items = iter(self._exitems)
        if not clause:
            return len(self._exitems)
        else:
            return len([e for e in self._exitems if clause(e)])

