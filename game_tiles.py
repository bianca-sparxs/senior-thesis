from typing import Tuple
import numpy as np
import colors

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
        ("light", graphic_dt),  # Graphics for when this tile is in FOV.
    ]
)

def new_tile(*, #enforce use of keywords, param order doesn't matter
    walkable: int,
    transparent: int,
    dark: Tuple[int, Tuple[int, int, int], Tuple[int, int, int]],
    light: Tuple[int, Tuple[int, int, int], Tuple[int, int, int]],
    
 ) -> np.ndarray:
    """Helper function for defining individual tile types """
    return np.array((walkable, transparent, dark, light), dtype=tile_dt)

SHROUD = np.array((ord(" "), (255, 255, 255), (0, 0, 0)), dtype=graphic_dt)

floor = new_tile(
    transparent=True, 
    walkable=True, 
    dark=(ord(" "), (255, 255, 255), (50, 50, 150)),
    light=(ord(" "), (255, 255, 255), (200, 180, 50)),
)
wall = new_tile(
    walkable=False, 
    transparent=False, 
    dark=(ord(" "), (0, 255, 255), (0, 0, 100)),
    light=(ord(" "), (255, 255, 255), (200, 180, 50)),
)

#COLOR PALETTE IN SEEK MODE:
s_floor = new_tile(
    transparent=True, 
    walkable=True, 
    dark=(ord(" "), (255, 255, 255), (50, 50, 150)),
    light=(ord(" "), (255, 255, 255), colors.salmon),
)

s_wall = new_tile(
    walkable=False, 
    transparent=False, 
    dark=(ord(" "), (0, 255, 255), (0, 0, 100)),
    light=(ord(" "), (255, 255, 255), colors.light_blue),
)