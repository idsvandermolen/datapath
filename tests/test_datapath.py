"""
Test datapath module
"""

import pytest
from datapath import DataPath


def test_datapath_getitem():
    "Test DataPath.__getitem__."
    data = {"a": {"b": 1, "c": [2], "d": [[3, 4], [5]]}}
    d = DataPath(data)
    assert d.data is data
    assert d["a"] == {"b": 1, "c": [2], "d": [[3, 4], [5]]}
    assert d["a.b"] == 1
    assert d["a.c"] == [2]
    assert d["a.c.0"] == 2
    assert d["a.c[0]"] == 2
    assert d["a.d"] == [[3, 4], [5]]
    assert d["a.d[0]"] == [3, 4]
    assert d["a.d[0][1]"] == 4
    assert d["a.d[1][0]"] == 5
    with pytest.raises(TypeError):
        _ = d["a.b.c"]
    with pytest.raises(KeyError):
        _ = d["a.e"]
    with pytest.raises(IndexError):
        _ = d["a.c.1"]
    with pytest.raises(IndexError):
        _ = d["a.c[1]"]


def test_datapath_getitem_delimiter():
    "Test DataPath.__getitem__ with different delimiter."
    data = {"a": {"b": 1, "c": [2], "d": [[3, 4], [5]]}}
    d = DataPath(data, delimiter="/")
    assert d.data is data
    assert d["a"] == {"b": 1, "c": [2], "d": [[3, 4], [5]]}
    assert d["a/b"] == 1


def test_datapath_quoting():
    "Test double quoting."
    data = {"a": {"0": 1, '"1"': 2}}
    d = DataPath(data)
    assert d.data is data
    assert d['a."0"'] == 1
    assert d['a["0"]'] == 1
    assert d['a.""1""'] == 2
    assert d['a[""1""]'] == 2
    with pytest.raises(KeyError):
        _ = d["a.0"]
    with pytest.raises(KeyError):
        _ = d["a[0]"]
    with pytest.raises(KeyError):
        _ = d["a.1"]
    with pytest.raises(KeyError):
        _ = d["a[1]"]


def test_datapath_quoting_delimiter():
    "Test double quoting with different delmiter."
    data = {"a": {"0": 1, '"1"': 2}}
    d = DataPath(data, delimiter="/")
    assert d.data is data
    assert d['a/"0"'] == 1


def test_datapath_setitem():
    "Test DataPath.__setitem__"
    data = {}
    d = DataPath(data)
    d["a"] = {"b": 1}
    assert d["a"] == {"b": 1}
    d["a.c"] = 2
    assert d["a.c"] == 2


def test_datapath_setitem_delimiter():
    "Test DataPath.__setitem__ with different delimiter."
    data = {}
    d = DataPath(data, delimiter="/")
    d["a"] = {"b": 1}
    assert d["a"] == {"b": 1}
    d["a/c"] = 2
    assert d["a/c"] == 2


def test_datapath_setitem_intermediate():
    "Test DataPath.__setitem__ with create_intermediate."
    data = {}
    d = DataPath(data)
    assert d.data is data
    with pytest.raises(KeyError):
        d["a.b"] = {}
    d = DataPath(data, create_intermediate=True)
    assert d.data is data
    d["a.b"] = {}
    assert d.data == {"a": {"b": {}}}
    d["a.b.c.d.e"] = 1
    assert d.data == {"a": {"b": {"c": {"d": {"e": 1}}}}}


def test_datapath_delitem():
    "Test DataPath.__delitem__"
    data = {"a": {"b": 1}}
    d = DataPath(data)
    assert d.data is data
    del d["a.b"]
    assert d.data == {"a": {}}


def test_datapath_delitem_delimiter():
    "Test DataPath.__delitem__ with different delimiter."
    data = {"a": {"b": 1}}
    d = DataPath(data, delimiter="/")
    assert d.data is data
    del d["a/b"]
    assert d.data == {"a": {}}


def test_datapath_contains():
    "Test DataPath.__contains__"
    data = {"a": {"b": 1}, "c": [{"d": 2}]}
    d = DataPath(data)
    assert "a" in d
    assert "a.b" in d
    assert "c[0].d" in d
    assert "b" not in d
    assert "a.b.c" not in d
    assert "a.c" not in d
    assert "b.c" not in d
    assert "c[0].e" not in d
    assert "c[1]" not in d
    assert "c[1].e" not in d


def test_datapath_contains_delimiter():
    "Test DataPath.__contains__"
    data = {"a": {"b": 1}, "c": [{"d": 2}]}
    d = DataPath(data, delimiter="/")
    assert "a" in d
    assert "a/b" in d


def test_datapath__iter__():
    "Test DataPath.__iter__"
    data = list(range(10))
    d = DataPath(data)
    assert list(_ for _ in d) == data


def test_datapath_get():
    "Test DataPath.get"
    data = {"a": {"b": 1}, "c": [{"d": 2}]}
    d = DataPath(data)
    assert d["a"] == {"b": 1}
    assert d.get("a") == {"b": 1}
    assert d["a.b"] == 1
    assert d.get("a.b") == 1
    assert d.get("b") is None
    assert d.get("b", 1) == 1
    assert d.get("a.c") is None
    assert d.get("a.c", 1) == 1
    assert d.get("c") == [{"d": 2}]
    assert d.get("c[0]") == {"d": 2}
    assert d.get("c.d") is None
    assert d.get("c[0].e") is None
    assert d.get("c[1]") is None
    assert d.get("c[1].d") is None


def test_datapath_get_delimiter():
    "Test DataPath.get with different delimiter."
    data = {"a": {"b": 1}, "c": [{"d": 2}]}
    d = DataPath(data, delimiter="/")
    assert d["a"] == {"b": 1}
    assert d.get("a") == {"b": 1}
    assert d["a/b"] == 1


def test_datapath_repr():
    "Test DataPath.__repr__"
    d = DataPath({})
    assert repr(d) == "DataPath({})"
