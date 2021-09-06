import collections
import logging
from typing import Any, Hashable, Union

import glom as g

LOGGER = logging.getLogger("glom-dict")

GlomDictKey = Union[g.Path, Hashable, str]


class GlomDict(collections.UserDict, dict):
    """
    Dict-like object that takes `glom` specs/paths for accessing and assigning nested values.

    Inherits from `collections.UserDict`.
    Underlying dict accessable with `.data`

    Example
    -------
    >>> d = GlomDict(my_dict={"a": {"b": "c"}})
    >>> d["my_dict.a.b"]
    'c'

    Implemented methods
      __getitem__
      __setitem__
      __delitem__
    """

    def __getitem__(self, key: GlomDictKey):
        return g.glom(self.data, key)

    def __setitem__(self, key: GlomDictKey, item: Any) -> None:
        g.assign(self.data, key, item)

    def __delitem__(self, key: GlomDictKey):
        g.delete(self, key)
