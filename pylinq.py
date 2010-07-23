"""
PyLINQ 

LINQ to python, based on http://jslinq.codeplex.com/.

"""

class PyLINQException(Exception):
    pass

class PyLINQ(object):
    def __init__(self, items):
        self.items = items

    def Items(self):
        return self.items

    def toList(self):
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


