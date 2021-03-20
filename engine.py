import tcod
from input_handles import EventHandler
from actions import EscapeAction, MovementAction
from entity import Entity
from game_map import Game_Map

from typing import Set, Iterable, Any

from tcod.context import Context
from tcod.console import Console




class Engine:
    def __init__(self, entities: Set[Entity], event_handler: EventHandler, player: Entity, game_map: Game_Map):
        self.entities = entities
        self.event_handler = event_handler
        self.player = player
        self.game_map = game_map

    def handle_events(self, events: Iterable[Any]) -> None:
        for event in events:
            action = self.event_handler.dispatch(event)

            if action is None:
                continue

            action.perform(self, self.player)


    def render(self, console: Console, context: Context) -> None:
        self.game_map.render(console)

        for entity in self.entities:
            console.print(entity.x, entity.y, entity.char, fg=entity.color)

        context.present(console)

        console.clear()


