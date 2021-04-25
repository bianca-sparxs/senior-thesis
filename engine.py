# import tcod
from __future__ import annotations
from typing import TYPE_CHECKING

from tcod.context import Context
from tcod.console import Console
from tcod.map import compute_fov

from input_handles import MainEventHandler

if TYPE_CHECKING:
    from entity import Actor
    from game_map import Game_Map
    from input_handles import EventHandler
    
    


class Engine:
    game_map: Game_Map

    def __init__(self, player: Actor, mode: str):
        self.event_handler: EventHandler = MainEventHandler(self)
        self.mode = mode
        self.player = player

    #change color of game_map
    def rerender(self):
        if self.mode == "idle":
            self.mode = "seek"
        else:
            self.mode = "idle"
        print(self.mode)

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




    def render(self, console: Console, context: Context) -> None:
        self.game_map.render(console)

        console.print(
            x=1,
            y=47,
            string=f"HP: {self.player.fighter.energy}/{self.player.fighter.max_energy}",
        )

        context.present(console)

        console.clear()


