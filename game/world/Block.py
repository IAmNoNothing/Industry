from dataclasses import dataclass
from typing import Any


@dataclass
class Block:
    x: int  # in world pos
    y: int
    chunk: Any  # chunk
    type_: float  # type ([0, 1])
    sprite: int  # sprite index in world.images
    sx: int  # screen pos
    sy: int
    rot_index: int = 0  # [0:3]
