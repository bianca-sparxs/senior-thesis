from __future__ import annotations

import random
import tcod
from typing import Iterator, Tuple, List, TYPE_CHECKING
import names

import game_tiles
import entity_maker
from game_map import Game_Map


if TYPE_CHECKING:
    from engine import Engine
    from entity import Entity

class RectangleRoom:
    def __init__(self, x: int, y: int, width: int, height: int):
        self.x1=x
        self.y1=y
        self.x2=x + width
        self.y2=y + height
    
    @property
    def center(self) -> Tuple[int, int]:
        center_x = int((self.x1 + self.x2) /2)
        center_y = int((self.y1 + self.y2) /2)

        return center_x, center_y
    
    @property
    def inner(self) -> Tuple[slice, slice]:
        return slice(self.x1 + 1, self.x2), slice(self.y1 + 1, self.y2)

    def intersects(self, other) -> bool:     
        return (
            self.x1 <= other.x2
            and self.x2 >= other.x1
            and self.y1 <= other.y2
            and self.y2 >= other.y1
        )

### BEGIN NON-CLASS METHODS
#Type hinting: methods are created before classes so if you type-hint a class name
#it must be in strings otherwise you'll get a Name Error IFF you are not using annotations import  


def place_entities(room: RectangleRoom, dungeon: Game_Map, monster_max: int, items_max: int) -> None:
    num_monsters = random.randint(0, monster_max)
    number_of_items = random.randint(0, items_max)

    for i in range(num_monsters):
        x = random.randint(room.x1 + 1, room.x2 - 1)
        y = random.randint(room.y1 + 1, room.y2 - 1)

        if not any(entity.x == x and entity.y == y for entity in dungeon.entities):
            # NOTTODO: if in 'seek' mode and not 'idle'
            # NOTTODO: monster types that change in mode
            other = entity_maker.getUniquePerson()
            other.spawn(x=x, y=y, gamemap=dungeon)
            # if random.random() < 0.8:         #no need for different monster types other ppl are rocks basically
                #spawn monstertype 1
            # else:
                #spawn monstertype 2
        
    for i in range(number_of_items):
        x = random.randint(room.x1 + 1, room.x2 - 1)
        y = random.randint(room.y1 + 1, room.y2 - 1)

        if not any(entity.x == x and entity.y == y for entity in dungeon.entities):
            entity_maker.food.spawn(dungeon, x, y)



def tunneler(start: Tuple[int, int], end: Tuple[int, int]) -> Iterator[Tuple[int, int]]:
    x1, y1 = start
    x2, y2 = end

    if random.random() < 0.5:  # 50% chance.
        # Move horizontally, then vertically.
        corner_x, corner_y = x2, y1
    else:
        # Move vertically, then horizontally.
        corner_x, corner_y = x1, y2

    for x, y in tcod.los.bresenham((x1, y1), (corner_x, corner_y)).tolist():
        yield x, y #yield restarts function with old state x,y
    for x, y in tcod.los.bresenham((corner_x, corner_y), (x2, y2)).tolist():
        yield x, y



def generate_dungeon(
    m_width: int, 
    m_height: int, 
    max_rooms: int, 
    room_min_size: int, 
    room_max_size: int,
    monster_max: int, #max monster per room
    items_max: int, #max item per room
    engine: Engine,
) -> Game_Map:

    player = engine.player
    dungeon = Game_Map(engine, m_width, m_height, entities=[player]);
    rooms: List[RectangleRoom] = []
    center_of_last_room = (0, 0)
    
    for i in range(max_rooms):
        # if random.random() < 0.7:

        #random width,height specified by main.py
        room_w = random.randint(room_min_size, room_max_size)
        room_h = random.randint(room_min_size, room_max_size)

        #random x,y coordinates within map size
        x = random.randint(0, dungeon.width - room_w - 1)
        y = random.randint(0, dungeon.height - room_h - 1)

        nw_room = RectangleRoom(x, y, room_w, room_h)
        center_of_last_room = nw_room.center
        


        #if any runs through all rooms, runs intersect function b/w self and other room
        if any(nw_room.intersects(other) for other in rooms):
            continue
        #dig out room tiles
        dungeon.tiles[nw_room.inner] = game_tiles.floor

        #put player in first room
        if len(rooms) == 0:
            # player.x, player.y = nw_room.center
            player.place(*nw_room.center, dungeon)
        else:
            #put tunnels b/w rest of rooms
            for x,y in tunneler(rooms[-1].center, nw_room.center):
                dungeon.tiles[x, y] = game_tiles.floor

        #push entities to room
        place_entities(room=nw_room, dungeon=dungeon, monster_max=monster_max, items_max=items_max)

        dungeon.tiles[center_of_last_room] = game_tiles.down_stairs
        dungeon.downstairs_location = center_of_last_room

        rooms.append(nw_room)



    # for x,y in tunneler(room_1.center, room_2.center):
    #     dungeon.tiles[x, y] = game_tiles.floor

    # dungeon.tiles[room_1.inner] = game_tiles.floor
    # dungeon.tiles[room_2.inner] = game_tiles.floor

    return dungeon