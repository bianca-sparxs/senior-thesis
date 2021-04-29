import tcod
import copy
# from typing import TYPE_CHECKING

from engine import Engine
import entity_maker
import colors
from procedures import generate_dungeon



def main():
    print ("wattup")
    # TODO: screen dimensions as the ratio of monitor, monitor dimensions are__

    screen_width = 35
    screen_height = 35
    # FLAGS = tcod.context.SDL_WINDOW_MAXIMIZED

    map_width = 35
    map_height = 30
    room_max_size = 10
    room_min_size = 6
    max_rooms = 30
    monster_max = 2 #max amt of monsters in a room

 
    tileset = tcod.tileset.load_tilesheet('dejavu16x16.png', 32, 8, tcod.tileset.CHARMAP_TCOD)

    player = copy.deepcopy(entity_maker.player)
    
    engine = Engine(player=player)

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
    engine.message_log.add_message(
        "Anyone who thinks sitting in a church makes you saint must think sitting in a garage makes you a car.", colors.lite_green
    )

    with tcod.context.new_terminal(
        screen_width,
        screen_height,
        tileset=tileset,
        title="Seek",
        vsync=True,
    ) as context:
        root_console = tcod.Console(screen_width, screen_height, order="F")
        # tcod.lib.SDL_SetWindowFullscreen(context.sdl_window_p,tcod.lib.SDL_WINDOW_FULLSCREEN_DESKTOP)
        # fullscreen = tcod.lib.SDL_GetWindowFlags(context.sdl_window_p) & (
        # tcod.lib.SDL_WINDOW_FULLSCREEN | tcod.lib.SDL_WINDOW_FULLSCREEN_DESKTOP
        #  )
        # tcod.lib.SDL_SetWindowFullscreen(
        #     context.sdl_window_p,
        #     0 if fullscreen else tcod.lib.SDL_WINDOW_FULLSCREEN_DESKTOP,
        # )
        
        while True:
            # tcod.console.recommended_size()
            root_console.clear()
            engine.event_handler.on_render(console=root_console)
            context.present(root_console)

            engine.event_handler.handle_events(context)

            


if __name__ == "__main__":
    main()