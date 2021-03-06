# import tcod
from __future__ import annotations
from typing import TYPE_CHECKING

from tcod.console import Console
from tcod.map import compute_fov
from random import random
import exceptions
import numpy as np

from input_handles import IntroScreen
from renderer import render_bar, render_task, render_names_at_mouse_location, render_effect
from message_log import MessageLog
from scorekeeper import ScoreKeeper
import colors
from procedures import generate_dungeon




if TYPE_CHECKING:
    from entity import Actor
    from game_map import Game_Map, GameWorld
    from input_handles import EventHandler
  

class Engine:
    game_map: Game_Map
    game_world: GameWorld

    def __init__(self, player: Actor):
        self.event_handler: EventHandler = IntroScreen(self)
        self.mode = "idle"
        self.player = player
        self.message_log = MessageLog()
        self.mouse_location = (0, 0)
        self.scorekeeper = ScoreKeeper()
        self.effect = None
    
    # @property
    # def task(self, console: Console, motivation: int, T_energy: int, special: bool):
    #     return render_task(console, motivation, special)
    

    #change color of game_map
    def rerender(self):
        if self.mode == "idle":
            self.mode = "seek"
            self.player.color = colors.salmon
            for entity in set(self.game_map.actors) - {self.player}:
                entity.color = colors.welcome_text
            
           
                
            
            #no. of times entered seek mode is part of score
            self.scorekeeper.seek_mode += 1

        else:
            self.mode = "idle"
            if self.effect:
                self.effect.deactivate
            self.player.color = colors.v_dark_purp
            for entity in set(self.game_map.actors) - {self.player}:
                entity.color = colors.bar_filled
        self.message_log.add_message(self.mode, colors.lite_blue)
    


    def others_handleturn(self) -> None:
        for entity in set(self.game_map.actors) - {self.player}:
            if entity.ai:
                try:
                    entity.ai.perform()
                except exceptions.Impossible:
                    pass  # Ignore impossible action exceptions from AI.
    
    def update_fov(self) -> None:
        if self.effect:
            if self.effect.type == "blindness":
                self.game_map.visible[:] = compute_fov(
                    self.game_map.tiles["transparent"],
                    (self.player.x, self.player.y),
                    radius=1,
                )

                #do not add visible tiles to explored
            elif self.effect.type == "clarity":
                self.game_map.visible[:] = compute_fov(
                    self.game_map.tiles["transparent"],
                    (self.player.x, self.player.y),
                    radius=1000,
                )   
            else:
                self.game_map.visible[:] = compute_fov(
                    self.game_map.tiles["transparent"],
                    (self.player.x, self.player.y),
                    radius=8,
                )        

        else:
            self.game_map.visible[:] = compute_fov(
                self.game_map.tiles["transparent"],
                (self.player.x, self.player.y),
                radius=8,
            )

            self.game_map.explored |= self.game_map.visible #visible tiles get added to explore
    
    #energy degenerates as you play
    def decrease_energy(self) -> None:
        if random() > 0.5: #will bring this down to 50/50, just to test game
            self.player.fighter.energy -= 1
            self.scorekeeper.score += 1
            if self.mode == "seek":
                self.scorekeeper.seek_energy_spent += 1

    def render(self, console: Console) -> None:
        self.game_map.render(console)
        self.message_log.render(console=console, x=17, y=30, width=15, height=5)
        render_bar(
            console=console,
            current_value=self.player.fighter.energy,
            maximum_value=self.player.fighter.max_energy,
            total_width=15
        )
        if self.effect:
            render_effect(console=console, type=self.effect.type)
        render_names_at_mouse_location(console=console, x=2, y=4, engine=self)

