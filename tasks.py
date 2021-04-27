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
    return True;

def create_task(self, entity: Entity):

    pass
    
