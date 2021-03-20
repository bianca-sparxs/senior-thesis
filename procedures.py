import random
import tcod
from typing import Iterator, Tuple

import game_tiles
from game_map import Game_Map

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

def generate_dungeon(m_width, m_height) -> Game_Map:
    dungeon = Game_Map(m_width, m_height);

    room_1 = RectangleRoom(x=20, y=15, width=10, height=15)
    room_2 = RectangleRoom(x=35, y=15, width=10, height=15)

    for x,y in tunneler(room_1.center, room_2.center):
        dungeon.tiles[x, y] = game_tiles.floor

    dungeon.tiles[room_1.inner] = game_tiles.floor
    dungeon.tiles[room_2.inner] = game_tiles.floor

    return dungeon