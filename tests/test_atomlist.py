#------------------------------------------------------------------------------
# Copyright (c) 2013-2017, Nucleic Development Team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file COPYING.txt, distributed with this software.
#------------------------------------------------------------------------------
from __future__ import (division, unicode_literals, print_function,
                        absolute_import)

from sys import version_info
from pickle import dumps, loads
from functools import wraps

import pytest
from atom.api import (Atom, List, Int, ContainerList, Value, atomlist, 
                      atomclist)


class StandardModel(Atom):
    """ A model class for testing atomlist behavior.

    """
    #: A standard list with no type checking.
    untyped = List()

    #: A standard list of integers.
    typed = List(Int())


class ContainerModel(Atom):
    """ A model class for testing atomclist behavior.

    """
    #: A container list with no type checking.
    untyped = ContainerList()

    #: A container list of integers.
    typed = ContainerList(Int())

    #: Change dictionary for the last notification
    change = Value()

    def _changed(self, change):
        self.change = change


class ListTestBase(object):
    """ A base class which provides base list tests.

    """
    #: Set this to one of the models defined above in setUp.
    model = None

    #--------------------------------------------------------------------------
    # Untyped Tests
    #--------------------------------------------------------------------------
    def test_untyped_any_data(self):
        data = [object(), object, type, 12.0, 'wfoo', 9j, 10, {}, [], ()]
        self.model.untyped = data
        assert self.model.untyped == data

    def test_untyped_convert_to_list(self):
        self.model.untyped = list(range(10))
        assert list(self.model.untyped) == list(range(10))

    def test_untyped_iterate(self):
        self.model.untyped = list(range(10))
        data = [i for i in self.model.untyped]
        assert data == list(range(10))

    def test_untyped_copy_on_assign(self):
        data = list(range(10))
        self.model.untyped = data
        assert self.model.untyped == data
        assert self.model.untyped is not data

    def test_untyped_append(self):
        self.model.untyped.append(1)
        assert self.model.untyped == [1]

    def test_untyped_extend(self):
        self.model.untyped.extend(list(range(10)))
        assert self.model.untyped == list(range(10))

    def test_untyped_insert(self):
        self.model.untyped = list(range(10))
        self.model.untyped.insert(0, 19)
        assert self.model.untyped == [19] +list(range(10))

    def test_untyped_remove(self):
        self.model.untyped = list(range(10))
        self.model.untyped.remove(5)
        data = list(range(10))
        data.remove(5)
        assert self.model.untyped == data

    def test_untyped_pop(self):
        self.model.untyped = list(range(10))
        self.model.untyped.pop()
        assert self.model.untyped == list(range(9))
        self.model.untyped.pop(0)
        assert self.model.untyped == list(range(1, 9))

    def test_untyped_index(self):
        self.model.untyped = list(range(10))
        index = self.model.untyped.index(5)
        assert index == 5

    def test_untyped_count(self):
        self.model.untyped = [1] * 10
        count = self.model.untyped.count(1)
        assert count == 10

    def test_untyped_reverse(self):
        self.model.untyped = list(range(10))
        self.model.untyped.reverse()
        assert self.model.untyped == list(reversed(range(10)))

    def test_untyped_sort(self):
        self.model.untyped = [8, 3, 2, 5, 9]
        self.model.untyped.sort()
        assert self.model.untyped == [2, 3, 5, 8, 9]
        self.model.untyped.sort(reverse=True)
        assert self.model.untyped == [9, 8, 5, 3, 2]

    def test_untyped_get_item(self):
        self.model.untyped = list(range(10))
        assert self.model.untyped[3] == 3

    def test_untyped_get_slice(self):
        self.model.untyped = list(range(10))
        assert self.model.untyped[3:8] == list(range(3, 8))

    def test_untyped_get_slice_step(self):
        self.model.untyped = list(range(10))
        assert self.model.untyped[3::2] == list(range(3, 10, 2))

    def test_untyped_set_item(self):
        self.model.untyped = list(range(10))
        self.model.untyped[5] = 42
        assert self.model.untyped[5] == 42

    def test_untyped_set_slice(self):
        self.model.untyped = list(range(5))
        self.model.untyped[3:5] = [42, 42]
        assert self.model.untyped == [0, 1, 2, 42, 42]

    def test_untyped_set_slice_step(self):
        self.model.untyped = list(range(5))
        self.model.untyped[::2] = [42, 42, 42]
        assert self.model.untyped == [42, 1, 42, 3, 42]

    def test_untyped_del_item(self):
        self.model.untyped = list(range(5))
        del self.model.untyped[3]
        assert self.model.untyped == [0, 1, 2, 4]

    def test_untyped_del_slice(self):
        self.model.untyped = list(range(5))
        del self.model.untyped[3:]
        assert self.model.untyped == list(range(3))

    def test_untyped_del_slice_step(self):
        self.model.untyped = list(range(10))
        del self.model.untyped[::2]
        assert self.model.untyped == list(range(1, 10, 2))

    def test_untyped_concat(self):
        self.model.untyped = list(range(10))
        self.model.untyped += list(range(5))
        assert self.model.untyped == list(range(10)) + list(range(5))

    def test_untyped_repeat(self):
        self.model.untyped = list(range(10))
        self.model.untyped *= 3
        assert self.model.untyped == list(range(10)) * 3

    #--------------------------------------------------------------------------
    # Typed Tests
    #--------------------------------------------------------------------------
    def test_typed_convert_to_list(self):
        self.model.typed = list(range(10))
        assert list(self.model.typed) == list(range(10))

    def test_typed_iterate(self):
        self.model.typed = list(range(10))
        data = [i for i in self.model.typed]
        assert data == list(range(10))

    def test_typed_copy_on_assign(self):
        data = list(range(10))
        self.model.typed = data
        assert self.model.typed == data
        assert self.model.typed is not data

    def test_typed_append(self):
        self.model.typed.append(1)
        assert self.model.typed == [1]

    def test_typed_extend(self):
        self.model.typed.extend(list(range(10)))
        assert self.model.typed == list(range(10))

    def test_typed_insert(self):
        self.model.typed = list(range(10))
        self.model.typed.insert(0, 19)
        assert self.model.typed == [19] + list(range(10))

    def test_typed_remove(self):
        self.model.typed = list(range(10))
        self.model.typed.remove(5)
        data = list(range(10))
        data.remove(5)
        assert self.model.typed == data

    def test_typed_pop(self):
        self.model.typed = list(range(10))
        self.model.typed.pop()
        assert self.model.typed == list(range(9))
        self.model.typed.pop(0)
        assert self.model.typed == list(range(1, 9))

    def test_typed_index(self):
        self.model.typed = list(range(10))
        index = self.model.typed.index(5)
        assert index == 5

    def test_typed_count(self):
        self.model.typed = [1] * 10
        count = self.model.typed.count(1)
        assert count == 10

    def test_typed_reverse(self):
        self.model.typed = list(range(10))
        self.model.typed.reverse()
        assert self.model.typed == list(reversed(range(10)))

    def test_typed_sort(self):
        self.model.typed = [8, 3, 2, 5, 9]
        self.model.typed.sort()
        assert self.model.typed == [2, 3, 5, 8, 9]
        self.model.typed.sort(reverse=True)
        assert self.model.typed == [9, 8, 5, 3, 2]

    def test_typed_get_item(self):
        self.model.typed = list(range(10))
        assert self.model.typed[3] == 3

    def test_typed_get_slice(self):
        self.model.typed = list(range(10))
        assert self.model.typed[3:8] == list(range(3, 8))

    def test_typed_get_slice_step(self):
        self.model.typed = list(range(10))
        assert self.model.typed[3::2] == list(range(3, 10, 2))

    def test_typed_set_item(self):
        self.model.typed = list(range(10))
        self.model.typed[5] = 42
        assert self.model.typed[5] == 42

    def test_typed_set_slice(self):
        self.model.typed = list(range(5))
        self.model.typed[3:5] = [42, 42]
        assert self.model.typed == [0, 1, 2, 42, 42]

    def test_typed_set_slice_step(self):
        self.model.typed = list(range(5))
        self.model.typed[::2] = [42, 42, 42]
        assert self.model.typed == [42, 1, 42, 3, 42]

    def test_typed_del_item(self):
        self.model.typed = list(range(5))
        del self.model.typed[3]
        assert self.model.typed == [0, 1, 2, 4]

    def test_typed_del_slice(self):
        self.model.typed = list(range(5))
        del self.model.typed[3:]
        assert self.model.typed == list(range(3))

    def test_typed_del_slice_step(self):
        self.model.typed = list(range(10))
        del self.model.typed[::2]
        assert self.model.typed == list(range(1, 10, 2))

    def test_typed_concat(self):
        self.model.typed = list(range(10))
        self.model.typed += list(range(5))
        assert self.model.typed == list(range(10)) + list(range(5))

    def test_typed_repeat(self):
        self.model.typed = list(range(10))
        self.model.typed *= 3
        assert self.model.typed == list(range(10)) * 3


class TestStandardList(ListTestBase):
    """ A test class for the List member.

    """
    def setup_method(self):
        self.model = StandardModel()

    def teardown_method(self):
        self.model = None

    def test_list_types(self):
        assert type(self.model.untyped) == atomlist
        assert type(self.model.typed) == atomlist

    def test_pickle(self):
        data = list(range(10))
        self.model.untyped = data
        self.model.typed = data
        assert data == loads(dumps(self.model.untyped, 0))
        assert data == loads(dumps(self.model.untyped, 1))
        assert data == loads(dumps(self.model.untyped, 2))
        assert data == loads(dumps(self.model.typed, 0))
        assert data == loads(dumps(self.model.typed, 1))
        assert data == loads(dumps(self.model.typed, 2))

    def test_typed_bad_append(self):
        with pytest.raises(TypeError):
            self.model.typed.append(1.0)

    def test_typed_bad_extend(self):
        with pytest.raises(TypeError):
            self.model.typed.extend([1, 2, 3, 'four'])

    def test_typed_bad_insert(self):
        self.model.typed = list(range(10))
        with pytest.raises(TypeError):
            self.model.typed.insert(0, object())

    def test_typed_bad_set_item(self):
        self.model.typed = list(range(10))
        with pytest.raises(TypeError):
            self.model.typed[5] = 42j

    def test_typed_bad_set_slice(self):
        self.model.typed = list(range(5))
        with pytest.raises(TypeError):
            self.model.typed[3:5] = ['None', 'None']

    def test_typed_bad_set_slice_step(self):
        self.model.typed = list(range(5))
        with pytest.raises(TypeError):
            self.model.typed[::2] = [56.7, 56.7, 56.7]

    def test_typed_bad_concat(self):
        self.model.typed = list(range(10))
        with pytest.raises(TypeError):
            self.model.typed += [12, 14, 'bad']


class TestContainerList(TestStandardList):
    """ A test class for the ContainerList.

    """

    def setup_method(self):
        self.model = ContainerModel()

    def teardown_method(self):
        self.model = None

    def test_list_types(self):
        assert type(self.model.untyped) == atomclist
        assert type(self.model.typed) == atomclist


@pytest.yield_fixture
def container_model():
    """ Create the typed model and setup the observers.

    """
    model = ContainerModel()
    model.untyped = list(range(10))
    model.typed = list(range(10))
    model.observe('untyped', model._changed)
    model.observe('typed', model._changed)
    yield model
    model.unobserve('untyped', model._changed)
    model.unobserve('typed', model._changed)


def verify_base_change(model, name):
    assert model.change['type'] == 'container'
    assert model.change['name'] == name
    assert model.change['object'] == model
    assert model.change['value'] == getattr(model, name)


@pytest.mark.parametrize("kind", ('untyped', 'typed'))
def test_container_append(container_model, kind):
    mlist = getattr(container_model, kind)
    mlist.append(1)
    verify_base_change(container_model, kind)
    assert container_model.change['operation'] == 'append'
    assert container_model.change['item'] == 1


@pytest.mark.parametrize("kind", ('untyped', 'typed'))
def test_container_insert(container_model, kind):
    mlist = getattr(container_model, kind)
    mlist.insert(0, 42)
    verify_base_change(container_model, kind)
    assert container_model.change['operation'] == 'insert'
    assert container_model.change['index'] == 0
    assert container_model.change['item'] == 42


@pytest.mark.parametrize("kind", ('untyped', 'typed'))
def test_container_extend(container_model, kind):
    mlist = getattr(container_model, kind)
    mlist.extend(list(range(3)))
    verify_base_change(container_model, kind)
    assert container_model.change['operation'] == 'extend'
    assert container_model.change['items'] == list(range(3))


@pytest.mark.parametrize("kind", ('untyped', 'typed'))
def test_container_remove(container_model, kind):
    mlist = getattr(container_model, kind)
    mlist.remove(5)
    verify_base_change(container_model, kind)
    assert container_model.change['operation'] == 'remove'
    assert container_model.change['item'] == 5


@pytest.mark.parametrize("kind", ('untyped', 'typed'))
def test_container_pop(container_model, kind):
    mlist = getattr(container_model, kind)
    mlist.pop(0)
    verify_base_change(container_model, kind)
    assert container_model.change['operation'] == 'pop'
    assert container_model.change['index'] == 0
    assert container_model.change['item'] == 0


@pytest.mark.parametrize("kind", ('untyped', 'typed'))
def test_container_reverse(container_model, kind):
    mlist = getattr(container_model, kind)
    mlist.reverse()
    verify_base_change(container_model, kind)
    assert container_model.change['operation'] == 'reverse'


@pytest.mark.parametrize("kind", ('untyped', 'typed'))
def test_container_sort(container_model, kind):
    mlist = getattr(container_model, kind)
    mlist.sort()
    verify_base_change(container_model, kind)
    assert container_model.change['operation'] == 'sort'
    assert container_model.change['key'] is None
    assert container_model.change['reverse'] is False

@pytest.mark.parametrize("kind", ('untyped', 'typed'))
def test_container_key_sort(container_model, kind):
    mlist = getattr(container_model, kind)
    key = lambda i: i
    mlist.sort(key=key, reverse=True)
    verify_base_change(container_model, kind)
    assert container_model.change['operation'] == 'sort'
    assert container_model.change['key'] == key
    assert container_model.change['reverse'] is True


@pytest.mark.parametrize("kind", ('untyped', 'typed'))
def test_container_set_item(container_model, kind):
    mlist = getattr(container_model, kind)
    mlist[0] = 42
    verify_base_change(container_model, kind)
    assert container_model.change['operation'] == '__setitem__'
    assert container_model.change['index'] == 0
    assert container_model.change['olditem'] == 0
    assert container_model.change['newitem'] == 42


@pytest.mark.parametrize("kind", ('untyped', 'typed'))
def test_container_set_slice(container_model, kind):
    mlist = getattr(container_model, kind)
    mlist[3:5] = [1, 2, 3]
    verify_base_change(container_model, kind)
    assert container_model.change['operation'] == '__setitem__'
    assert container_model.change['index'] == slice(3, 5, None)
    assert container_model.change['olditem'] == [3, 4]
    assert container_model.change['newitem'] == [1, 2, 3]


@pytest.mark.parametrize("kind", ('untyped', 'typed'))
def test_container_set_slice_step(container_model, kind):
    mlist = getattr(container_model, kind)
    mlist[::2] = [1, 2, 3, 4, 5]
    verify_base_change(container_model, kind)
    assert container_model.change['operation'] == '__setitem__'
    assert container_model.change['index'] == slice(None, None, 2)
    assert container_model.change['olditem'] == [0, 2, 4, 6, 8]
    assert container_model.change['newitem'] == [1, 2, 3, 4, 5]


@pytest.mark.parametrize("kind", ('untyped', 'typed'))
def test_container_del_item(container_model, kind):
    mlist = getattr(container_model, kind)
    del mlist[0]
    verify_base_change(container_model, kind)
    assert container_model.change['operation'] == '__delitem__'
    assert container_model.change['index'] == 0
    assert container_model.change['item'] == 0


@pytest.mark.parametrize("kind", ('untyped', 'typed'))
def test_container_del_slice(container_model, kind):
    mlist = getattr(container_model, kind)
    del mlist[0:5]
    verify_base_change(container_model, kind)
    assert container_model.change['operation'] == '__delitem__'
    assert container_model.change['index'] == slice(0, 5, None)
    assert container_model.change['item'] == list(range(5))


@pytest.mark.parametrize("kind", ('untyped', 'typed'))
def test_container_del_slice_step(container_model, kind):
    mlist = getattr(container_model, kind)
    del mlist[::2]
    verify_base_change(container_model, kind)
    assert container_model.change['operation'] == '__delitem__'
    assert container_model.change['index'] == slice(None, None, 2)
    assert container_model.change['item'] == list(range(10))[::2]


@pytest.mark.parametrize("kind", ('untyped', 'typed'))
def test_container_concat(container_model, kind):
    mlist = getattr(container_model, kind)
    mlist += [1, 2, 3]
    verify_base_change(container_model, kind)
    assert container_model.change['operation'] == '__iadd__'
    assert container_model.change['items'] == [1, 2, 3]


@pytest.mark.parametrize("kind", ('untyped', 'typed'))
def test_container_repeat(container_model, kind):
    mlist = getattr(container_model, kind)
    mlist *= 2
    verify_base_change(container_model, kind)
    assert container_model.change['operation'] == '__imul__'
    assert container_model.change['count'] == 2
