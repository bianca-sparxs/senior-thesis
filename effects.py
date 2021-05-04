from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from engine import Engine

"""
    apply effect onto engine as a string
    tasks.py and updateFOV(in engine.py) will check if there is an effect,
    then change params based on effect tag
"""
class Effect():
    def __init__(self, engine: Engine):
        self.engine = engine
        self.turns = 13 # all debuffs lasts for 12 actions
    # only one player that effect happens to
    # know what buff they currently have (can't have more than one buff at a time, keep it mad simple)
    # know the duration of the buff, (some kinf of apply method)
    # removal method

    @property
    def turn_duration(self) -> int:
        print(self.turns)
        return self.turns
    
    @property
    def deactivate(self):
        print("deactivae")
        self.engine.effect = None

    @turn_duration.setter
    def turn_duration(self, value: int):
        self.turns = max(0, value)
        if self.turns == 0:
            self.deactivate

    


    def render_effect(type: str):
        pass

# lowest motivation for all tasks
class Demotivation(Effect):
    def __init__(self, engine: Engine):
        super().__init__(engine)
        self.type="demotivation"

# highest motivation for all tasks
class Hope(Effect):
    def __init__(self, engine: Engine):
        super().__init__(engine)
        self.type="hope"
        print("you got hope")

# can see whole map
class Clarity(Effect):
    def __init__(self, engine: Engine):
        super().__init__(engine)
        self.type="clarity"

# FOV radius of 1
class Blindness(Effect):
    def __init__(self, engine: Engine):
        super().__init__(engine)
        self.type="blindness"
