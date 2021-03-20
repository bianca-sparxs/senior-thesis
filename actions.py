from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from engine import Engine
    from entity import Entity

class Action:
    """ all subclasses must invoke a perform method that takes:
        @params: 
            - entity: thing that will be changed (either player or entities)
            - engine:  the game engine context
    """
    def perform(self, engine: Engine, entity: Entity) -> None:
        raise NotImplementedError()



class EscapeAction(Action):
    def perform(self, engine: Engine, entity: Entity) -> None:
        raise SystemExit()

    pass


class MovementAction(Action):
    def __init__(self, dx: int, dy: int):
        super().__init__()

        self.dx = dx
        self.dy = dy

    def perform(self, engine: Engine, entity: Entity) -> None:
        dest_x = self.dx + entity.x
        dest_y = self.dy + entity.y

        if not engine.game_map.in_bounds(dest_x, dest_y):
            return  # Destination is out of bounds.
        if not engine.game_map.tiles["walkable"][dest_x, dest_y]:
            return  # Destination is blocked by a tile.

        
        entity.move(dx=self.dx, dy=self.dy)

