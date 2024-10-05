"""
Provide access to data structures using a path expression.

Use JSONPath like path spec. Split path in segments by delimiter (default ".")
Support both keys and indices as path segments, but also item[key] as path segment
If you want to evaluate numbers as strings, quote the value with double quotes. If you
want to start and end a value with double quotes, you need to double quote them again
with double quotes.
"""

import re
from typing import Callable, Any, Tuple

__all__ = ["DataPath"]


class DataPath:
    "Access data with path spec."

    def __init__(
        self,
        data,
        delimiter: str = ".",
        create_intermediate=False,
        intermediate: Callable = dict,
    ):
        """Initialise with data object.

        `delimiter` is the character used to split the path into segments.
        If `create_intermediate` is True, intermediate items are created by calling `intermediate` if they do not exist.
        """
        self.data = data
        self.delimiter = delimiter
        self.create_intermediate = create_intermediate
        self.intermediate = intermediate

    def parse_path(self, path: str, delimiter: str = ".") -> list:
        "Parse path into list of strings and integers."
        out = []
        if path:
            # split on delimiter or [index]
            for segment in re.split(r"\[([^\]]+)\]|" + re.escape(delimiter), path):
                if segment in ("", None):
                    # "" when matching more than once (brackets and delimiter like '[a].b') or 'a..b'
                    # None when matching without regex group, i.e 'a.b'
                    continue
                if segment.startswith('"') and segment.endswith('"'):
                    # remove double quotes
                    out.append(segment[1:-1])
                    continue
                try:
                    # try if it is a integer index
                    out.append(int(segment))
                except ValueError as _:
                    out.append(segment)
        return out

    def _get_path(self, path: str) -> Tuple[Any, Any]:
        # return find(self.data, parse_path(path, delimiter=self.delimiter))
        """Get path in data.

        Returns a tuple with the reference to the item before the last path segment and the last path segment.
        """
        ref = self.data
        segments = self.parse_path(path, delimiter=self.delimiter)
        for segment in segments[:-1]:
            ref = ref[segment]

        return ref, segments[-1]

    def _set_path(self, path: str, value: Any) -> None:
        """Set path in data to value.

        Intermediate items are created by calling `intermediate` if they do not exist.
        """
        segments = self.parse_path(path, delimiter=self.delimiter)
        ref = self.data
        for segment in segments[:-1]:
            try:
                ref = ref[segment]
            except Exception as _:
                ref[segment] = self.intermediate()
                ref = ref[segment]
        ref[segments[-1]] = value

    def __getitem__(self, path: str) -> Any:
        "Return data at path."
        ref, key = self._get_path(path)
        return ref[key]

    def __setitem__(self, path: str, value: Any) -> None:
        "Set data at path to value."
        if self.create_intermediate:
            self._set_path(path, value)
        else:
            ref, key = self._get_path(path)
            ref[key] = value

    def __delitem__(self, path: str) -> None:
        "Delete item at path."
        ref, key = self._get_path(path)
        del ref[key]

    def __contains__(self, path: str) -> bool:
        "True if path exists, False otherwise."
        try:
            _ = self[path]
            return True
        except Exception as _:
            return False

    def __iter__(self) -> Any:
        "Iterate over items and return next."
        for _ in self.data:
            yield _

    def get(self, path: str, default=None) -> Any:
        "Return the value for path if path exists, else default."
        try:
            return self[path]
        except Exception as _:
            return default

    def __repr__(self) -> str:
        "Return repr(self)."
        return f"{self.__class__.__name__}({repr(self.data)})"
