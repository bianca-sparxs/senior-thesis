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
    gamemap: Game_Map
    
    def __init__(
        self, 
        gamemap: Optional[Game_Map] = None,
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
        if gamemap:
            # If gamemap isn't provided now then it will be set later.
            self.gamemap = gamemap
            gamemap.entities.add(self)

    def spawn(self: T, gamemap: Game_Map, x: int, y: int) -> T:
        """Spawn a copy of this instance at the given location."""
        clone = copy.deepcopy(self)
        clone.x = x
        clone.y = y
        clone.gamemap = gamemap
        gamemap.entities.add(clone)
        return clone
    
    def place(self, x: int, y: int, gamemap: Optional[Game_Map] = None) -> None:
        """Place this entity at a new location.  Handles moving across GameMaps."""
        self.x = x
        self.y = y
        if gamemap:
            if hasattr(self, "gamemap"):  # Possibly uninitialized.
                self.gamemap.entities.remove(self)
            self.gamemap = gamemap
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
            self.fighter.entity = self

    @property
    def is_alive(self) -> bool:
        """Returns True as long as this actor can perform actions."""
        return bool(self.ai)
    
    
