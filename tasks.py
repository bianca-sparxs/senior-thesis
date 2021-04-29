import random

from typing import TYPE_CHECKING

from entity import Actor, Entity
from renderer import render_task

if TYPE_CHECKING:
    from input_handles import TaskHandler
    

def motivation():
    return random.random()

def t_energyGain():
    return random.random()

def special():
    if random.random() > 0.5:
        return False
    return True;

def create_task():
    return {
        "motivation": motivation(),
        "T Energy Gain": t_energyGain(),
        "special": special()
    }

