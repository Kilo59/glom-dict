"""Tests for the `cli` module."""

import collections
from pprint import pformat as pf

import glom as g
import pytest

from glom_dict import GlomDict


@pytest.fixture
def sample() -> dict:
    return {
        "pretty": "standard",
        "a": {"b": {"c": "d"}},
        "a_list": ["hay0", "hay1", "needle", "hay3", "hay4"],
        "my_tuple": (
            0,
            1,
            2,
            {
                "deeply": {
                    "nested": {"key": ["not", "not", "not", "not", "it", "not", "not"]}
                }
            },
        ),
    }


@pytest.mark.parametrize(
    "path, expected",
    [
        (g.Path("pretty"), "standard"),
        (g.Path("a", "b", "c"), "d"),
        (g.Path("a_list", 2), "needle"),
        (g.Path("my_tuple", 3, "deeply", "nested", "key", 4), "it"),
    ],
)
class TestGetItem:
    def test_glom_path(self, sample, path: g.Path, expected):
        gd = GlomDict(**sample)

        assert gd[path] == expected

    def test_str(self, sample, path: g.Path, expected):
        gd = GlomDict(**sample)

        str_path = ".".join(str(p) for p in path.values())
        assert gd[str_path] == expected

    def test_get(self, sample, path, expected):
        gd = GlomDict(**sample)

        assert gd.get(g.Path(*path)) == expected

    def test_get_not_there(self, sample, path, expected):
        gd = GlomDict(**sample)

        glom_path = g.Path(*path[:-1], "not_there")
        print(glom_path)
        assert gd.get(glom_path) is None


@pytest.mark.parametrize(
    "path, value",
    [
        (g.Path("a", "b", "c"), "D"),
        (g.Path("a_list", 2), "ANOTHER_NEEDLE"),
    ],
)
class TestSetItem:
    def test_glom_path(self, sample, path: g.Path, value):
        gd = GlomDict(**sample)

        glom_path = g.Path(*path)
        gd[glom_path] = value
        assert gd[glom_path] == value

    def test_str_path(self, sample, path: g.Path, value):
        gd = GlomDict(**sample)

        str_path = ".".join(str(p) for p in path.values())
        gd[str_path] = value
        assert gd[str_path] == value


class TestAssign:
    @pytest.mark.parametrize(
        "path, value",
        [
            (g.Path("a", "b", "c"), "D"),
            (g.Path("a_list", 2), "ANOTHER_NEEDLE"),
        ],
    )
    def test_simple_assignment(self, sample, path: g.Path, value):
        gd = GlomDict(**sample)

        glom_path = g.Path(*path)
        gd.assign(glom_path, value)
        assert gd[glom_path] == value

    @pytest.mark.parametrize(
        "path, value, missing",
        [
            (g.Path("a", "KEY", "THAT", "DOES NOT"), "EXIST", dict),
            (g.Path("NEEDS", "BACKFILL"), {"foo": "bar"}, dict),
        ],
    )
    def test_assignment_backfill(self, sample, path: g.Path, value, missing):
        gd = GlomDict(**sample)

        gd.assign(path, value, missing=missing)
        print(pf(gd, depth=2))
        assert gd[path] == value


@pytest.mark.parametrize(
    "path, value",
    [
        (g.Path("a", "b", "c"), "d"),
        (g.Path("a_list", 2), "needle"),
    ],
)
class TestDelItem:
    def test_del(self, sample, path: g.Path, value):
        gd = GlomDict(**sample)
        print(gd[path.values()[0]])

        del gd[path]
        assert gd.get(path) != value

    def test_pop(self, sample, path: g.Path, value):
        gd = GlomDict(**sample)
        print(gd[path.values()[0]])

        popped = gd.pop(path)
        assert popped == value
        assert gd.get(path) != value

    def test_pop_not_there(self, sample, path: g.Path, value):
        gd = GlomDict(**sample)

        with pytest.raises(g.PathAccessError):
            gd.pop(g.Path(path.values()[0], "not_there"))

        assert gd[path] == value

    def test_pop_not_there_w_default(self, sample, path: g.Path, value):
        gd = GlomDict(**sample)

        popped = gd.pop(g.Path(path.values()[0], "not_there"), default="DEFAULT")

        assert popped == "DEFAULT"


@pytest.mark.parametrize("type_", [dict, collections.UserDict, GlomDict])
def test_isinstance(type_):
    gd = GlomDict(foo="foo", bar="bar")
    assert isinstance(gd, type_)


def test_init(sample: dict):
    a = GlomDict(sample)
    b = GlomDict(**sample)

    for d in [a, b]:
        assert d["pretty"] == "standard"


if __name__ == "__main__":
    pytest.main(["-vv"])
