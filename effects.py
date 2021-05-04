from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from engine import Engine

class Effect():
    def __init__(self):
        self.turn_duration = 13; # all debuffs lasts for 12 actions
    # only one player that effect happens to
    # know what buff they currently have (can't have more than one buff at a time, keep it mad simple)
    # know the duration of the buff, (some kinf of apply method)
    # removal method

    @property
    def turn_duration(self):
        return self.turn_duration

    @turn_duration.setter
    def turn_duration(value):
        self.turn_duration = max(0, value)
        if self.turn_duration == 0:
            self.deactivate
    
    def deactivate():
        self.engine.effect = None


    def render_effect(type: str):
        pass

# lowest motivation for all tasks
class Demotivation(Effect):
    def __init__():
        self.type="demotivation"

# highest motivation for all tasks
class Hope(Effect):
    def __init__(self):
        self.type="hope"
        print("you got hope")

# can see whole map
class Clarity(Effect):
    def __init__():
        self.type="clarity"

# FOV radius of 1
class Blindness(Effect):
    pass
