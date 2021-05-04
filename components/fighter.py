from __future__ import annotations

from typing import TYPE_CHECKING
from render_order import RenderOrder
from input_handles import GameOverEventHandler, TaskHandler, MainEventHandler
import colors

from components.base import BaseComponent
##TODO: other people don't play game like you, they're just rocks

if TYPE_CHECKING:
    from engine import Engine

class Person(BaseComponent):
    parent: Actor

 
class Fighter(Person):
    parent: Actor
    def __init__(self, energy: int):
        self.max_energy = energy
        self._energy = energy


    @property
    def energy(self) -> int:
        return self._energy
    
    @property
    def die(self) -> None:
        if self.engine.player is self.parent:
            death_message = "You died!"
            death_message_color = colors.player_die
            self.parent.char = "!"
            self.parent.color = (191, 0, 0)
            self.engine.event_handler = GameOverEventHandler(self.engine)
        else:
            death_message = f"{self.parent.name} needs your help and awaits a response..."
            death_message_color = colors.lite_blue
            self.parent.color = colors.salmon
        self.parent.blocks_movement = False
        self.parent.ai = None
        self.parent.name = f"{self.parent.name} is sleeping..."
        self.parent.render_order = RenderOrder.CORPSE

        self.engine.message_log.add_message(death_message, death_message_color)
    

    @energy.setter
    def energy(self, value: int) -> None:
        self._energy = max(0, min(value, self.max_energy))
        if self._energy == 0 and self.parent.ai:
            self.die
    
    # def create_task(self) -> None:
    #     self.engine.event_handler = TaskHandler(self.engine)
    def resume(self) -> None:
        self.engine.event_handler = MainEventHandler(self.engine)
    
    def heal(self, amount: int) -> int:
        if self.energy == self.max_energy:
            return 0

        new_energy_value = self.energy + amount

        if new_energy_value > self.max_energy:
            new_energy_value = self.max_energy

        amount_recovered = new_energy_value - self.energy

        self.energy = new_energy_value

        return amount_recovered
    