# datapath
Path based access to items in a data structure

# description
Suppose you have two simple data structures:
```python
config = {
    "foo": {
        "a": 5
    },
    "bar": {
        "baz": [1,2,3]
    }
}

data = {
    "a": {
        "b": 1
    },
    "c": {
        "d": [4,5,6]
    }
}
```
Then you could do something like this:
```python
from datapath import DataPath
c = DataPath(config)
d = DataPath(data)
d["a.b"] = c["foo.a"]
d["c.d[0]"] = c["bar.baz.2"]
d["c[d][1]"] = c["bar[baz].1"]
d["c.d.2"] = c["bar[baz][0]"]
```
See for more examples the [tests](./tests) folder.
