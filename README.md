# glom-dict

[![ci](https://github.com/Kilo59/glom-dict/workflows/ci/badge.svg)](https://github.com/Kilo59/glom-dict/actions)
[![documentation](https://img.shields.io/badge/docs-mkdocs%20material-blue.svg?style=flat)](https://glom_dict.github.io/glom-dict/)
[![pypi version](https://img.shields.io/pypi/v/glom-dict.svg)](https://pypi.org/project/glom-dict/)

Custom Dictionary with glom path compatible get, set and delete methods.

https://glom.readthedocs.io/en/latest/

For easy access to and operations on nested data.

## Installation

```bash
python -m pip install glom-dict
```

## Examples

```python
>>> from glom_dict import GlomDict
>>> d = GlomDict(my_dict={"a": {"b": "c"}})
>>> d["my_dict.a.b"]
 'c'

>>> d["my_dict.a.b"] = "C"
>>> d["my_dict.a.b"]
 'C'
```

### Better error messages.

```python
>>> d = GlomDict({'a': {'b': None}})
>>> d["a.b.c"]
Traceback (most recent call last):
...
PathAccessError: could not access 'c', index 2 in path Path('a', 'b', 'c'), got error: ...
```

### Glom Paths

```python
from glom_dict import GlomDict, Path
>>> my_path = Path("a", "b", 1)
>>> d = GlomDict({"a": {"b": ["it", "works", "with", "lists", "too"]}})
>>> d[my_path]
'works'
```

For more examples refer to the excellent `glom` tutorial.

https://glom.readthedocs.io/en/latest/tutorial.html

## Details

Based on `collections.UserDict`

Implemented methods

- [x] `__getitem__` - `glom.glom()`
- [x] `__setitem__` - `glom.assign()`
- [x] `__delitem__` - `glom.delete()`
- [ ] `update` - Works but no special behavior
