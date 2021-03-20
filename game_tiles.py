from typing import Tuple
import numpy as np

#set up structs that are compatible with tcod.Console.tiles_rgb
#ord() -> python func that take a one-char string as arg and return the unicode representation
graphic_dt = np.dtype(
    [
        ("ch", np.int32),
        ("fg", "3B"), #3 unsigned bytes, RGB colors
        ("bg", "3B"),
    ]
)

# Tile struct used for statically defined tile data.
tile_dt = np.dtype(
    [
        ("walkable", np.bool),  # True if this tile can be walked over.
        ("transparent", np.bool),  # True if this tile doesn't block FOV.
        ("dark", graphic_dt),  # Graphics for when this tile is not in FOV.
    ]
)

def new_tile(*, #enforce use of keywords, param order doesn't matter
    walkable: int,
    transparent: int,
    dark: Tuple[int, Tuple[int, int, int], Tuple[int, int, int]],
 ) -> np.ndarray:
    """Helper function for defining individual tile types """
    return np.array((walkable, transparent, dark), dtype=tile_dt)

floor = new_tile(
    transparent=True, walkable=True, dark=(ord("F"), (255, 0, 255), (50, 50, 150)),
)
wall = new_tile(
    walkable=False, transparent=False, dark=(ord("W"), (0, 255, 255), (0, 0, 100)),
)