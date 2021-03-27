import tcod
from input_handles import EventHandler
from actions import EscapeAction, MovementAction
from entity import Entity
from game_map import Game_Map

from typing import Iterable, Any

from tcod.context import Context
from tcod.console import Console
from tcod.map import compute_fov

# TODO: enviroment keeps track of two game modes seek and idle. need to edit input_handle & main(?)

class Engine:
    def __init__(self, event_handler: EventHandler, player: Entity, game_map: Game_Map):
        self.event_handler = event_handler
        self.player = player
        self.game_map = game_map
        self.update_fov()

    def others_handleturn(self) -> None:
        for entity in self.game_map.entities - {self.player}:
            print(f'The {entity.name} wonders when it will get to take a real turn.')

    def handle_events(self, events: Iterable[Any]) -> None:
        for event in events:
            action = self.event_handler.dispatch(event)

            if action is None:
                continue

            action.perform(self, self.player)
            self.others_handleturn()

            self.update_fov() #update field of view after actions
    
    def update_fov(self) -> None:
        # print('update!')
        self.game_map.visible[:] = compute_fov(
            self.game_map.tiles["transparent"],
            (self.player.x, self.player.y),
            radius=8,
        )

        self.game_map.explored |= self.game_map.visible #visible tiles get added to explore




    def render(self, console: Console, context: Context) -> None:
        self.game_map.render(console)

        context.present(console)

        console.clear()


