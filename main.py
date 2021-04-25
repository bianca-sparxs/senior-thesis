import tcod
import copy
# from typing import TYPE_CHECKING

from engine import Engine
import entity_maker
from procedures import generate_dungeon



def main():
    print ("wattup")
    # TODO: screen dimensions as the ratio of monitor, monitor dimensions are__

    screen_width = 50
    screen_height = 60
    # FLAGS = tcod.context.SDL_WINDOW_MAXIMIZED

    map_width = 50
    map_height = 50
    room_max_size = 10
    room_min_size = 6
    max_rooms = 30
    monster_max = 2 #max amt of monsters in a room

 
    tileset = tcod.tileset.load_tilesheet('arial10x10.png', 32, 8, tcod.tileset.CHARMAP_TCOD)

    player = copy.deepcopy(entity_maker.player)
    
    engine = Engine(player=player, mode="idle")

    engine.game_map = generate_dungeon(
        m_width=map_width, 
        m_height=map_height, 
        max_rooms=max_rooms, 
        room_min_size=room_min_size, 
        room_max_size=room_max_size, 
        monster_max=monster_max, 
        engine=engine
    )
    engine.update_fov()

    with tcod.context.new_terminal(
        screen_width,
        screen_height,
        tileset=tileset,
        title="Seek",
        vsync=True,
    ) as context:
        root_console = tcod.Console(screen_width, screen_height, order="F")
        # print(tcod.console.recommended_size())
        while True:
            engine.render(console=root_console, context=context)
            engine.event_handler.handle_events()


if __name__ == "__main__":
    main()