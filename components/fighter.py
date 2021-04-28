from __future__ import annotations

from typing import TYPE_CHECKING
from render_order import RenderOrder
from input_handles import GameOverEventHandler, TaskHandler, MainEventHandler
import colors

from components.base import BaseComponent
##TODO: other people don't play game like you, they're just rocks

if TYPE_CHECKING:
    from entity import Actor

class Person(BaseComponent):
    entity: Actor

 
class Fighter(Person):
    entity: Actor
    def __init__(self, energy: int):
        self.max_energy = energy
        self._energy = energy


    @property
    def energy(self) -> int:
        return self._energy
    
    @property
    def die(self) -> None:
        if self.engine.player is self.entity:
            death_message = "You died!"
            death_message_color = colors.player_die
            self.entity.char = "%"
            self.entity.color = (191, 0, 0)
            self.engine.event_handler = GameOverEventHandler(self.engine)
        else:
            death_message = f"{self.entity.name} waits for a response..."
            death_message_color = colors.lite_blue
            self.entity.char = "T"
            self.entity.color = colors.salmon
        self.entity.blocks_movement = False
        self.entity.ai = None
        self.entity.name = f"{self.entity.name} is sleeping..."
        self.entity.render_order = RenderOrder.CORPSE

        self.engine.message_log.add_message(death_message, death_message_color)
        self.engine.message_log.add_message(str(self.engine.scorekeeper.score), colors.white)
    
    

    @energy.setter
    def energy(self, value: int) -> None:
        self._energy = max(0, min(value, self.max_energy))
        if self._energy == 0 and self.entity.ai:
            self.die
    
    # def create_task(self) -> None:
    #     self.engine.event_handler = TaskHandler(self.engine)
    def resume(self) -> None:
        self.engine.event_handler = MainEventHandler(self.engine)
    