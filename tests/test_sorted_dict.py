import copy
import pytest
from swatchbook import SortedDict


def make_sd(*pairs):
    d = SortedDict()
    for k, v in pairs:
        d[k] = v
    return d


def test_insertion_order():
    d = make_sd(('a', 1), ('b', 2), ('c', 3))
    assert list(d.keys()) == ['a', 'b', 'c']
    assert list(d.values()) == [1, 2, 3]


def test_insert_at_index():
    d = make_sd(('a', 1), ('c', 3))
    d.insert(1, 'b', 2)
    assert list(d.keys()) == ['a', 'b', 'c']
    assert list(d.values()) == [1, 2, 3]


def test_setitem_existing_key_preserves_order():
    d = make_sd(('a', 1), ('b', 2), ('c', 3))
    d['b'] = 99
    assert list(d.keys()) == ['a', 'b', 'c']
    assert d['b'] == 99


def test_del_updates_keyorder():
    d = make_sd(('a', 1), ('b', 2), ('c', 3))
    del d['b']
    assert 'b' not in d.keyOrder
    assert list(d.keys()) == ['a', 'c']


def test_pop_with_default():
    d = make_sd(('a', 1))
    result = d.pop('missing', 'default')
    assert result == 'default'
    assert list(d.keys()) == ['a']


def test_pop_existing_key():
    d = make_sd(('a', 1), ('b', 2))
    result = d.pop('a')
    assert result == 1
    assert list(d.keys()) == ['b']


def test_popitem_removes_last():
    d = make_sd(('a', 1), ('b', 2), ('c', 3))
    key, val = d.popitem()
    assert key not in d
    assert key not in d.keyOrder


def test_values_ordered():
    d = make_sd(('x', 10), ('y', 20), ('z', 30))
    assert d.values() == [10, 20, 30]


def test_items_ordered():
    d = make_sd(('x', 10), ('y', 20))
    assert d.items() == [('x', 10), ('y', 20)]


def test_value_for_index():
    d = make_sd(('first', 'A'), ('second', 'B'), ('third', 'C'))
    assert d.value_for_index(0) == 'A'
    assert d.value_for_index(2) == 'C'


def test_deepcopy_independence():
    d = make_sd(('a', [1, 2, 3]))
    d2 = copy.deepcopy(d)
    d2['a'].append(99)
    assert d['a'] == [1, 2, 3]
    assert d2.keyOrder == d.keyOrder


def test_clear():
    d = make_sd(('a', 1), ('b', 2))
    d.clear()
    assert len(d) == 0
    assert d.keyOrder == []


def test_update_preserves_order():
    d = make_sd(('a', 1), ('b', 2))
    d.update({'c': 3})
    assert list(d.keys()) == ['a', 'b', 'c']
    assert d['c'] == 3
