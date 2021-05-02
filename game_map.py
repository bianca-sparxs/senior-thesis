from __future__ import annotations
from typing import Iterable, Optional, TYPE_CHECKING

import numpy as np
import game_tiles
from entity import Actor, Item

from tcod.console import Console

if TYPE_CHECKING:
    from engine import Engine
    from entity import Entity

class Game_Map:
    def __init__(self, engine: Engine, width: int, height: int, entities: Iterable[Entity] = ()):
        self.engine=engine
        self.entities=set(entities)
        self.width, self.height=width, height
        self.tiles=np.full((width, height), fill_value=game_tiles.wall, order="F" ) #reg mode wall
        self.s_tiles=np.full((width, height), fill_value=game_tiles.s_wall, order="F") #seek mode wall
        self.visible=np.full(
            (width, height), 
            fill_value=False, order="F" #order F means...
        ) #tile can see 
        self.explored=np.full(
            (width, height), 
            fill_value=False, order="F"
        ) #tile seen before 

    @property
    def gamemap(self) -> GameMap:
        return self
    
    @property
    def items(self) -> Iterator[Item]:
        yield from (entity for entity in self.entities if isinstance(entity, Item))

    @property
    def actors(self) -> Iterator[Actor]:
        """Iterate over this maps living actors."""
        yield from (
            entity
            for entity in self.entities
            if isinstance(entity, Actor) and entity.is_alive
        )

   #usage: take 
    def get_blocking_entity_at_location(
        self, 
        location_x: int, 
        location_y: int
    ) -> Optional[Entity]:
        for entity in self.entities:
            if (
                entity.blocks_movement 
                and entity.x == location_x 
                and entity.y == location_y
            ):
                return entity

        return None
    
    def get_actor_at_location(self, x: int, y: int) -> Optional[Actor]:
        for actor in self.actors:
            if actor.x == x and actor.y == y:
                return actor

        return None
    
    def get_item_at_location(self, x: int, y: int) -> Optional[Actor]:
        for item in self.items:
            if item.x == x and item.y == y:
                return item

        return None

    def in_bounds(self, x: int, y: int) -> bool:
        """Return True if x and y are inside of the bounds of this map."""
        return 0 <= x < self.width and 0 <= y < self.height

    def render(self, console: Console) -> None:
        entities_sorted_for_rendering = sorted(
            self.entities, key=lambda x: x.render_order.value
        )
        if self.engine.mode == "idle":
            console.tiles_rgb[0:self.width, 0:self.height] = np.select(
                condlist=[self.visible, self.explored],
                choicelist=[self.tiles["light"], self.tiles["dark"]],
                default=game_tiles.SHROUD,
            ) 
        else:
            console.tiles_rgb[0:self.width, 0:self.height] = np.select(
            condlist=[self.visible, self.explored],
            choicelist=[self.s_tiles["light"], self.s_tiles["dark"]],
            default=game_tiles.S_SHROUD,
        )

        for entity in entities_sorted_for_rendering:
            if self.visible[entity.x, entity.y]:
                console.print(
                    x=entity.x, y=entity.y, 
                    string=entity.char, fg=entity.color
                )

    #i'm assuming this will rerender everything in new locations with new colors
