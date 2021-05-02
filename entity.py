from __future__ import annotations

from typing import Optional, Tuple, TypeVar, TYPE_CHECKING 
import copy

from render_order import RenderOrder

if TYPE_CHECKING:
    from components.ai import BaseAI
    from components.fighter import Fighter
    from game_map import Game_Map

##TODO: entity object carries gamemode as attribute in order to change color


T = TypeVar("T", bound="Entity")
"""
    A generic object to represent players, enemies, items, etc.
    """
    #python, have to have all non-default args first before default, instead of changing code, just make all args default
class Entity:
    parent: Game_Map
    
    def __init__(
        self, 
        parent: Optional[GameMap] = None,
        x: int = 0, 
        y: int = 0, 
        char: str = "?", 
        color: Tuple[int, int, int] = (255,255,255),
        name: str = "<NoName>",
        blocks_movement: bool = False,
        render_order: RenderOrder = RenderOrder.CORPSE,
        ):
        self.x = x
        self.y = y
        self.char = char
        self.color = color
        self.name = name
        self.blocks_movement = blocks_movement
        self.render_order = render_order
        if parent:
            # If gamemap isn't provided now then it will be set later.
            self.parent = parent
            parent.entities.add(self)
    
    @property
    def gamemap(self) -> GameMap:
        return self.parent.gamemap

    def spawn(self: T, gamemap: Game_Map, x: int, y: int) -> T:
        """Spawn a copy of this instance at the given location."""
        clone = copy.deepcopy(self)
        clone.x = x
        clone.y = y
        clone.parent = gamemap
        gamemap.entities.add(clone)
        return clone
    
    def place(self, x: int, y: int, gamemap: Optional[Game_Map] = None) -> None:
        """Place this entity at a new location.  Handles moving across GameMaps."""
        self.x = x
        self.y = y
        if gamemap:
            if hasattr(self, "parent"):  # Possibly uninitialized.
                if self.parent is self.gamemap:
                    self.gamemap.entities.remove(self)
            self.parent = gamemap
            gamemap.entities.add(self)

    def move(self, dx: int, dy: int) -> None:
        # Move the entity by a given amount
        self.x += dx
        self.y += dy

class Actor(Entity):
    def __init__(
        self,
        *,
        x: int = 0,
        y: int = 0,
        char: str = "?",
        color: Tuple[int, int, int] = (255, 255, 255),
        name: str = "<Unnamed>",
        fighter: Fighter, #only player entity is a fighter (for now at least)
        ai_cls: Type[BaseAI],
    ):
        super().__init__( #setting up superclass vars (Entity) from Actor init,
            x=x,
            y=y,
            char=char,
            color=color,
            name=name,
            blocks_movement=True, #every Actor entity is one that blocks mvmnt
            render_order=RenderOrder.ACTOR, 
        )

        self.ai: Optional[BaseAI] = ai_cls(self)

        if fighter:
            self.fighter = fighter
            self.fighter.parent = self

    @property
    def is_alive(self) -> bool:
        """Returns True as long as this actor can perform actions."""
        return bool(self.ai)
    
class Item(Entity):
    def __init__(
        self,
        *,
        x: int = 0,
        y: int = 0,
        char: str = "?",
        color: Tuple[int, int, int] = (255, 255, 255),
        name: str = "<Unnamed>",
        consumable: Consumable,
    ):
        super().__init__(
            x=x,
            y=y,
            char=char,
            color=color,
            name=name,
            blocks_movement=False,
            render_order=RenderOrder.ITEM,
        )

        self.consumable = consumable
        self.consumable.parent = self

    @property
    def is_active(self) -> bool:
         return bool(self.consumable)
    
    
