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
        self.downstairs_location = (0, 0)

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
        elif self.engine.mode == "seek":
            console.tiles_rgb[0:self.width, 0:self.height] = np.select(
            condlist=[self.visible, self.explored],
            choicelist=[self.tiles["light"], self.tiles["dark"]],
            default=game_tiles.S_SHROUD,
        )

        for entity in entities_sorted_for_rendering:
            if self.visible[entity.x, entity.y]:
                console.print(
                    x=entity.x, y=entity.y, 
                    string=entity.char, fg=entity.color
                )

    #i'm assuming this will rerender everything in new locations with new colors
class GameWorld:
    """
    Holds the settings for the GameMap, and generates new maps when moving down the stairs.
    """

    def __init__(
        self,
        *,
        engine: Engine,
        m_width: int,
        m_height: int,
        max_rooms: int,
        room_min_size: int,
        room_max_size: int,
        monster_max: int,
        items_max: int,
        current_floor: int = 0
    ):
        self.engine = engine

        self.m_width = m_width
        self.m_height = m_height

        self.max_rooms = max_rooms

        self.room_min_size = room_min_size
        self.room_max_size = room_max_size

        self.monster_max = monster_max
        self.items_max = items_max

        self.current_floor = current_floor

    def generate_floor(self) -> None:
        from procedures import generate_dungeon

        self.current_floor += 1

        self.engine.game_map = generate_dungeon(
            max_rooms=self.max_rooms,
            room_min_size=self.room_min_size,
            room_max_size=self.room_max_size,
            m_width=self.m_width,
            m_height=self.m_height,
            monster_max=self.monster_max,
            items_max=self.items_max,
            engine=self.engine,
        )