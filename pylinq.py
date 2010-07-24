"""
PyLINQ

LINQ to python, based on http://jslinq.codeplex.com/.

Copyright (C) 2010  Insophia

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
"""
from itertools import tee, chain, imap, ifilter

def _check(clause):
    if not callable(clause):
        raise TypeError("clause argument must be callable.")

class PyLINQ(object):
    def __init__(self, items):
        self.__items = iter(items)

    def iteritems(self):
        """returns collection as generator"""
        self.__items, ret = tee(self.__items)
        return ret

    def items(self):
        """returns collection as list"""
        self.__items, ret = tee(self.__items)
        return list(ret)

    def where(self, clause):
        """return all items in collection for which clause returns true"""
        _check(clause)
        return PyLINQ(ifilter(clause, self.iteritems()))

    def select(self, clause):
        """returns new collection resultant of application of clause
        over each item in input collection"""
        _check(clause)
        return PyLINQ(imap(clause, self.iteritems()))

    def order_by(self, clause, cmp=None, order='asc'):
        """returns new collection ordered by the result of clause over
        each item in input collection"""
        _check(clause)
        ls = sorted(self.iteritems(), key=clause, cmp=cmp, reverse=(order != 'asc'))
        return PyLINQ(ls)

    def count(self, clause=None):
        """returns the count of items in collection"""
        if not clause:
            return len(self.items())
        else:
            return len(filter(clause, self.iteritems()))

    def distinct(self, clause):
        """returns new collection mapped from input collection
        by clause, but avoiding duplicates"""
        _check(clause)
        seen = set()
        def _isnew(item):
            try:
                if not item in seen:
                    seen.add(item)
                    return True
                return False
            except:
                raise TypeError("clause should return a hashable item")
        return PyLINQ(ifilter(_isnew, imap(clause, self.iteritems())))

    def any(self, clause):
        _check(clause)
        for x in self.iteritems():
            if clause(x):
                return x
        return

    def all(self, clause):
        _check(clause)
        for x in self.iteritems():
            if not clause(x):
                return False
        return True

    def reverse(self):
        return PyLINQ(self.items()[::-1])

    def _get_elem(self, clause, pos):
        if clause:
            return self.where(clause).first()
        elist = self.items()
        return elist[pos] if elist else None

    def first(self, clause=None):
        return self._get_elem(0)

    def last(self, clause=None):
        return self._get_elem(-1)

    def elementAt(self, index):
        elist = self.items()
        return elist[index]

    def concat(self, items):
        return PyLINQ(chain(self.iteritems(), items))

    def default_if_empty(self, default=None):
        default = default or []
        if not self.items():
            return default
        return self

    def elementat_or_default(self, index, defaultitem=None):
        try:
            elist = self.items()
            item = elist[index]
            return item
        except IndexError:
            return defaultitem

    def first_or_default(self, defaultitem=None):
        return self.first() or defaultitem

    def last_or_default(self, defaultitem=None):
        return self.last() or defaultitem


