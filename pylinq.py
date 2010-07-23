"""
PyLINQ 

LINQ to python, based on http://jslinq.codeplex.com/.

"""

class PyLINQException(Exception):
    pass

class PyLINQ(object):
    def __init__(self, items):
        assert (items is not None and isinstance(items[0], dict))
        self.items

    def Where(self, clause):
        it = iter(self.items)
        if not callable(clause):
            raise PyLINQException("caluse argument must be callable.")
        return (e for e in it if clause(e))
