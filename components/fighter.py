from __future__ import annotations

from typing import TYPE_CHECKING
from render_order import RenderOrder

from components.base import BaseComponent
##TODO: other people don't play game like you, they're just rocks

if TYPE_CHECKING:
    from entity import Actor

class Person(BaseComponent):
    entity: Actor

    @property
    def die(self) -> None:
        if self.engine.player is self.entity:
            death_message = "You died!"
        else:
            death_message = f"{self.entity.name} is no longer availble..."

        self.entity.char = "%"
        self.entity.color = (191, 0, 0)
        self.entity.blocks_movement = False
        self.entity.ai = None
        self.entity.name = f"remains of {self.entity.name}"
        self.entity.render_order = RenderOrder.CORPSE

        print(death_message)



class Fighter(Person):
    entity: Actor
    def __init__(self, energy: int):
        self.max_energy = energy
        self._energy = energy


    @property
    def energy(self) -> int:
        return self._energy

    #refactor to make only applicable to player, lets get onto making inteerfaces alreadyyy
    @energy.setter
    def energy(self, value: int) -> None:
        self._energy = max(0, min(value, self.max_energy))
        if self._energy == 0 and self.entity.ai:
            self.die()

    