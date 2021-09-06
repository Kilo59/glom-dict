"""
glom_dict package.

Custom Dictionary with glom get and set methods
"""

from typing import List

from glom import Path, PathAccessError

from .__main__ import GlomDict

__all__: List[str] = ["GlomDict", "Path", "PathAccessError"]
