import tcod
from engine import Engine
from game_map import Game_Map
from entity import Entity
from input_handles import EventHandler
from procedures import generate_dungeon



def main():
    print ("wattup")
    # TODO: screen dimensions as the ratio of monitor, monitor dimensions are__
    screen_width = 50
    screen_height = 60

    map_width = 50
    map_height = 50

    tileset = tcod.tileset.load_tilesheet('arial10x10.png', 32, 8, tcod.tileset.CHARMAP_TCOD)

    player = Entity(int(screen_width / 2), int(screen_height / 2), "@", (255, 255, 0))
    npc = Entity(int(screen_width / 2 - 5), int(screen_height / 2), "@", (255, 255, 255))

    game_map = generate_dungeon(map_width, map_height)

    # entities on map on startup:
    entities = {npc, player}

    #set up listeners for mouse and keyboard
    event_handler = EventHandler()
    engine = Engine(game_map=game_map, entities=entities, event_handler=event_handler, player=player)


    with tcod.context.new_terminal(
        screen_width,
        screen_height,
        tileset=tileset,
        title="Seek",
        vsync=True
    ) as context:
        root_console = tcod.Console(screen_width, screen_height, order="F")
        # print(tcod.console.recommended_size())
        while True:
            engine.render(console=root_console, context=context)

            events = tcod.event.wait()

            engine.handle_events(events)


if __name__ == "__main__":
    main()