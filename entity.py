from typing import Tuple, TypeVar, TYPE_CHECKING
import copy

if TYPE_CHECKING:
    from game_map import Game_Map

T = TypeVar("T", bound="Entity")

class Entity:
    """
    A generic object to represent players, enemies, items, etc.
    """
    #python, have to have all non-default args first before default, instead of changing code, just make all args default
    def __init__(
        self, 
        x: int = 0, 
        y: int = 0, 
        char: str = "?", 
        color: Tuple[int, int, int] = (255,255,255),
        name: str = "<NoName>",
        blocks_movement: bool = False
        ):
        self.x = x
        self.y = y
        self.char = char
        self.color = color
        self.name = name
        self.blocks_movement = blocks_movement

    def spawn(self: T, game_map: 'Game_Map', x: int, y: int) -> T:
        """Spawn a copy of this instance at the given location."""
        clone = copy.deepcopy(self)
        clone.x = x
        clone.y = y
        game_map.entities.add(clone)
        return clone

    def move(self, dx: int, dy: int) -> None:
        # Move the entity by a given amount
        self.x += dx
        self.y += dy