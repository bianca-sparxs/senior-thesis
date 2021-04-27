# import tcod
from __future__ import annotations
from typing import TYPE_CHECKING

from tcod.console import Console
from tcod.map import compute_fov

from input_handles import MainEventHandler
from renderer import render_bar, render_task
from message_log import MessageLog
import colors


if TYPE_CHECKING:
    from entity import Actor
    from game_map import Game_Map
    from input_handles import EventHandler
  

class Engine:
    game_map: Game_Map

    def __init__(self, player: Actor):
        self.event_handler: EventHandler = MainEventHandler(self)
        self.mode = "idle"
        self.player = player
        self.message_log = MessageLog()
    
    # @property
    # def task(self, console: Console, motivation: int, T_energy: int, special: bool):
    #     return render_task(console, motivation, special)
    

    #change color of game_map
    def rerender(self):
        if self.mode == "idle":
            self.mode = "seek"
        else:
            self.mode = "idle"
        self.message_log.add_message(self.mode, colors.lite_blue)

    def others_handleturn(self) -> None:
        for entity in set(self.game_map.actors) - {self.player}:
            if entity.ai:
                entity.ai.perform()
    
    def update_fov(self) -> None:
        # print('update!')
        self.game_map.visible[:] = compute_fov(
            self.game_map.tiles["transparent"],
            (self.player.x, self.player.y),
            radius=8,
        )

        self.game_map.explored |= self.game_map.visible #visible tiles get added to explore
    
    #energy degenerates as you play
    #TODO: smart way to decrease energy
    def decrease_energy(self) -> None:
        self.player.fighter.energy -= 2

    def render(self, console: Console) -> None:
        self.game_map.render(console)
        self.message_log.render(console=console, x=21, y=45, width=40, height=5)
        render_bar(
            console=console,
            current_value=self.player.fighter.energy,
            maximum_value=self.player.fighter.max_energy,
            total_width=33
        )

