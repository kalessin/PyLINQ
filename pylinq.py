"""
PyLINQ 

LINQ to python, based on http://jslinq.codeplex.com/.

"""

class PyLINQException(Exception):
    pass

def _check(clause):
    if not callable(clause):
        raise PyLINQException("clause argument must be callable.")

class PyLINQ(object):
    def __init__(self, items):
        self.__items = items

    def iteritems(self):
        return iter(self.__items)

    def items(self):
        return list(self.__items)

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

