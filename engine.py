import tcod as libtcod
from input_handles import key_handles

def main():
    print ("wattup")
    # TODO: screen dimensions as the ratio of monitor, monitor dimensions are ____
    screen_width = 50
    screen_height = 60
    foreground = libtcod.green
    background = libtcod.red

    # player position coordinates:
    px = int(screen_width / 2)
    py = int(screen_height / 2)

    libtcod.console_set_custom_font('arial10x10.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)
    libtcod.console_init_root(screen_width, screen_height, 'Seek', False)

    #set up listeners for mouse and keyboard
    key = libtcod.Key()
    mouse = libtcod.Mouse()

    

    while not libtcod.console_is_window_closed():
        libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS, key, mouse)
        #TODO: deprecated functions, check docs for new version for default fg/bg, quit, & event get
        libtcod.console_set_default_foreground(0, foreground)
        libtcod.console_set_default_background(0, background)
        # libtcod.console_set_char_background(0, 0, 2, libtcod.green, flag=BKGND_DEFAULT)
        libtcod.console_put_char(0, px, py, '@', libtcod.BKGND_NONE)
        libtcod.console_flush()

        ### Parse Actions
        action = key_handles(key)

        #key handles returns dictionary of keypress type and val
        move =  action.get('move')
        fullscreen = action.get('fullscreen')
        g_exit = action.get('exit')
        

        if move:
            dx, dy = move
            px += dx
            py += dy

        if fullscreen:
            libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())

        if g_exit:
            return True

    

if __name__ == "__main__":
    main()