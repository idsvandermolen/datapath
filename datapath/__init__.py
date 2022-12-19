"""
Provide access to data structures using a path expression.

Use JSONPath like path spec. Split path in segments by delimiter (default ".")
Support both keys and indices as path segments, but also key[index] as path segment
"""
import re

__all__ = ["parse_path", "find", "DataPath"]


def parse_path(path: str, delimiter: str = "."):
    "Parse path into list of strings and integers."
    out = []
    if path:
        # split on delimiter or [index]
        for segment in re.split(r"\[(\d+)\]|" + re.escape(delimiter), path):
            if segment in ("", None):
                continue
            try:
                out.append(int(segment))
            except ValueError as _:
                out.append(segment)
    return out


def find(data, path: list):
    "Find path in data."
    ref = data
    for segment in path[:-1]:
        ref = ref[segment]
    key = path[-1]

    return ref, key


class DataPath:
    "Access data with path spec."

    def __init__(self, data):
        """Initialise with data object.

        data object should raise either KeyError or IndexError when an item does not exists
        """
        self.data = data

    def __getitem__(self, path):
        "Return data at path."
        ref, key = find(self.data, parse_path(path))
        return ref[key]

    def __setitem__(self, path, value):
        "Set data at path to value."
        ref, key = find(self.data, parse_path(path))
        ref[key] = value

    def __delitem__(self, path):
        "Delete item at path."
        ref, key = find(self.data, parse_path(path))
        del ref[key]

    def __contains__(self, path) -> bool:
        "True if path exists, False otherwise."
        try:
            _ = self[path]
            return True
        except (KeyError, IndexError) as _:
            return False

    def get(self, path, default=None):
        "Return the value for path if path exists, else default."
        try:
            return self[path]
        except (KeyError, IndexError) as _:
            return default

    def __repr__(self):
        "Return repr(self)."
        return f"{self.__class__.__name__}({repr(self.data)})"
