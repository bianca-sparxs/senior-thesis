import numpy as np
from tcod.console import Console

import game_tiles

class Game_Map:
    def __init__(self, width: int, height: int):
        self.width, self.height=width, height
        self.tiles=np.full((width, height), fill_value=game_tiles.wall, order="F") #order F means...
        self.visible=np.full((width, height), fill_value=False, order="F")
        self.explored=np.full((width, height), fill_value=False, order="F")


    def in_bounds(self, x: int, y: int) -> bool:
        """Return True if x and y are inside of the bounds of this map."""
        return 0 <= x < self.width and 0 <= y < self.height

    def render(self, console: Console) -> None:
        console.tiles_rgb[0:self.width, 0:self.height] = np.select(
            condlist=[self.visible, self.explored],
            choicelist=[self.tiles["light"], self.tiles["dark"]],
            default=game_tiles.SHROUD
        ) 