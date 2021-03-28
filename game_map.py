import numpy as np
from tcod.console import Console
from typing import Iterable, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from entity import Entity
    
    
import game_tiles

class Game_Map:
    def __init__(self, width: int, height: int, entities: Iterable['Entity'] = ()):
        self.entities=set(entities)
        self.width, self.height=width, height
        self.tiles=np.full((width, height), fill_value=game_tiles.wall, order="F") #order F means...
        self.s_tiles=np.full((width, height), fill_value=game_tiles.s_wall, order="F") #order F means...
        self.visible=np.full((width, height), fill_value=False, order="F")
        self.explored=np.full((width, height), fill_value=False, order="F")

   #usage: take 
    def get_blocking_entity_at_location(self, location_x: int, location_y: int) -> Optional['Entity']:
        for entity in self.entities:
            if entity.blocks_movement and entity.x == location_x and entity.y == location_y:
                return entity

        return None


    def in_bounds(self, x: int, y: int) -> bool:
        """Return True if x and y are inside of the bounds of this map."""
        return 0 <= x < self.width and 0 <= y < self.height

    def render(self, console: Console) -> None:
        console.tiles_rgb[0:self.width, 0:self.height] = np.select(
            condlist=[self.visible, self.explored],
            choicelist=[self.tiles["light"], self.tiles["dark"]],
            default=game_tiles.SHROUD
        ) 
        for entity in self.entities:
            if self.visible[entity.x, entity.y]:
                console.print(x=entity.x, y=entity.y, string=entity.char, fg=entity.color)

    #i'm assuming this will rerender everything in new locations with new colors
    #TODO: make rerender only affect colors not map SAD FACE MAKE GAME IS SO MANY PARTS
    def s_render(self, console: Console) -> None:
        console.tiles_rgb[0:self.width, 0:self.height] = np.select(
            condlist=[self.visible, self.explored],
            choicelist=[self.tiles["light"], self.tiles["dark"]],
            default=game_tiles.SHROUD
        ) 
        for entity in self.entities:
            if self.visible[entity.x, entity.y]:
                console.print(x=entity.x, y=entity.y, string=entity.char, fg=entity.color)
            