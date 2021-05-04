from __future__ import annotations
from typing import Optional, TYPE_CHECKING

import tcod.event

from renderer import render_task
from tasks import create_task
from actions import (
    Action, 
    BumpAction, 
    EscapeAction, 
    GameModeAction, 
    HandleTaskAction,
    TakeStairsAction
)

import colors
import exceptions

if TYPE_CHECKING:
    from engine import Engine
    from actions import InitiateAction

MOVE_KEYS = {
    # Arrow keys.
    tcod.event.K_UP: (0, -1),
    tcod.event.K_DOWN: (0, 1),
    tcod.event.K_LEFT: (-1, 0),
    tcod.event.K_RIGHT: (1, 0),
    tcod.event.K_HOME: (-1, -1),
    tcod.event.K_END: (-1, 1),
    tcod.event.K_PAGEUP: (1, -1),
    tcod.event.K_PAGEDOWN: (1, 1),
    # Numpad keys.
    tcod.event.K_KP_1: (-1, 1),
    tcod.event.K_KP_2: (0, 1),
    tcod.event.K_KP_3: (1, 1),
    tcod.event.K_KP_4: (-1, 0),
    tcod.event.K_KP_6: (1, 0),
    tcod.event.K_KP_7: (-1, -1),
    tcod.event.K_KP_8: (0, -1),
    tcod.event.K_KP_9: (1, -1),
    # Vi keys. #why no wasd ever
    tcod.event.K_h: (-1, 0),
    tcod.event.K_j: (0, 1),
    tcod.event.K_k: (0, -1),
    tcod.event.K_l: (1, 0),
    tcod.event.K_y: (-1, -1),
    tcod.event.K_u: (1, -1),
    tcod.event.K_b: (-1, 1),
    tcod.event.K_n: (1, 1),
}

WAIT_KEYS = {
    tcod.event.K_PERIOD,
    tcod.event.K_KP_5,
    tcod.event.K_CLEAR,
}



class EventHandler(tcod.event.EventDispatch[Action]):
    def __init__(self, engine: Engine):
        self.engine = engine
    
    def handle_events(self, event: tcod.event.Event) -> None:
        self.handle_action(self.dispatch(event))
    
    def handle_action(self, action: Optional[Action]) -> bool:
        """Handle actions returned from event methods.

        Returns True if the action will advance a turn.
        """
        if action is None:
            return False

        try:
            action.perform()
        except exceptions.Impossible as exc:
            self.engine.message_log.add_message(exc.args[0], colors.impossible)
            return False  # Skip enemy turn on exceptions.

        self.engine.others_handleturn()
        self.engine.update_fov() # Update the FOV before the players next action.
        self.engine.decrease_energy()

        return True

    def ev_mousemotion(self, event: tcod.event.MouseMotion) -> None:
        if self.engine.game_map.in_bounds(event.tile.x, event.tile.y):
            self.engine.mouse_location = event.tile.x, event.tile.y

    def ev_quit(self, event: tcod.event.Quit) -> Optional[Action]:
        raise SystemExit()
    
    def on_render(self, console: tcod.Console) -> None:
        self.engine.render(console)

class MainEventHandler(EventHandler):
    
    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[Action]:
        action: Optional[Action] = None
        key = event.sym
        modifier = event.mod
        player = self.engine.player

        #take stairs
        if key == tcod.event.K_PERIOD and modifier & (
            tcod.event.KMOD_LSHIFT | tcod.event.KMOD_RSHIFT
        ):
            return TakeStairsAction(player)

        #movement
        if key in MOVE_KEYS:
            dx, dy = MOVE_KEYS[key]
            action = BumpAction(player, dx, dy)
        elif key in WAIT_KEYS:
            action = WaitAction(player)

        #game mode
        elif key == tcod.event.K_s:
            print("switch game mode")
            action = GameModeAction(player)
        
        #full message log history
        elif key == tcod.event.K_v:
            self.engine.event_handler = HistoryViewer(self.engine)

        #quit game, see score without exit app
        elif key == tcod.event.K_q:
            self.engine.event_handler = GameOverEventHandler(self.engine)


        #exit game
        elif key == tcod.event.K_ESCAPE:
            action = EscapeAction(player)


        # No valid key was pressed
        return action

class TaskHandler(EventHandler):
    def __init__(self, engine: Engine) -> None:
        super().__init__(engine)
        self.task = create_task()
    
    def handle_action(self, action: Optional[Action]) -> bool:
        """Handle actions returned from event methods.

        Returns True if the action will advance a turn.
        """
        if action is None:
            return False

        try:
            action.perform()
        except exceptions.Impossible as exc:
            self.engine.message_log.add_message(exc.args[0], colors.impossible)
            return False  # Skip enemy turn on exceptions.
        
        return True

            
    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[Action]:
        action: Optional[Action] = None
        key = event.sym
        player = self.engine.player
        # print(self.task["motivation"]) 

        #accept/reject task
        if key == tcod.event.K_n:
            action = HandleTaskAction(player).perform(
                decision=False, 
                motivation=self.task["motivation"], 
                t_energyGain=self.task["T Energy Gain"], 
                special=self.task["special"]
            )
        elif key == tcod.event.K_y:
            action = HandleTaskAction(player).perform(
                decision=True, 
                motivation=self.task["motivation"], 
                t_energyGain=self.task["T Energy Gain"], 
                special=self.task["special"]
            )
            

        #quick quit game    
        elif key == tcod.event.K_ESCAPE:
            action = EscapeAction(player)
    
        # No valid key was pressed
        return action
    
    def on_render(self, console: tcod.Console) -> None: # When main switches to this eventHandler, call this on_render
        super().on_render(console)  # Draw the main state as the background.
        # print("render task")
        render_task(console, self.task["motivation"], self.task["T Energy Gain"], self.task["special"])


CURSOR_Y_KEYS = {
    tcod.event.K_UP: -1,
    tcod.event.K_DOWN: 1,
    tcod.event.K_PAGEUP: -10,
    tcod.event.K_PAGEDOWN: 10,
}

class GameOverEventHandler(EventHandler):
    def __init__(self, engine: Engine):
        super().__init__(engine)  
        # self.engine = engine  
        self.engine.scorekeeper.game_over    
        self.log_length = len(self.engine.scorekeeper.score_msgs.messages)
        self.cursor = self.log_length - 1
        
    #render score here
    def handle_action(self, action: Optional[Action]) -> bool:
        """Handle actions returned from event methods.

        Returns True if the action will advance a turn.
        """
        if action is None:
            return False

        try:
            action.perform()
        except exceptions.Impossible as exc:
            self.engine.message_log.add_message(exc.args[0], colors.impossible)
            return False  # Skip enemy turn on exceptions.
        
        return True

    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[Action]:
        action: Optional[Action] = None
        key = event.sym
        player = self.engine.player


        # Fancy conditional movement to make it feel right.
        if key in CURSOR_Y_KEYS:
            adjust = CURSOR_Y_KEYS[key]
            if adjust < 0 and self.cursor == 0:
                # Only move from the top to the bottom when you're on the edge.
                self.cursor = self.log_length - 1
            elif adjust > 0 and self.cursor == self.log_length - 1:
                # Same with bottom to top movement.
                self.cursor = 0
            else:
                # Otherwise move while staying clamped to the bounds of the history log.
                self.cursor = max(0, min(self.cursor + adjust, self.log_length - 1))

        #exit game
        if key == tcod.event.K_ESCAPE:
            action = EscapeAction(player)

        # No valid key was pressed
        return action

    def on_render(self, console: tcod.Console) -> None:
        super().on_render(console)  # Draw the main state as the background.
        
        log_console = tcod.Console(console.width - 6, console.height - 6)

        # Draw a frame with a custom banner title.
        log_console.draw_frame(0, 0, log_console.width, log_console.height)
        log_console.print_box(
            0, 0, log_console.width, 1, "┤Game Over!├", alignment=tcod.CENTER
        )
        
        self.engine.scorekeeper.score_msgs.render_messages(
            log_console,
            1,
            1,
            log_console.width - 2,
            log_console.height - 2,
            self.engine.scorekeeper.score_msgs.messages[: self.cursor + 1],
        )


        log_console.blit(console, 2, 2)

        console.draw_rect(
            x=1, y=31, width=33, height=2, ch=1, bg=colors.descend
        )

        console.print(
        x=3, y=31, string=f"""use arrow keys to scroll \nthrough the score""", fg=colors.bar_text
        )


        




class HistoryViewer(EventHandler):
    """Print the history on a larger window which can be navigated."""

    def __init__(self, engine: Engine):
        super().__init__(engine)
        self.log_length = len(engine.message_log.messages)
        self.cursor = self.log_length - 1

    def on_render(self, console: tcod.Console) -> None:
        super().on_render(console)  # Draw the main state as the background.

        log_console = tcod.Console(console.width - 6, console.height - 6)

        # Draw a frame with a custom banner title.
        log_console.draw_frame(0, 0, log_console.width, log_console.height)
        log_console.print_box(
            0, 0, log_console.width, 1, "┤Message history├", alignment=tcod.CENTER
        )

        # Render the message log using the cursor parameter.
        self.engine.message_log.render_messages(
            log_console,
            1,
            1,
            log_console.width - 2,
            log_console.height - 2,
            self.engine.message_log.messages[: self.cursor + 1],
        )
        log_console.blit(console, 3, 3)

    def ev_keydown(self, event: tcod.event.KeyDown) -> None:
        # Fancy conditional movement to make it feel right.
        if event.sym in CURSOR_Y_KEYS:
            adjust = CURSOR_Y_KEYS[event.sym]
            if adjust < 0 and self.cursor == 0:
                # Only move from the top to the bottom when you're on the edge.
                self.cursor = self.log_length - 1
            elif adjust > 0 and self.cursor == self.log_length - 1:
                # Same with bottom to top movement.
                self.cursor = 0
            else:
                # Otherwise move while staying clamped to the bounds of the history log.
                self.cursor = max(0, min(self.cursor + adjust, self.log_length - 1))
        elif event.sym == tcod.event.K_HOME:
            self.cursor = 0  # Move directly to the top message.
        elif event.sym == tcod.event.K_END:
            self.cursor = self.log_length - 1  # Move directly to the last message.
        else:  # Any other key moves back to the main game state.
            self.engine.event_handler = MainEventHandler(self.engine)
