import tcod
from input_handles import EventHandler
from actions import EscapeAction, MovementAction

def main():
    print ("wattup")
    # TODO: screen dimensions as the ratio of monitor, monitor dimensions are ____
    screen_width = 50
    screen_height = 60
    # foreground = libtcod.green
    # background = libtcod.red

    # player position coordinates:
    px = int(screen_width / 2)
    py = int(screen_height / 2)

    tileset = tcod.tileset.load_tilesheet('arial10x10.png', 32, 8, tcod.tileset.CHARMAP_TCOD)

    #set up listeners for mouse and keyboard
    event_handler = EventHandler()


    with tcod.context.new_terminal(
        screen_width,
        screen_height,
        tileset=tileset,
        title="Seek",
        vsync=True
    ) as context:
        root_console = tcod.Console(screen_width, screen_height, order="F")
        while True:
            root_console.print(x=px, y=py, string="A")
            context.present(root_console)
            root_console.clear()

            for event in tcod.event.wait():
                ### Parse Actions in Event Queue
                action = event_handler.dispatch(event)

                if action is None:
                    continue

                if isinstance(action, MovementAction):
                    px += action.dx
                    py += action.dy
                
                if isinstance(action, EscapeAction):
                    raise SystemExit()
    

if __name__ == "__main__":
    main()