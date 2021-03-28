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

class GameModeAction(Action):
    def perform(self, engine: Engine, entity: Entity) -> None:
        return engine.rerender()
    pass

#super class that will hold the movement from the input handle
class ActionWithDirection(Action):
    def __init__(self, dx: int, dy: int):
        super().__init__()

        self.dx = dx
        self.dy = dy
    
    #each subclass needs a perform method
    def perform(self, engine: Engine, entity: Entity) -> None:
        raise NotImplementedError()

#perform movement action is blocking, else do initiate task 
class BumpAction(ActionWithDirection):
    def perform(self, engine: Engine, entity: Entity) -> None:
        dest_x = entity.x + self.dx
        dest_y = entity.y + self.dy

        if engine.game_map.get_blocking_entity_at_location(dest_x, dest_y):
            return InitiateAction(self.dx, self.dy).perform(engine, entity)

        else:
            return MovementAction(self.dx, self.dy).perform(engine, entity)

#equivalent of melee actions
class InitiateAction(ActionWithDirection):
    def perform(self, engine: Engine, entity: Entity) -> None:
        dest_x = entity.x + self.dx
        dest_y = entity.y + self.dy
        target = engine.game_map.get_blocking_entity_at_location(dest_x, dest_y)
        if not target:
            return  # No entity to attack.

        print(f"You inquire about {target.name}'s well being.")


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
        if engine.game_map.get_blocking_entity_at_location(dest_x, dest_y):
            return #destination is blocked by entity

        
        entity.move(dx=self.dx, dy=self.dy)

